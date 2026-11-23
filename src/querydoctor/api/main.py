"""App factory: build a fully wired FastAPI app from settings."""

import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from querydoctor.api.errors import register_error_handlers
from querydoctor.api.middleware import request_context
from querydoctor.api.routes import documents, health
from querydoctor.config import Settings, get_settings
from querydoctor.db.session import make_engine, make_sessionmaker
from querydoctor.logging_setup import setup_logging

logger = logging.getLogger("querydoctor")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    setup_logging(settings.log_level)

    engine = make_engine(settings)
    session_factory = make_sessionmaker(engine)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("startup: engine pool ready")
        yield
        await engine.dispose()
        logger.info("shutdown: engine disposed")

    app = FastAPI(title=settings.app_name, version="0.2.0", lifespan=lifespan)
    app.state.settings = settings
    app.state.engine = engine
    app.state.sessionmaker = session_factory
    app.middleware("http")(request_context)
    register_error_handlers(app)

    v1 = APIRouter(prefix="/v1")
    v1.include_router(documents.router)
    app.include_router(health.router)
    app.include_router(v1)

    return app
