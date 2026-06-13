"""Normalized alerts stored for analysis."""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Boolean, DateTime, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AnalysisAlert(Base):
    __tablename__ = "analysis_alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_id: Mapped[str] = mapped_column(
        String(255), index=True, nullable=False
    )
    project_id: Mapped[str | None] = mapped_column(
        String(50), index=True, nullable=True
    )
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    service_name: Mapped[str] = mapped_column(
        String(160), index=True, nullable=False
    )
    alert_type: Mapped[str] = mapped_column(
        String(50), index=True, nullable=False
    )
    severity: Mapped[str] = mapped_column(
        String(30), index=True, nullable=False
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    environment: Mapped[str] = mapped_column(
        String(50), index=True, nullable=False
    )
    metric_name: Mapped[str | None] = mapped_column(String(255))
    metric_value: Mapped[Any | None] = mapped_column(JSON)
    threshold: Mapped[str | None] = mapped_column(String(255))
    resource_id: Mapped[str | None] = mapped_column(Text)
    dashboard_url: Mapped[str | None] = mapped_column(Text)
    runbook_url: Mapped[str | None] = mapped_column(Text)
    fired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, index=True, nullable=False
    )
    is_duplicate: Mapped[bool] = mapped_column(
        Boolean, default=False, index=True, nullable=False
    )
