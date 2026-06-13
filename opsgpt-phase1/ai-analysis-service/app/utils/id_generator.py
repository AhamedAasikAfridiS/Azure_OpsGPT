"""Stable unique identifier generation."""

from datetime import datetime, timezone
from secrets import randbelow


def generate_incident_id() -> str:
    year = datetime.now(timezone.utc).year
    return f"INC-{year}-{randbelow(1_000_000):06d}"


def generate_correlation_id() -> str:
    year = datetime.now(timezone.utc).year
    return f"CORR-{year}-{randbelow(1_000_000):06d}"
