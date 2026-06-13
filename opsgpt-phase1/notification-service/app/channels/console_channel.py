"""Console notification channel for local development."""

from app.channels.base_channel import (
    BaseNotificationChannel,
    ChannelDeliveryResult,
)

class ConsoleChannel(BaseNotificationChannel):
    def send(self, message: str) -> ChannelDeliveryResult:
        print(f"OpsGPT notification:\n{message}", flush=True)
        return ChannelDeliveryResult(succeeded=True)
