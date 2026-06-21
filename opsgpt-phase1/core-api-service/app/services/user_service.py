from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import User


def upsert_entra_user(db: Session, claims: dict[str, Any], role: str) -> User:
    entra_oid = claims["oid"]
    email = claims.get("preferred_username") or claims.get("email")
    if not isinstance(email, str) or not email.strip():
        raise ValueError("Microsoft Entra access token has no preferred username or email")

    email = email.strip().lower()
    name = claims.get("name") if isinstance(claims.get("name"), str) else ""
    name = name.strip() or email

    user = db.query(User).filter(User.entra_oid == entra_oid).first()
    if not user:
        user = db.query(User).filter(func.lower(User.email) == email).first()

    if not user:
        user = User(
            name=name,
            email=email,
            password_hash=None,
            entra_oid=entra_oid,
            auth_provider="entra",
            role=role,
            is_active=True,
        )
        db.add(user)
    else:
        user.name = name
        user.email = email
        user.entra_oid = entra_oid
        user.auth_provider = "entra"
        user.role = role
        user.is_active = True

    db.commit()
    db.refresh(user)
    return user
