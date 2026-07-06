import logging
import time
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def is_database_ready() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as exc:
        logger.warning("Core API database readiness check failed: %s", exc.__class__.__name__)
        return False


def init_db() -> bool:
    from app.models import models  # noqa: F401

    for attempt in range(1, settings.db_init_max_attempts + 1):
        try:
            Base.metadata.create_all(bind=engine)
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS entra_oid VARCHAR(255)"))
                connection.execute(
                    text("ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_provider VARCHAR(40) NOT NULL DEFAULT 'local'")
                )
                connection.execute(text("ALTER TABLE users ALTER COLUMN password_hash DROP NOT NULL"))
                connection.execute(
                    text(
                        "CREATE UNIQUE INDEX IF NOT EXISTS ix_users_entra_oid_unique "
                        "ON users (entra_oid) WHERE entra_oid IS NOT NULL"
                    )
                )
            logger.info("Core API database tables are ready")
            return True
        except SQLAlchemyError as exc:
            logger.warning("Core API database not ready, attempt %s: %s", attempt, exc.__class__.__name__)
            time.sleep(settings.db_init_delay_seconds)

    logger.error("Core API database initialization did not complete")
    return False
