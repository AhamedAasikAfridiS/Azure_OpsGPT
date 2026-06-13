"""Knowledge base endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.rbac import ADMIN, SENIOR_ENGINEER, require_roles
from app.core.security import CurrentUser
from app.db.database import get_db
from app.models.knowledge_base import KnowledgeBase
from app.models.user import User
from app.schemas.knowledge_base_schema import (
    KnowledgeBaseCreate,
    KnowledgeBaseResponse,
)
from app.services.knowledge_base_service import (
    create_entry,
    get_entry_or_404,
    list_entries,
)

router = APIRouter(prefix="/knowledge-base", tags=["Knowledge Base"])
EditorUser = Annotated[
    User,
    Depends(require_roles(SENIOR_ENGINEER, ADMIN)),
]


@router.get("", response_model=list[KnowledgeBaseResponse])
def get_knowledge_base(
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    service_name: str | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[KnowledgeBase]:
    return list_entries(
        db,
        service_name=service_name,
        limit=limit,
        offset=offset,
    )


@router.get("/{kb_id}", response_model=KnowledgeBaseResponse)
def get_knowledge_base_entry(
    kb_id: int,
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> KnowledgeBase:
    return get_entry_or_404(db, kb_id)


@router.post(
    "",
    response_model=KnowledgeBaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_knowledge_base_entry(
    payload: KnowledgeBaseCreate,
    current_user: EditorUser,
    db: Annotated[Session, Depends(get_db)],
) -> KnowledgeBase:
    return create_entry(db, payload, created_by=current_user.id)
