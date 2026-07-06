import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analysis
from app.core.config import settings
from app.db.database import init_db, is_database_ready

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OpsGPT AI Analysis Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)


@app.on_event("startup")
def startup() -> None:
    if not init_db():
        logger.error("AI Analysis started without confirmed database initialization")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "ai-analysis-service",
    }


@app.get("/ready")
def ready() -> dict:
    if not is_database_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is not ready",
        )
    return {"status": "ready", "service": "ai-analysis-service", "checks": {"database": "ok"}}
