from sqlalchemy import JSON, Column, DateTime, Integer, String, Text, func

from app.db.database import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String(80), index=True, nullable=False)
    project_id = Column(String(80), nullable=True, index=True)
    correlation_id = Column(String(120), index=True, nullable=False)
    ai_summary = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    supporting_evidence = Column(JSON, nullable=True)
    confidence_score = Column(Integer, nullable=True)
    recommended_fix = Column(JSON, nullable=True)
    raw_ai_response = Column(JSON, nullable=True)
    analysis_status = Column(String(40), default="pending", nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
