"""Notification template field formatting."""

from typing import Any


def format_action_list(actions: list[str] | None) -> str:
    if not actions:
        return "Not provided"
    return "\n".join(
        f"{index}. {action}"
        for index, action in enumerate(actions, start=1)
    )


class SafeTemplateValues(dict):
    def __missing__(self, key: str) -> str:
        return "Not provided"


def format_template(
    template_text: str,
    values: dict[str, Any],
) -> str:
    normalized = {
        key: ("Not provided" if value is None or value == "" else value)
        for key, value in values.items()
    }
    return template_text.format_map(SafeTemplateValues(normalized)).strip()
