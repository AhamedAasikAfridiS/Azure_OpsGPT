"""Source severity normalization."""

AZURE_SEVERITY_MAP = {
    "sev0": "critical",
    "sev1": "critical",
    "sev2": "warning",
    "sev3": "warning",
    "sev4": "informational",
    "critical": "critical",
    "warning": "warning",
    "informational": "informational",
    "info": "informational",
}

STANDARD_SEVERITY_MAP = {
    "critical": "critical",
    "warning": "warning",
    "warn": "warning",
    "informational": "informational",
    "info": "informational",
}


def map_azure_severity(value: str | None) -> str:
    normalized = (value or "").strip().lower()
    return AZURE_SEVERITY_MAP.get(normalized, normalized)


def map_standard_severity(value: str | None) -> str:
    normalized = (value or "").strip().lower()
    return STANDARD_SEVERITY_MAP.get(normalized, normalized)
