"""Knowledge base request and response schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeBaseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    service_name: str = Field(min_length=1, max_length=120)
    root_cause: str | None = None
    summary: str | None = None
    resolution_steps: list[Any] | dict[str, Any] | None = None
    source_incident_id: str | None = Field(default=None, max_length=50)


class KnowledgeBaseResponse(BaseModel):
    id: int
    title: str
    service_name: str
    root_cause: str | None
    summary: str | None
    resolution_steps: list[Any] | dict[str, Any] | None
    source_incident_id: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
