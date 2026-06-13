"""Correlation time-window helpers."""

from datetime import datetime, timedelta, timezone


def correlation_cutoff(window_minutes: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(minutes=window_minutes)
