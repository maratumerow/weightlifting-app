from fastapi import FastAPI

from app.api.routes.users import router
from app.config import AppConfig
from app.data.session import db_connect_init

def get_web_app():
    db_connect_init()
    config = AppConfig()
    app = FastAPI(title=config.api_title)
    app.include_router(router=router)
    return app

app = get_web_app()


