"""Normalized alert validation."""

from typing import Any

from app.schemas.alert_schema import NormalizedAlertCreate


def validate_normalized_alert(
    alert_data: dict[str, Any],
) -> NormalizedAlertCreate:
    return NormalizedAlertCreate.model_validate(alert_data)
