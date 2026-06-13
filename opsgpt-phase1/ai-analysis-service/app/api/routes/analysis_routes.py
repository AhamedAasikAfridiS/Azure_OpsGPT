"""AI analysis, correlation, and debugging endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai_clients.base_ai_client import AIProviderError
from app.db.database import get_db
from app.models.analysis_result import AnalysisResult
from app.models.correlation_group import CorrelationGroup
from app.schemas.alert_schema import NormalizedAlertInput
from app.schemas.analysis_schema import (
    AlertAnalysisResponse,
    AnalysisResultResponse,
    FixRequest,
    FixResponse,
    IncidentAnalysisDebugResponse,
    RCARequest,
    RCAResponse,
    SummaryRequest,
    SummaryResponse,
)
from app.schemas.correlation_schema import (
    CorrelateRequest,
    CorrelateResponse,
    CorrelationGroupResponse,
)
from app.schemas.similar_incident_schema import (
    SimilarIncidentRequest,
    SimilarIncidentResponse,
)
from app.services.ai_analysis_service import (
    generate_fix,
    generate_rca,
    generate_summary,
)
from app.services.analysis_orchestrator_service import (
    correlate_alerts_for_development,
    process_normalized_alert,
)
from app.services.similar_incident_service import score_similar_incidents

router = APIRouter(prefix="/analysis", tags=["Analysis"])


def _raise_controlled_ai_error(exc: Exception) -> None:
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=f"AI provider response failed: {exc}",
    ) from exc


@router.post("/alerts", response_model=AlertAnalysisResponse)
def analyze_alert(
    payload: NormalizedAlertInput,
    db: Annotated[Session, Depends(get_db)],
) -> AlertAnalysisResponse:
    return process_normalized_alert(db, payload)


@router.post("/correlate", response_model=CorrelateResponse)
def correlate_alerts(
    payload: CorrelateRequest,
    db: Annotated[Session, Depends(get_db)],
) -> CorrelateResponse:
    groups = correlate_alerts_for_development(db, payload.alerts)
    return CorrelateResponse(
        groups=[
            CorrelationGroupResponse.model_validate(group)
            for group in groups
        ]
    )


@router.post("/generate-summary", response_model=SummaryResponse)
def create_summary(payload: SummaryRequest) -> SummaryResponse:
    try:
        return generate_summary(
            payload.service_name,
            payload.severity.value,
            payload.alerts,
        )
    except (AIProviderError, ValidationError, ValueError) as exc:
        _raise_controlled_ai_error(exc)


@router.post("/generate-rca", response_model=RCAResponse)
def create_rca(payload: RCARequest) -> RCAResponse:
    try:
        return generate_rca(payload.service_name, payload.alerts)
    except (AIProviderError, ValidationError, ValueError) as exc:
        _raise_controlled_ai_error(exc)


@router.post("/generate-fix", response_model=FixResponse)
def create_fix(payload: FixRequest) -> FixResponse:
    try:
        return generate_fix(
            payload.root_cause,
            payload.service_name,
            payload.severity.value,
        )
    except (AIProviderError, ValidationError, ValueError) as exc:
        _raise_controlled_ai_error(exc)


@router.post(
    "/similar-incidents",
    response_model=SimilarIncidentResponse,
)
def find_similar_incidents(
    payload: SimilarIncidentRequest,
) -> SimilarIncidentResponse:
    return score_similar_incidents(payload)


@router.get(
    "/incidents/{incident_id}",
    response_model=IncidentAnalysisDebugResponse,
)
def get_incident_analysis(
    incident_id: str,
    db: Annotated[Session, Depends(get_db)],
) -> IncidentAnalysisDebugResponse:
    analysis = db.scalar(
        select(AnalysisResult)
        .where(AnalysisResult.incident_id == incident_id)
        .order_by(AnalysisResult.created_at.desc())
    )
    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis result not found",
        )

    group = db.scalar(
        select(CorrelationGroup).where(
            CorrelationGroup.correlation_id == analysis.correlation_id
        )
    )
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Correlation group not found",
        )

    return IncidentAnalysisDebugResponse(
        analysis=AnalysisResultResponse.model_validate(analysis),
        correlation_group=CorrelationGroupResponse.model_validate(group),
    )
