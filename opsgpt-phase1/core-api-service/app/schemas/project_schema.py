"""Project, membership, and monitoring source schemas."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class MonitoringSourceType(StrEnum):
    grafana = "grafana"
    azure_monitor = "azure_monitor"
    custom = "custom"


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    description: str | None = None
    environment: str = Field(default="production", min_length=1, max_length=50)
    owner_team: str | None = Field(default=None, max_length=160)
    is_active: bool = True


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = None
    environment: str | None = Field(
        default=None, min_length=1, max_length=50
    )
    owner_team: str | None = Field(default=None, max_length=160)
    is_active: bool | None = None


class ProjectResponse(BaseModel):
    project_id: str
    name: str
    description: str | None
    environment: str
    owner_team: str | None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectMembershipCreate(BaseModel):
    user_id: int
    role_in_project: str | None = Field(default=None, max_length=80)


class ProjectMembershipResponse(BaseModel):
    project_id: str
    user_id: int
    role_in_project: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MonitoringSourceCreate(BaseModel):
    source_type: MonitoringSourceType
    source_name: str = Field(min_length=2, max_length=160)
    dashboard_url: str | None = Field(default=None, max_length=2000)
    alert_rule_url: str | None = Field(default=None, max_length=2000)
    is_active: bool = True


class MonitoringSourceUpdate(BaseModel):
    source_type: MonitoringSourceType | None = None
    source_name: str | None = Field(
        default=None, min_length=2, max_length=160
    )
    dashboard_url: str | None = Field(default=None, max_length=2000)
    alert_rule_url: str | None = Field(default=None, max_length=2000)
    is_active: bool | None = None


class MonitoringSourceResponse(BaseModel):
    source_id: str
    project_id: str
    source_type: MonitoringSourceType
    source_name: str
    dashboard_url: str | None
    alert_rule_url: str | None
    webhook_token: str
    webhook_path: str
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MonitoringSourceValidationResponse(BaseModel):
    valid: bool
    project_id: str
    source_type: MonitoringSourceType
    source_id: str
