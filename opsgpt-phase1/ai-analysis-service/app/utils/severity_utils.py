"""Severity ordering and comparison."""

SEVERITY_RANK = {
    "informational": 1,
    "warning": 2,
    "critical": 3,
}


def highest_severity(severities: list[str]) -> str:
    return max(severities, key=lambda value: SEVERITY_RANK[value])


def severities_are_close(first: str, second: str) -> bool:
    return abs(SEVERITY_RANK[first] - SEVERITY_RANK[second]) <= 1
