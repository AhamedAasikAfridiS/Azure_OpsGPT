"""Slack Incoming Webhook request schema."""

from pydantic import BaseModel, Field


class SlackWebhookPayload(BaseModel):
    text: str = Field(min_length=1)
