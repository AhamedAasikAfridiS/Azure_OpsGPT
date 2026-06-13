"""Development seed users."""

from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserRole
from app.services.user_service import create_user, get_user_by_email

SEED_USERS = (
    UserCreate(
        name="Junior Engineer",
        email="junior.engineer@company.com",
        password="password123",
        role=UserRole.junior_engineer,
    ),
    UserCreate(
        name="Senior Engineer",
        email="senior.engineer@company.com",
        password="password123",
        role=UserRole.senior_engineer,
    ),
    UserCreate(
        name="Admin",
        email="admin@company.com",
        password="password123",
        role=UserRole.admin,
    ),
)


def seed_users(db: Session) -> None:
    for seed_user in SEED_USERS:
        if get_user_by_email(db, seed_user.email) is None:
            create_user(db, seed_user)
