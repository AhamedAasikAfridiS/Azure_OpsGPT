"""Stored AI analysis result."""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Float, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    incident_id: Mapped[str] = mapped_column(
        String(50), index=True, nullable=False
    )
    project_id: Mapped[str | None] = mapped_column(
        String(50), index=True, nullable=True
    )
    correlation_id: Mapped[str] = mapped_column(
        String(50), index=True, nullable=False
    )
    ai_summary: Mapped[str | None] = mapped_column(Text)
    root_cause: Mapped[str | None] = mapped_column(Text)
    supporting_evidence: Mapped[list[Any] | None] = mapped_column(JSON)
    confidence_score: Mapped[float | None] = mapped_column(Float)
    recommended_fix: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    raw_ai_response: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    analysis_status: Mapped[str] = mapped_column(
        String(30), default="pending", index=True, nullable=False
    )
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
