"""Grafana webhook payload models."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class GrafanaAlert(BaseModel):
    status: str | None = None
    labels: dict[str, str] = Field(default_factory=dict)
    annotations: dict[str, str] = Field(default_factory=dict)
    starts_at: str | None = Field(default=None, alias="startsAt")
    generator_url: str | None = Field(default=None, alias="generatorURL")
    dashboard_url: str | None = Field(default=None, alias="dashboardURL")
    panel_url: str | None = Field(default=None, alias="panelURL")
    fingerprint: str | None = None
    values: dict[str, Any] | None = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class GrafanaPayload(BaseModel):
    receiver: str | None = None
    status: str | None = None
    alerts: list[GrafanaAlert] = Field(min_length=1)

    model_config = ConfigDict(extra="allow")
