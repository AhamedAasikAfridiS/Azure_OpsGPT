"""Role-based access control and internal API authentication."""

import secrets
from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from app.core.config import get_settings
from app.core.security import get_current_user
from app.models.user import User

JUNIOR_ENGINEER = "junior_engineer"
SENIOR_ENGINEER = "senior_engineer"
ADMIN = "admin"

VALID_ROLES = {JUNIOR_ENGINEER, SENIOR_ENGINEER, ADMIN}
EDITOR_ROLES = {SENIOR_ENGINEER, ADMIN}


def require_roles(*allowed_roles: str) -> Callable:
    def role_checker(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return role_checker


def verify_internal_api_key(
    api_key: Annotated[
        str | None,
        Header(alias="X-Internal-API-Key"),
    ] = None,
) -> None:
    expected_key = get_settings().internal_api_key
    if not api_key or not secrets.compare_digest(api_key, expected_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid internal API key",
        )
