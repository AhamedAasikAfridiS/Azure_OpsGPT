"""Alert identifier generation."""

from datetime import datetime, timezone
from uuid import uuid4


def generate_alert_id() -> str:
    year = datetime.now(timezone.utc).year
    suffix = uuid4().hex[:10].upper()
    return f"ALT-{year}-{suffix}"
