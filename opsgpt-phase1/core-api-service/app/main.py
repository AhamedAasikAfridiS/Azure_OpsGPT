"""FastAPI application entry point for the OpsGPT Core API Service."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    audit_routes,
    auth_routes,
    dashboard_routes,
    incident_routes,
    internal_routes,
    knowledge_base_routes,
    monitoring_source_routes,
    project_routes,
    user_routes,
)
from app.core.config import get_settings
from app.db.database import Base, SessionLocal, engine
from app.db.seed import seed_users
from app import models  # noqa: F401

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_users(db)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(incident_routes.router)
app.include_router(knowledge_base_routes.router)
app.include_router(audit_routes.router)
app.include_router(internal_routes.router)
app.include_router(project_routes.router)
app.include_router(monitoring_source_routes.router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "healthy", "service": "core-api-service"}
