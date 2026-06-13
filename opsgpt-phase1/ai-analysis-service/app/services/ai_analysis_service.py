"""AI provider calls and strict response validation."""

from app.ai_clients.ai_client_factory import create_ai_client
from app.ai_clients.base_ai_client import BaseAIClient
from app.schemas.alert_schema import NormalizedAlertInput
from app.schemas.analysis_schema import (
    AIAnalysisOutput,
    FixResponse,
    RCAResponse,
    SummaryResponse,
)
from app.services.prompt_builder_service import (
    build_fix_prompt,
    build_full_analysis_prompt,
    build_rca_prompt,
    build_summary_prompt,
)


def generate_full_analysis(
    service_name: str,
    severity: str,
    alerts: list,
    client: BaseAIClient | None = None,
) -> tuple[AIAnalysisOutput, dict]:
    ai_client = client or create_ai_client()
    raw_response = ai_client.generate_json(
        build_full_analysis_prompt(service_name, severity, alerts)
    )
    return AIAnalysisOutput.model_validate(raw_response), raw_response


def generate_summary(
    service_name: str,
    severity: str,
    alerts: list[NormalizedAlertInput],
) -> SummaryResponse:
    raw_response = create_ai_client().generate_json(
        build_summary_prompt(service_name, severity, alerts)
    )
    return SummaryResponse.model_validate(raw_response)


def generate_rca(
    service_name: str,
    alerts: list[NormalizedAlertInput],
) -> RCAResponse:
    raw_response = create_ai_client().generate_json(
        build_rca_prompt(service_name, alerts)
    )
    return RCAResponse.model_validate(raw_response)


def generate_fix(
    root_cause: str,
    service_name: str,
    severity: str,
) -> FixResponse:
    raw_response = create_ai_client().generate_json(
        build_fix_prompt(root_cause, service_name, severity)
    )
    return FixResponse.model_validate(raw_response)
