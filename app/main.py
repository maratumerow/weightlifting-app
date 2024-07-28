from fastapi import FastAPI

from app.api.routes.users import router
from app.config import Settings, settings
from app.data.session import db_connect_init
from app.tools.logging_config import setup_logging
from app.tools.sentry import sentry_init


def get_web_app(config: Settings) -> FastAPI:
    """Create a FastAPI application."""

    sentry_init()
    db_connect_init()

    app_ = FastAPI(
        title=config.app.api_title,
    )

    app_.include_router(router=router)
    return app_


app: FastAPI = get_web_app(config=settings)
setup_logging()
