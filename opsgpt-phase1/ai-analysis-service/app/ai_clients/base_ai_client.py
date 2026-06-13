"""Base interface for AI provider clients."""

from abc import ABC, abstractmethod
from typing import Any


class AIProviderError(RuntimeError):
    pass


class BaseAIClient(ABC):
    @abstractmethod
    def generate_json(self, prompt: str) -> dict[str, Any]:
        """Generate and parse one JSON object from the selected provider."""
