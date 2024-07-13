# type: ignore
from unittest.mock import Mock

import pytest

import app.api.routes.users
from app.schemas.user import User as UserSchema


@pytest.fixture
def mock_create_user_service(monkeypatch) -> Mock:
    mock_service = Mock()

    mock_cls = Mock(return_value=mock_service)

    monkeypatch.setattr(
        app.api.routes.users,
        "UserCreateService",
        mock_cls,
    )
    return mock_service


class TestCreateUsersAPI:
    """Test cases for creating a user."""

    CREATE_USER_URL = "/users/register"

    def test_create_user_success(
        self, http_client, mock_create_user_service, user_data
    ):
        """Test creating a user."""

        service_response: UserSchema = UserSchema(**user_data)

        mock_create_user_service.return_value = service_response

        result = http_client.post(
            self.CREATE_USER_URL,
            json={
                "email": user_data["email"],
                "username": user_data["username"],
                "password": "password",
            },
        )

        assert result.status_code == 201
        assert result.json() == user_data
        mock_create_user_service.assert_called()

    @pytest.mark.parametrize(
        "request_data",
        [
            {},
            {
                "email": "",
                "username": "username1",
                "password": "password1",
            },
            {
                "email": "test@gmail.com",
                "username": "",
                "password": "password1",
            },
            {
                "email": "test@gmail.com",
                "username": "username1",
                "password": "",
            },
        ],
    )
    def test_create_user_invalid(
        self,
        http_client,
        mock_create_user_service,
        request_data,
    ):
        """Test creating a user with invalid request_data."""

        mock_create_user_service.return_value = None

        result = http_client.post(self.CREATE_USER_URL, json=request_data)

        assert result.status_code == 422
        mock_create_user_service.assert_not_called()
