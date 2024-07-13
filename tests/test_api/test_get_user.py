# type: ignore
from unittest.mock import Mock

import pytest

import app.api.routes.users
from app.exceptions.exc_404 import ObjectsNotFoundException
from app.schemas.user import User as UserSchema


@pytest.fixture
def mock_get_user_service(monkeypatch) -> Mock:
    mock_service = Mock()
    mock_cls = Mock(return_value=mock_service)
    monkeypatch.setattr(app.api.routes.users, "UserGetService", mock_cls)
    return mock_service


class TestGetUserAPI:
    """Test cases for getting a user."""

    def test_get_user_success(
        self, http_client, mock_get_user_service, user_data
    ):
        """Test getting a user."""

        service_response: UserSchema = UserSchema(**user_data)
        mock_get_user_service.return_value = service_response

        result = http_client.get(f"/users/{user_data['id']}")

        assert result.status_code == 200
        assert result.json() == user_data

    def test_get_user_not_found(
        self, http_client, mock_get_user_service, user_data
    ):
        """Test user not found."""

        user: UserSchema = UserSchema(**user_data)

        mock_get_user_service.side_effect = ObjectsNotFoundException(
            "User not found"
        )

        result = http_client.get(f"/users/{user.id}")

        assert result.status_code == 404
        assert result.json() == {"detail": "User not found"}
        mock_get_user_service.assert_called()
