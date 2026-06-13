"""Audit log response schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    user_id: int | None
    action: str
    entity_type: str
    entity_id: str
    old_value: dict[str, Any] | list[Any] | None
    new_value: dict[str, Any] | list[Any] | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
