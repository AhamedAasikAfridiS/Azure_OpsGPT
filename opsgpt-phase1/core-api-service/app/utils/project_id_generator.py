"""Public identifier and webhook-token generation."""

import secrets
from datetime import datetime, timezone


def generate_project_id() -> str:
    year = datetime.now(timezone.utc).year
    return f"PROJ-{year}-{secrets.randbelow(1_000_000):06d}"


def generate_source_id() -> str:
    year = datetime.now(timezone.utc).year
    return f"SRC-{year}-{secrets.randbelow(1_000_000):06d}"


def generate_webhook_token() -> str:
    return secrets.token_urlsafe(32)
