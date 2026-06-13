"""End-to-end normalized alert analysis orchestration."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.analysis_alert import AnalysisAlert
from app.models.analysis_result import AnalysisResult
from app.models.correlation_group import CorrelationGroup
from app.schemas.alert_schema import NormalizedAlertInput
from app.schemas.analysis_schema import AlertAnalysisResponse
from app.schemas.correlation_schema import CorrelationGroupResponse
from app.services.ai_analysis_service import generate_full_analysis
from app.services.analysis_log_service import create_analysis_log
from app.services.core_api_client import (
    CoreAPIError,
    create_core_incident,
    update_core_incident_analysis,
)
from app.services.correlation_service import (
    correlate_alert,
    find_group_for_duplicate,
    get_group_alerts,
    group_has_meaningful_incident_state,
)
from app.services.duplicate_detection_service import find_duplicate_alert
from app.utils.id_generator import generate_incident_id


def _store_alert(
    db: Session,
    payload: NormalizedAlertInput,
    *,
    is_duplicate: bool,
) -> AnalysisAlert:
    alert_data = payload.model_dump(mode="python", exclude={"status"})
    if alert_data["threshold"] is not None:
        alert_data["threshold"] = str(alert_data["threshold"])
    alert = AnalysisAlert(
        **alert_data,
        is_duplicate=is_duplicate,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    create_analysis_log(
        db,
        alert_id=alert.alert_id,
        event_type="alert_received",
        message="Normalized alert received and stored for analysis",
    )
    return alert


def _generate_unique_incident_id(db: Session) -> str:
    while True:
        candidate = generate_incident_id()
        group_exists = db.scalar(
            select(CorrelationGroup.id).where(
                CorrelationGroup.incident_id == candidate
            )
        )
        result_exists = db.scalar(
            select(AnalysisResult.id).where(
                AnalysisResult.incident_id == candidate
            )
        )
        if group_exists is None and result_exists is None:
            return candidate


def _store_failed_result(
    db: Session,
    *,
    incident_id: str,
    correlation_id: str,
    project_id: str | None,
    error_message: str,
    raw_ai_response: dict | None = None,
) -> AnalysisResult:
    result = AnalysisResult(
        incident_id=incident_id,
        project_id=project_id,
        correlation_id=correlation_id,
        raw_ai_response=raw_ai_response,
        analysis_status="failed",
        error_message=error_message,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def _analysis_response(
    alert: AnalysisAlert,
    *,
    duplicate: bool,
    group: CorrelationGroup | None,
    incident_id: str | None,
    analysis_status: str,
    error_message: str | None = None,
) -> AlertAnalysisResponse:
    return AlertAnalysisResponse(
        alert=alert,
        duplicate=duplicate,
        correlation_group=(
            CorrelationGroupResponse.model_validate(group) if group else None
        ),
        incident_id=incident_id,
        analysis_status=analysis_status,
        error_message=error_message,
    )


def process_normalized_alert(
    db: Session,
    payload: NormalizedAlertInput,
) -> AlertAnalysisResponse:
    settings = get_settings()
    duplicate_of = find_duplicate_alert(
        db,
        payload,
        settings.correlation_window_minutes,
    )
    alert = _store_alert(
        db,
        payload,
        is_duplicate=duplicate_of is not None,
    )

    if duplicate_of:
        group = find_group_for_duplicate(
            db,
            duplicate_of,
            settings.correlation_window_minutes,
        )
        create_analysis_log(
            db,
            alert_id=alert.alert_id,
            correlation_id=group.correlation_id if group else None,
            event_type="duplicate_detected",
            message=(
                f"Duplicate of stored analysis alert record "
                f"{duplicate_of.id}; no new incident requested"
            ),
        )
        return _analysis_response(
            alert,
            duplicate=True,
            group=group,
            incident_id=group.incident_id if group else None,
            analysis_status="duplicate",
        )

    group = correlate_alert(
        db,
        alert,
        settings.correlation_window_minutes,
    )
    if not group_has_meaningful_incident_state(db, group):
        return _analysis_response(
            alert,
            duplicate=False,
            group=group,
            incident_id=group.incident_id,
            analysis_status="pending_correlation",
        )

    incident_id = group.incident_id
    if incident_id is None:
        incident_id = _generate_unique_incident_id(db)
        create_analysis_log(
            db,
            alert_id=alert.alert_id,
            correlation_id=group.correlation_id,
            event_type="incident_create_requested",
            message=f"Requesting Core API incident {incident_id}",
        )
        try:
            create_core_incident(
                {
                    "incident_id": incident_id,
                    "project_id": group.project_id,
                    "title": (
                        f"{group.service_name} incident detected - "
                        f"{group.severity}"
                    ),
                    "service_name": group.service_name,
                    "severity": group.severity,
                    "status": "open",
                    "related_alert_ids": group.related_alert_ids,
                }
            )
        except CoreAPIError as exc:
            error_message = str(exc)
            _store_failed_result(
                db,
                incident_id=incident_id,
                correlation_id=group.correlation_id,
                project_id=group.project_id,
                error_message=error_message,
            )
            create_analysis_log(
                db,
                alert_id=alert.alert_id,
                correlation_id=group.correlation_id,
                event_type="core_api_update_failed",
                message=error_message,
            )
            return _analysis_response(
                alert,
                duplicate=False,
                group=group,
                incident_id=None,
                analysis_status="failed",
                error_message=error_message,
            )

        group.incident_id = incident_id
        group.status = "incident_created"
        db.commit()
        db.refresh(group)
        create_analysis_log(
            db,
            alert_id=alert.alert_id,
            correlation_id=group.correlation_id,
            event_type="core_api_update_success",
            message=f"Core API created incident {incident_id}",
        )
    else:
        group.status = "updated"
        db.commit()
        db.refresh(group)

    result = AnalysisResult(
        incident_id=incident_id,
        project_id=group.project_id,
        correlation_id=group.correlation_id,
        analysis_status="pending",
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    group_alerts = get_group_alerts(db, group)
    create_analysis_log(
        db,
        alert_id=alert.alert_id,
        correlation_id=group.correlation_id,
        event_type="ai_prompt_sent",
        message=(
            f"Sent structured analysis prompt using "
            f"AI_PROVIDER={settings.ai_provider}"
        ),
    )

    try:
        analysis, raw_response = generate_full_analysis(
            group.service_name,
            group.severity,
            group_alerts,
        )
    except Exception as exc:
        error_message = f"AI analysis failed: {exc}"
        result.analysis_status = "failed"
        result.error_message = error_message
        db.commit()
        db.refresh(result)
        create_analysis_log(
            db,
            alert_id=alert.alert_id,
            correlation_id=group.correlation_id,
            event_type="ai_analysis_failed",
            message=error_message,
        )
        return _analysis_response(
            alert,
            duplicate=False,
            group=group,
            incident_id=incident_id,
            analysis_status="failed",
            error_message=error_message,
        )

    result.raw_ai_response = raw_response
    result.ai_summary = analysis.incident_summary
    result.root_cause = analysis.root_cause
    result.supporting_evidence = analysis.supporting_evidence
    result.confidence_score = analysis.confidence_score
    result.recommended_fix = analysis.recommended_fix.model_dump()
    db.commit()
    create_analysis_log(
        db,
        alert_id=alert.alert_id,
        correlation_id=group.correlation_id,
        event_type="ai_response_received",
        message="Received and validated JSON from the configured AI provider",
    )

    try:
        update_core_incident_analysis(
            incident_id,
            {
                "ai_summary": analysis.incident_summary,
                "root_cause": analysis.root_cause,
                "supporting_evidence": analysis.supporting_evidence,
                "confidence_score": analysis.confidence_score,
                "recommended_fix": analysis.recommended_fix.model_dump(),
            },
        )
    except CoreAPIError as exc:
        error_message = str(exc)
        result.analysis_status = "failed"
        result.error_message = error_message
        db.commit()
        db.refresh(result)
        create_analysis_log(
            db,
            alert_id=alert.alert_id,
            correlation_id=group.correlation_id,
            event_type="core_api_update_failed",
            message=error_message,
        )
        return _analysis_response(
            alert,
            duplicate=False,
            group=group,
            incident_id=incident_id,
            analysis_status="failed",
            error_message=error_message,
        )

    result.analysis_status = "completed"
    result.error_message = None
    db.commit()
    db.refresh(result)
    create_analysis_log(
        db,
        alert_id=alert.alert_id,
        correlation_id=group.correlation_id,
        event_type="core_api_update_success",
        message=f"Core API analysis updated for incident {incident_id}",
    )
    create_analysis_log(
        db,
        alert_id=alert.alert_id,
        correlation_id=group.correlation_id,
        event_type="ai_analysis_completed",
        message="AI analysis completed and persisted",
    )
    return _analysis_response(
        alert,
        duplicate=False,
        group=group,
        incident_id=incident_id,
        analysis_status="completed",
    )


def correlate_alerts_for_development(
    db: Session,
    alerts: list[NormalizedAlertInput],
) -> list[CorrelationGroup]:
    settings = get_settings()
    groups: dict[str, CorrelationGroup] = {}

    for payload in alerts:
        duplicate_of = find_duplicate_alert(
            db,
            payload,
            settings.correlation_window_minutes,
        )
        alert = _store_alert(
            db,
            payload,
            is_duplicate=duplicate_of is not None,
        )
        if duplicate_of:
            group = find_group_for_duplicate(
                db,
                duplicate_of,
                settings.correlation_window_minutes,
            )
            create_analysis_log(
                db,
                alert_id=alert.alert_id,
                correlation_id=group.correlation_id if group else None,
                event_type="duplicate_detected",
                message="Duplicate detected during manual correlation",
            )
        else:
            group = correlate_alert(
                db,
                alert,
                settings.correlation_window_minutes,
            )
        if group:
            groups[group.correlation_id] = group

    return list(groups.values())
