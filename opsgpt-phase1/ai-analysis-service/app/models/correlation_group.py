from sqlalchemy import JSON, Column, DateTime, Integer, String, func

from app.db.database import Base


class CorrelationGroup(Base):
    __tablename__ = "correlation_groups"

    id = Column(Integer, primary_key=True, index=True)
    correlation_id = Column(String(120), unique=True, index=True, nullable=False)
    project_id = Column(String(80), nullable=True, index=True)
    service_name = Column(String(120), nullable=False, index=True)
    environment = Column(String(80), nullable=False, index=True)
    severity = Column(String(40), nullable=False, index=True)
    status = Column(String(40), default="open", nullable=False, index=True)
    related_alert_ids = Column(JSON, nullable=False, default=list)
    incident_id = Column(String(80), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
