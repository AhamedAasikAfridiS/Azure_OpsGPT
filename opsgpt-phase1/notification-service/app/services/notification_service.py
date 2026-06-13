"""Notification creation, delivery, and history queries."""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.notification import Notification
from app.schemas.notification_schema import NotificationEventRequest
from app.services.retry_service import deliver_with_retry
from app.services.template_service import format_event_message
from app.utils.id_generator import generate_notification_id


def _generate_unique_notification_id(db: Session) -> str:
    while True:
        candidate = generate_notification_id()
        exists = db.scalar(
            select(Notification.id).where(
                Notification.notification_id == candidate
            )
        )
        if exists is None:
            return candidate


def _create_pending_notification(
    db: Session,
    *,
    incident_id: str | None,
    event_type: str,
    message: str,
) -> Notification:
    notification = Notification(
        notification_id=_generate_unique_notification_id(db),
        incident_id=incident_id,
        event_type=event_type,
        channel=get_settings().notification_channel,
        message=message,
        delivery_status="pending",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def process_notification_event(
    db: Session,
    payload: NotificationEventRequest,
) -> Notification:
    notification = _create_pending_notification(
        db,
        incident_id=payload.incident_id,
        event_type=payload.event_type.value,
        message=format_event_message(payload),
    )
    return deliver_with_retry(db, notification)


def process_test_notification(
    db: Session,
    message: str,
) -> Notification:
    notification = _create_pending_notification(
        db,
        incident_id=None,
        event_type="slack_test",
        message=message,
    )
    return deliver_with_retry(db, notification)


def list_notifications(
    db: Session,
    *,
    incident_id: str | None = None,
    event_type: str | None = None,
    delivery_status: str | None = None,
    channel: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Notification]:
    statement = select(Notification)
    if incident_id:
        statement = statement.where(Notification.incident_id == incident_id)
    if event_type:
        statement = statement.where(Notification.event_type == event_type)
    if delivery_status:
        statement = statement.where(
            Notification.delivery_status == delivery_status
        )
    if channel:
        statement = statement.where(Notification.channel == channel)
    statement = (
        statement.order_by(Notification.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def get_notification_or_404(
    db: Session,
    notification_id: str,
) -> Notification:
    notification = db.scalar(
        select(Notification).where(
            Notification.notification_id == notification_id
        )
    )
    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    return notification


def get_incident_notifications(
    db: Session,
    incident_id: str,
) -> list[Notification]:
    return list_notifications(
        db,
        incident_id=incident_id,
        limit=200,
    )
