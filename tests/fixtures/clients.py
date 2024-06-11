from _pytest.fixtures import fixture
from fastapi import FastAPI
from starlette.testclient import TestClient


@fixture
def http_client(app: FastAPI):
    """Return a TestClient instance for the FastAPI application."""
    yield TestClient(app)
