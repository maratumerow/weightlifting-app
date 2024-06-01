from _pytest.fixtures import fixture
from fastapi import FastAPI

from app.api.routes.users import router
from app.config import AppConfig

pytest_plugins = ("tests.fixtures.clients",)


def test_web_app():
    app_config = AppConfig()
    app = FastAPI(title=app_config.api_title)
    app.include_router(router=router)
    return app


@fixture(scope="session")
def app():
    return test_web_app()
