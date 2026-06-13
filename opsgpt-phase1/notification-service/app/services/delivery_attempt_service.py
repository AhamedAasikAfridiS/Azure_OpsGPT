"""Notification delivery attempt persistence."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.delivery_attempt import NotificationDeliveryAttempt


def create_delivery_attempt(
    db: Session,
    *,
    notification_id: str,
    attempt_number: int,
    channel: str,
    status: str,
    error_message: str | None = None,
) -> NotificationDeliveryAttempt:
    attempt = NotificationDeliveryAttempt(
        notification_id=notification_id,
        attempt_number=attempt_number,
        channel=channel,
        status=status,
        error_message=error_message,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def list_delivery_attempts(
    db: Session,
    notification_id: str,
) -> list[NotificationDeliveryAttempt]:
    return list(
        db.scalars(
            select(NotificationDeliveryAttempt)
            .where(
                NotificationDeliveryAttempt.notification_id
                == notification_id
            )
            .order_by(
                NotificationDeliveryAttempt.attempt_number.asc(),
                NotificationDeliveryAttempt.attempted_at.asc(),
            )
        )
    )
