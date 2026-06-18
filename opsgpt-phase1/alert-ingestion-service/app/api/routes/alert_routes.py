"""Alert ingestion and retrieval endpoints."""

import json
from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.normalized_alert import NormalizedAlert
from app.schemas.alert_schema import (
    AlertSource,
    AlertStatus,
    NormalizedAlertResponse,
    RawAlertResponse,
)
from app.services.alert_forwarder_service import forward_alert_to_analysis
from app.services.alert_normalization_service import (
    get_candidate_alert_id,
    normalize_alert,
)
from app.services.alert_storage_service import (
    get_normalized_alert_or_404,
    get_raw_alert_or_404,
    list_normalized_alerts,
    store_normalized_alert,
    store_raw_alert,
    update_alert_status,
)
from app.services.alert_validation_service import validate_normalized_alert
from app.services.ingestion_log_service import create_ingestion_log
from app.services.project_validation_client import (
    ProjectWebhookValidationError,
    validate_project_webhook,
)
from app.utils.id_generator import generate_alert_id

router = APIRouter(prefix="/alerts", tags=["Alerts"])


def _format_validation_errors(exc: ValidationError) -> list[dict[str, Any]]:
    return exc.errors(include_url=False)


def _ingest_alert(
    db: Session,
    *,
    source: str,
    payload: dict[str, Any],
    project_id: str | None = None,
) -> NormalizedAlert:
    candidate_alert_id = get_candidate_alert_id(source, payload)
    store_raw_alert(
        db,
        alert_id=candidate_alert_id,
        source=source,
        raw_payload=payload,
        project_id=project_id,
    )
    create_ingestion_log(
        db,
        alert_id=candidate_alert_id,
        event_type="alert_received",
        message=f"Raw {source} alert received and stored",
    )

    try:
        normalized_data = normalize_alert(
            source,
            payload,
            candidate_alert_id,
        )
        normalized_data["project_id"] = project_id
        normalized = validate_normalized_alert(normalized_data)
    except ValidationError as exc:
        errors = _format_validation_errors(exc)
        create_ingestion_log(
            db,
            alert_id=candidate_alert_id,
            event_type="alert_rejected",
            message=json.dumps(errors, default=str),
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Alert validation failed",
                "errors": errors,
            },
        ) from exc
    except (TypeError, ValueError) as exc:
        create_ingestion_log(
            db,
            alert_id=candidate_alert_id,
            event_type="alert_rejected",
            message=str(exc),
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Alert normalization failed",
                "errors": [str(exc)],
            },
        ) from exc

    actual_alert_id = normalized.alert_id
    create_ingestion_log(
        db,
        alert_id=actual_alert_id,
        event_type="alert_validated",
        message="Normalized alert fields passed validation",
    )
    processed_alert = normalized.model_copy(
        update={"status": AlertStatus.processed}
    )
    stored_alert = store_normalized_alert(db, processed_alert)
    create_ingestion_log(
        db,
        alert_id=actual_alert_id,
        event_type="alert_normalized",
        message="Alert normalized and stored",
    )

    forwarding_result = forward_alert_to_analysis(stored_alert)
    if not forwarding_result.attempted:
        return stored_alert

    if forwarding_result.succeeded:
        update_alert_status(db, stored_alert, AlertStatus.forwarded)
        create_ingestion_log(
            db,
            alert_id=actual_alert_id,
            event_type="alert_forwarded_to_analysis",
            message=forwarding_result.message,
        )
    else:
        update_alert_status(db, stored_alert, AlertStatus.failed)
        create_ingestion_log(
            db,
            alert_id=actual_alert_id,
            event_type="alert_forward_failed",
            message=forwarding_result.message,
        )
    return stored_alert


@router.post(
    "/webhook/azure-monitor",
    response_model=NormalizedAlertResponse,
    status_code=status.HTTP_201_CREATED,
)
def receive_azure_monitor_alert(
    payload: Annotated[dict[str, Any], Body()],
    db: Annotated[Session, Depends(get_db)],
) -> NormalizedAlert:
    return _ingest_alert(db, source="azure_monitor", payload=payload)


@router.post(
    "/webhook/grafana",
    response_model=NormalizedAlertResponse,
    status_code=status.HTTP_201_CREATED,
)
def receive_grafana_alert(
    payload: Annotated[dict[str, Any], Body()],
    db: Annotated[Session, Depends(get_db)],
) -> NormalizedAlert:
    return _ingest_alert(db, source="grafana", payload=payload)


@router.post(
    "/manual",
    response_model=NormalizedAlertResponse,
    status_code=status.HTTP_201_CREATED,
)
def receive_manual_alert(
    payload: Annotated[dict[str, Any], Body()],
    db: Annotated[Session, Depends(get_db)],
) -> NormalizedAlert:
    return _ingest_alert(db, source="manual", payload=payload)


@router.post(
    "/webhook/project/{project_id}/{webhook_token}",
    response_model=NormalizedAlertResponse,
    status_code=status.HTTP_201_CREATED,
)
def receive_project_alert(
    project_id: str,
    webhook_token: str,
    payload: Annotated[dict[str, Any], Body()],
    db: Annotated[Session, Depends(get_db)],
) -> NormalizedAlert:
    try:
        source = validate_project_webhook(project_id, webhook_token)
    except ProjectWebhookValidationError as exc:
        alert_id = generate_alert_id()
        store_raw_alert(
            db,
            alert_id=alert_id,
            project_id=project_id,
            source="custom",
            raw_payload=payload,
        )
        create_ingestion_log(
            db,
            alert_id=alert_id,
            event_type="alert_rejected",
            message=str(exc),
        )
        raise HTTPException(
            status_code=exc.status_code,
            detail=str(exc),
        ) from exc

    return _ingest_alert(
        db,
        source=source.source_type,
        payload=payload,
        project_id=source.project_id,
    )


@router.get("", response_model=list[NormalizedAlertResponse])
def get_alerts(
    db: Annotated[Session, Depends(get_db)],
    source: AlertSource | None = None,
    alert_status: AlertStatus | None = Query(default=None, alias="status"),
    service_name: str | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[NormalizedAlert]:
    return list_normalized_alerts(
        db,
        source=source.value if source else None,
        alert_status=alert_status.value if alert_status else None,
        service_name=service_name,
        limit=limit,
        offset=offset,
    )


@router.get("/{alert_id}", response_model=NormalizedAlertResponse)
def get_alert(
    alert_id: str,
    db: Annotated[Session, Depends(get_db)],
) -> NormalizedAlert:
    return get_normalized_alert_or_404(db, alert_id)


@router.get("/{alert_id}/raw", response_model=RawAlertResponse)
def get_raw_alert(
    alert_id: str,
    db: Annotated[Session, Depends(get_db)],
) -> RawAlertResponse:
    return RawAlertResponse.model_validate(get_raw_alert_or_404(db, alert_id))
