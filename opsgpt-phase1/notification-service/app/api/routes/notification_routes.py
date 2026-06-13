"""Notification delivery and history endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.notification import Notification
from app.schemas.notification_schema import (
    DeliveryStatus,
    NotificationChannel,
    NotificationDeliveryResponse,
    NotificationDetailResponse,
    NotificationEventRequest,
    NotificationEventType,
    NotificationResponse,
    SlackTestRequest,
)
from app.services.delivery_attempt_service import list_delivery_attempts
from app.services.notification_service import (
    get_incident_notifications,
    get_notification_or_404,
    list_notifications,
    process_notification_event,
    process_test_notification,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def _delivery_response(
    notification: Notification,
) -> NotificationDeliveryResponse:
    return NotificationDeliveryResponse(
        notification_id=notification.notification_id,
        delivery_status=notification.delivery_status,
        channel=notification.channel,
        error_message=notification.error_message,
    )


@router.post(
    "/events",
    response_model=NotificationDeliveryResponse,
)
def receive_notification_event(
    payload: NotificationEventRequest,
    db: Annotated[Session, Depends(get_db)],
) -> NotificationDeliveryResponse:
    return _delivery_response(process_notification_event(db, payload))


@router.post(
    "/slack/test",
    response_model=NotificationDeliveryResponse,
)
def test_notification_channel(
    payload: SlackTestRequest,
    db: Annotated[Session, Depends(get_db)],
) -> NotificationDeliveryResponse:
    return _delivery_response(
        process_test_notification(db, payload.message)
    )


@router.get("", response_model=list[NotificationResponse])
def get_notifications(
    db: Annotated[Session, Depends(get_db)],
    incident_id: str | None = None,
    event_type: NotificationEventType | None = None,
    delivery_status: DeliveryStatus | None = None,
    channel: NotificationChannel | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Notification]:
    return list_notifications(
        db,
        incident_id=incident_id,
        event_type=event_type.value if event_type else None,
        delivery_status=(
            delivery_status.value if delivery_status else None
        ),
        channel=channel.value if channel else None,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/incident/{incident_id}",
    response_model=list[NotificationResponse],
)
def get_notifications_for_incident(
    incident_id: str,
    db: Annotated[Session, Depends(get_db)],
) -> list[Notification]:
    return get_incident_notifications(db, incident_id)


@router.get(
    "/{notification_id}",
    response_model=NotificationDetailResponse,
)
def get_notification(
    notification_id: str,
    db: Annotated[Session, Depends(get_db)],
) -> NotificationDetailResponse:
    notification = get_notification_or_404(db, notification_id)
    notification_data = NotificationResponse.model_validate(
        notification
    ).model_dump()
    return NotificationDetailResponse(
        **notification_data,
        delivery_attempts=list_delivery_attempts(
            db,
            notification.notification_id,
        ),
    )
