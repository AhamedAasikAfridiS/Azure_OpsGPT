"""Alert type inference from source labels and message text."""

ALLOWED_ALERT_TYPES = {
    "cpu",
    "memory",
    "api_latency",
    "database",
    "application_error",
    "custom",
}


def infer_alert_type(
    *,
    explicit_type: str | None = None,
    metric_name: str | None = None,
    message: str | None = None,
) -> str:
    normalized_explicit = (explicit_type or "").strip().lower()
    if normalized_explicit in ALLOWED_ALERT_TYPES:
        return normalized_explicit

    search_text = f"{metric_name or ''} {message or ''}".lower()
    if "cpu" in search_text:
        return "cpu"
    if "memory" in search_text:
        return "memory"
    if "latency" in search_text or "response time" in search_text:
        return "api_latency"
    if any(
        term in search_text
        for term in ("database", " db ", "connection", "postgres", "mysql")
    ):
        return "database"
    if any(
        term in search_text
        for term in ("500", "error", "exception", "failure")
    ):
        return "application_error"
    return "custom"
