from abc import ABC, abstractmethod
from typing import Any


class AIProviderError(RuntimeError):
    def __init__(self, message: str, raw_response: dict[str, Any] | str | None = None) -> None:
        super().__init__(message)
        self.raw_response = raw_response


class BaseAIClient(ABC):
    @abstractmethod
    def generate_json(self, prompt: str) -> dict[str, Any]:
        raise NotImplementedError
