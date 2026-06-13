"""User management operations."""

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserRole
from app.services.audit_service import create_audit_log


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(
        select(User).where(func.lower(User.email) == email.lower())
    )


def list_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.created_at.asc())))


def create_user(
    db: Session,
    payload: UserCreate,
    *,
    created_by: int | None = None,
) -> User:
    if get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    user = User(
        name=payload.name,
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        role=payload.role.value,
        is_active=payload.is_active,
    )
    db.add(user)
    db.flush()
    create_audit_log(
        db,
        user_id=created_by,
        action="user_created",
        entity_type="user",
        entity_id=str(user.id),
        new_value={
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        },
    )
    db.commit()
    db.refresh(user)
    return user


def update_user_role(
    db: Session,
    user_id: int,
    role: UserRole,
    *,
    changed_by: int,
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    old_role = user.role
    user.role = role.value
    create_audit_log(
        db,
        user_id=changed_by,
        action="user_role_updated",
        entity_type="user",
        entity_id=str(user.id),
        old_value={"role": old_role},
        new_value={"role": user.role},
    )
    db.commit()
    db.refresh(user)
    return user
