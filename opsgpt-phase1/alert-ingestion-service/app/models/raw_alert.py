"""Raw alert payload persistence."""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RawAlert(Base):
    __tablename__ = "raw_alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_id: Mapped[str] = mapped_column(
        String(255), index=True, nullable=False
    )
    project_id: Mapped[str | None] = mapped_column(
        String(50), index=True, nullable=True
    )
    source: Mapped[str] = mapped_column(
        String(50), index=True, nullable=False
    )
    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
