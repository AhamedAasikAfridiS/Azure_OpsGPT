"""Service health endpoint."""

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "healthy",
        "service": "ai-analysis-service",
        "ai_provider": settings.ai_provider,
    }
