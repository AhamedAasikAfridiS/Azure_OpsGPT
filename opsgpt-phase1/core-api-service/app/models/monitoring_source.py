"""Monitoring source metadata owned by the Core API."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class MonitoringSource(Base):
    __tablename__ = "monitoring_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    source_type: Mapped[str] = mapped_column(
        String(40), index=True, nullable=False
    )
    source_name: Mapped[str] = mapped_column(String(160), nullable=False)
    dashboard_url: Mapped[str | None] = mapped_column(String(2000))
    alert_rule_url: Mapped[str | None] = mapped_column(String(2000))
    webhook_token: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    webhook_path: Mapped[str] = mapped_column(
        String(1000), unique=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, index=True, nullable=False
    )
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
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
