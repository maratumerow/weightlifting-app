from _pytest.fixtures import fixture
from fastapi import FastAPI

from app.api.routes.users import router
from app.config import settings

pytest_plugins = ("tests.fixtures.clients", "tests.fixtures.user_data")


def test_web_app() -> FastAPI:
    app_ = FastAPI(title=settings.app.api_title)
    app_.include_router(router=router)
    return app_


@fixture(scope="session")
def app() -> FastAPI:
    return test_web_app()
