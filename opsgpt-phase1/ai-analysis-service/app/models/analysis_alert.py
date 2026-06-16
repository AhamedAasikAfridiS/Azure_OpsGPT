from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, func

from app.db.database import Base


class AnalysisAlert(Base):
    __tablename__ = "analysis_alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(120), unique=True, index=True, nullable=False)
    project_id = Column(String(80), nullable=True, index=True)
    source = Column(String(80), nullable=False, index=True)
    source_type = Column(String(80), nullable=True, index=True)
    service_name = Column(String(120), nullable=False, index=True)
    alert_type = Column(String(80), nullable=False, index=True)
    severity = Column(String(40), nullable=False, index=True)
    message = Column(String(1000), nullable=False)
    description = Column(String(2000), nullable=True)
    environment = Column(String(80), default="production", nullable=False, index=True)
    metric_name = Column(String(120), nullable=True)
    metric_value = Column(JSON, nullable=True)
    threshold = Column(String(120), nullable=True)
    resource_id = Column(String(500), nullable=True)
    dashboard_url = Column(String(500), nullable=True)
    runbook_url = Column(String(500), nullable=True)
    labels = Column(JSON, nullable=True)
    annotations = Column(JSON, nullable=True)
    raw_payload_summary = Column(JSON, nullable=True)
    parsing_confidence = Column(Integer, default=50, nullable=False)
    parser_used = Column(String(120), nullable=True)
    fired_at = Column(DateTime(timezone=True), nullable=True)
    received_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_duplicate = Column(Boolean, default=False, nullable=False)
