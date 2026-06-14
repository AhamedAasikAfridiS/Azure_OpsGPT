"""User profile and administration endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.rbac import ADMIN, require_roles
from app.core.security import CurrentUser
from app.db.database import get_db
from app.models.user import User
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserRoleUpdate,
    UserSearchResponse,
)
from app.services.user_service import (
    create_user,
    list_users,
    update_user_role,
)
from app.services.user_search_service import search_active_users

router = APIRouter(prefix="/users", tags=["Users"])
AdminUser = Annotated[User, Depends(require_roles(ADMIN))]


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.get("", response_model=list[UserResponse])
def get_users(
    _: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> list[User]:
    return list_users(db)


@router.get("/search", response_model=list[UserSearchResponse])
def search_users(
    _: AdminUser,
    db: Annotated[Session, Depends(get_db)],
    query: Annotated[str, Query(min_length=1, max_length=255)],
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> list[User]:
    return search_active_users(db, query, limit)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    payload: UserCreate,
    current_user: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    return create_user(db, payload, created_by=current_user.id)


@router.patch("/{user_id}/role", response_model=UserResponse)
def change_user_role(
    user_id: int,
    payload: UserRoleUpdate,
    current_user: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    return update_user_role(
        db,
        user_id,
        payload.role,
        changed_by=current_user.id,
    )
