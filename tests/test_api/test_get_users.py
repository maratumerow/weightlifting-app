# type: ignore
from unittest.mock import Mock

import pytest

import app.api.routes.users
from app.schemas.user import User as UserSchema


@pytest.fixture
def mock_get_users_service(monkeypatch) -> Mock:
    mock_service = Mock()

    mock_cls = Mock(return_value=mock_service)

    monkeypatch.setattr(
        app.api.routes.users,
        "UsersGetService",
        mock_cls,
    )
    return mock_service


class TestGetUsersAPI:
    """Test cases for getting all users."""

    def test_get_users_success(
        self,
        http_client,
        mock_get_users_service,
        get_fake_users,
    ):
        """Test getting all users."""

        users = get_fake_users(10)
        service_response: list[UserSchema] = [
            UserSchema(**user_data) for user_data in users
        ]

        mock_get_users_service.return_value = service_response

        result = http_client.get("/users")

        assert result.status_code == 200
        assert len(result.json()) == 10
        assert result.json() == users
        mock_get_users_service.assert_called()
