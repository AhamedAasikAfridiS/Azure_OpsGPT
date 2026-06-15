"""FastAPI entry point for the OpsGPT Notification Service."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401
from app.api.routes import health_routes, notification_routes
from app.core.config import get_settings
from app.db.database import Base, engine
from app.services.retry_service import create_channel

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_channel(settings)
    Base.metadata.create_all(bind=engine)
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

app.include_router(notification_routes.router)
app.include_router(health_routes.router)
