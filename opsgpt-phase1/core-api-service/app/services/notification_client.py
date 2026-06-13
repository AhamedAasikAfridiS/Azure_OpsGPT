"""Optional HTTP handoff to the Notification Service."""

import logging
from typing import Any

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def send_notification_event(payload: dict[str, Any]) -> bool:
    settings = get_settings()
    if not settings.enable_notifications:
        return False

    try:
        response = httpx.post(
            f"{settings.notification_service_url.rstrip('/')}/notifications/events",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.warning("Notification Service request failed: %s", exc)
        return False
    return True
