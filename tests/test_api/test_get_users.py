from unittest.mock import Mock

import pytest

import app.api.routes.users
from app.schemas.user import User


@pytest.fixture
def mock_get_users_service(monkeypatch) -> Mock:
    mock_service = Mock()
    monkeypatch.setattr(
        app.api.routes.users,
        "get_users_service",
        mock_service,
    )
    return mock_service


class TestGetUsersAPI:
    """Test cases for getting all users."""

    def test_get_users_success(
        self,
        http_client,
        mock_get_users_service,
        user_data_list,
    ):
        """Test getting all users."""

        service_response: list[User] = [
            User(**user_data) for user_data in user_data_list
        ]

        mock_get_users_service.return_value = service_response

        result = http_client.get("/users")

        assert result.status_code == 200
        assert len(result.json()) == len(user_data_list)
        assert result.json() == user_data_list
        mock_get_users_service.assert_called()
