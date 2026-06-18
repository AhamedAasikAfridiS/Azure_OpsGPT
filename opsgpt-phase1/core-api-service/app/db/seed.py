import logging

from app.core.security import hash_password
from app.db.database import SessionLocal
from app.models.models import User

logger = logging.getLogger(__name__)

DEFAULT_USERS = [
    {
        "name": "Junior Engineer",
        "email": "junior.engineer@company.com",
        "password": "password123",
        "role": "junior_engineer",
    },
    {
        "name": "Senior Engineer",
        "email": "senior.engineer@company.com",
        "password": "password123",
        "role": "senior_engineer",
    },
    {"name": "Admin", "email": "admin@company.com", "password": "password123", "role": "admin"},
]


def seed_default_users() -> None:
    db = SessionLocal()
    try:
        for item in DEFAULT_USERS:
            existing = db.query(User).filter(User.email == item["email"]).first()
            if existing:
                continue
            db.add(
                User(
                    name=item["name"],
                    email=item["email"],
                    password_hash=hash_password(item["password"]),
                    role=item["role"],
                    is_active=True,
                )
            )
        db.commit()
        logger.info("Core API default users are present")
    except Exception as exc:
        db.rollback()
        logger.error("Failed to seed default users: %s", exc.__class__.__name__)
    finally:
        db.close()
