"""Audit log endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.rbac import ADMIN, require_roles
from app.db.database import get_db
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.audit_schema import AuditLogResponse
from app.services.audit_service import list_audit_logs

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])
AdminUser = Annotated[User, Depends(require_roles(ADMIN))]


@router.get("", response_model=list[AuditLogResponse])
def get_audit_logs(
    _: AdminUser,
    db: Annotated[Session, Depends(get_db)],
    action: str | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[AuditLog]:
    return list_audit_logs(
        db,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        limit=limit,
        offset=offset,
    )
