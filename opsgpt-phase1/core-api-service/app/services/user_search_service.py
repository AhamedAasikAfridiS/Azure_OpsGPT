"""Admin-only active user search."""

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.user import User


def search_active_users(
    db: Session,
    query: str,
    limit: int = 20,
) -> list[User]:
    search_term = f"%{query.strip()}%"
    return list(
        db.scalars(
            select(User)
            .where(
                User.is_active.is_(True),
                or_(
                    User.name.ilike(search_term),
                    User.email.ilike(search_term),
                    User.role.ilike(search_term),
                ),
            )
            .order_by(User.name.asc(), User.email.asc())
            .limit(limit)
        )
    )
