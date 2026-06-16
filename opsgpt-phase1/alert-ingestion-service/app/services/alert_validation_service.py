from pydantic import ValidationError

from app.schemas.alert_schema import NormalizedAlertCreate


def validate_normalized_alert(alert_data: dict) -> NormalizedAlertCreate:
    try:
        return NormalizedAlertCreate(**alert_data)
    except ValidationError:
        raise
