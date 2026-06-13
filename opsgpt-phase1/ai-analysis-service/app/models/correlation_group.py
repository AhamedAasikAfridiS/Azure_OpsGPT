"""Correlated alert group."""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CorrelationGroup(Base):
    __tablename__ = "correlation_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    correlation_id: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    service_name: Mapped[str] = mapped_column(
        String(160), index=True, nullable=False
    )
    environment: Mapped[str] = mapped_column(
        String(30), index=True, nullable=False
    )
    severity: Mapped[str] = mapped_column(
        String(30), index=True, nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(30), default="open", index=True, nullable=False
    )
    related_alert_ids: Mapped[list[Any]] = mapped_column(
        JSON, default=list, nullable=False
    )
    incident_id: Mapped[str | None] = mapped_column(
        String(50), unique=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
