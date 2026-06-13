"""Human-readable identifier generation."""

from datetime import datetime, timezone
from uuid import uuid4


def generate_incident_id() -> str:
    year = datetime.now(timezone.utc).year
    suffix = uuid4().hex[:8].upper()
    return f"INC-{year}-{suffix}"
