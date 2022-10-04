from typing import Callable

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# from src.app.api.routers import api_router
from src.app.config.settings import settings
from src.app.extensions.db import db
from src.app.graphql.routers import graphql_router
from src.app.log_utils import logging_setup


def init_app() -> FastAPI:
    logging_setup(settings)

    settings_ = {
        "title": f"{settings.PROJECT_NAME} 🚀🚀🚀",
        "debug": settings.DEBUG,
        "docs_url": settings.DOCS_URL,
        "redoc_url": settings.REDOC_URL,
        "openapi_url": settings.OPENAPI_URL,
        "description": f"API docs for {settings.PROJECT_NAME}",
        "version": "0.0.1",
        "contact": {
            "name": "Medniy200 Team",
            "email": "your@gmail.com",
        },
    }
    application = FastAPI(**settings_)  # type: ignore

    register_middleware(application)
    # application.include_router(api_router)
    application.include_router(graphql_router, prefix="/api/v1/graphql")

    application.add_event_handler(
        "startup",
        on_startup_app_handler(application),
    )
    application.add_event_handler("shutdown", on_shutdown_handler(application))

    return application


def on_startup_app_handler(
    application: FastAPI,
) -> Callable:  # type: ignore
    async def start_app() -> None:
        db.init_app(application)

    return start_app


def on_shutdown_handler(application: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        pass

    return stop_app


def register_middleware(application: FastAPI) -> None:
    if settings.CORS_ORIGIN_WHITELIST:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[str(item) for item in settings.CORS_ORIGIN_WHITELIST],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


app = init_app()
