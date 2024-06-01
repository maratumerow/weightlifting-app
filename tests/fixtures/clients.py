from _pytest.fixtures import fixture
from fastapi import FastAPI
from starlette.testclient import TestClient


@fixture
def http_client(app: FastAPI):
    return TestClient(app)
