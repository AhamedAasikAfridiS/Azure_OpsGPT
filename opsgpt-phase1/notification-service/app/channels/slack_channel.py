"""Slack Incoming Webhook notification channel."""

import httpx

from app.channels.base_channel import (
    BaseNotificationChannel,
    ChannelDeliveryResult,
)
from app.schemas.slack_schema import SlackWebhookPayload


class SlackChannel(BaseNotificationChannel):
    def __init__(self, webhook_url: str, timeout_seconds: int) -> None:
        self.webhook_url = webhook_url
        self.timeout_seconds = timeout_seconds

    def send(self, message: str) -> ChannelDeliveryResult:
        try:
            response = httpx.post(
                self.webhook_url,
                json=SlackWebhookPayload(text=message).model_dump(),
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            return ChannelDeliveryResult(
                succeeded=False,
                error_message=f"Slack delivery failed: {exc}",
            )
        return ChannelDeliveryResult(succeeded=True)
