"""Strict JSON extraction for AI provider responses."""

import json
from typing import Any


class InvalidAIResponseError(ValueError):
    pass


def parse_json_object(content: str) -> dict[str, Any]:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise InvalidAIResponseError(
            "AI provider returned invalid JSON"
        ) from exc

    if not isinstance(parsed, dict):
        raise InvalidAIResponseError(
            "AI provider response must be a JSON object"
        )
    return parsed
