"""Base notification channel interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ChannelDeliveryResult:
    succeeded: bool
    error_message: str | None = None


class BaseNotificationChannel(ABC):
    @abstractmethod
    def send(self, message: str) -> ChannelDeliveryResult:
        """Deliver one formatted notification message."""
