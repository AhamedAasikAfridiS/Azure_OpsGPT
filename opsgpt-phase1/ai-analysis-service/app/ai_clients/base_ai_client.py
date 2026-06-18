from abc import ABC, abstractmethod
from typing import Any


class AIClient(ABC):
    @abstractmethod
    async def analyze_incident(self, alerts: list[dict[str, Any]]) -> dict[str, Any]:
        raise NotImplementedError
