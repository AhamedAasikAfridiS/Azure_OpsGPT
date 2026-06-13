"""Configured notification delivery and retry loop."""

from sqlalchemy.orm import Session

from app.channels.base_channel import BaseNotificationChannel
from app.channels.console_channel import ConsoleChannel
from app.channels.slack_channel import SlackChannel
from app.core.config import Settings, get_settings
from app.models.notification import Notification
from app.services.delivery_attempt_service import create_delivery_attempt


def create_channel(settings: Settings) -> BaseNotificationChannel:
    if settings.notification_channel == "console":
        return ConsoleChannel()
    if settings.notification_channel == "slack":
        return SlackChannel(
            settings.slack_webhook_url,
            settings.notification_timeout_seconds,
        )
    raise ValueError(
        f"Unsupported notification channel: {settings.notification_channel}"
    )


def deliver_with_retry(
    db: Session,
    notification: Notification,
) -> Notification:
    settings = get_settings()
    channel = create_channel(settings)
    last_error: str | None = None

    for attempt_number in range(1, settings.notification_retry_count + 1):
        result = channel.send(notification.message)
        create_delivery_attempt(
            db,
            notification_id=notification.notification_id,
            attempt_number=attempt_number,
            channel=notification.channel,
            status="sent" if result.succeeded else "failed",
            error_message=result.error_message,
        )

        if result.succeeded:
            notification.delivery_status = "sent"
            notification.error_message = None
            db.commit()
            db.refresh(notification)
            return notification

        last_error = result.error_message
        if attempt_number < settings.notification_retry_count:
            notification.delivery_status = "retrying"
            notification.error_message = last_error
            db.commit()

    notification.delivery_status = "failed"
    notification.error_message = last_error or "Notification delivery failed"
    db.commit()
    db.refresh(notification)
    return notification
