"""Notification identifier generation."""

from datetime import datetime, timezone
from secrets import randbelow


def generate_notification_id() -> str:
    year = datetime.now(timezone.utc).year
    return f"NOTIF-{year}-{randbelow(1_000_000):06d}"
