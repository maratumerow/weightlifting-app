from unittest.mock import Mock

import pytest

import app.api.routes.users
from app.exceptions.exc_404 import ObjectsNotFoundException
from app.schemas.user import UserUpdate


@pytest.fixture
def mock_update_user_service(monkeypatch) -> Mock:
    mock_service = Mock()
    monkeypatch.setattr(
        app.api.routes.users, "update_user_service", mock_service
    )
    return mock_service


class TestUpdateUserApi:
    """Test cases for updating a user."""

    def test_update_user_success(
        self, http_client, mock_update_user_service, user_data
    ):
        """Test updating a user."""

        service_response: UserUpdate = UserUpdate(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
        )

        mock_update_user_service.return_value = service_response

        result = http_client.put(
            f"/users/{user_data['id']}",
            json={
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
            },
        )

        assert result.status_code == 200
        assert result.json() == {
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
        }
        assert mock_update_user_service.called

    @pytest.mark.parametrize(
        "wrong_data, expected_error",
        [
            (
                {"id": 1, "first_name": "", "last_name": "Doe"},
                {
                    "msg": "String should have at least 2 characters",
                    "loc": ["body", "first_name"],
                },
            ),
            (
                {"id": 2, "first_name": "Jane", "last_name": ""},
                {
                    "msg": "String should have at least 2 characters",
                    "loc": ["body", "last_name"],
                },
            ),
            (
                {"id": 3, "first_name": "John", "last_name": 123},
                {
                    "msg": "Input should be a valid string",
                    "loc": ["body", "last_name"],
                },
            ),
            (
                {"id": 4, "first_name": 123, "last_name": "Doe"},
                {
                    "msg": "Input should be a valid string",
                    "loc": ["body", "first_name"],
                },
            ),
            (
                {"id": 5},
                {
                    "msg": "String should have at least 2 characters",
                    "loc": ["body", "first_name"],
                },
            ),
        ],
    )
    def test_update_user_invalid(
        self, http_client, mock_update_user_service, wrong_data, expected_error
    ):
        """Test updating a user with invalid data."""
        mock_update_user_service.return_value = None

        result = http_client.put(
            f"/users/{wrong_data['id']}",
            json={
                "first_name": wrong_data.get("first_name", ""),
                "last_name": wrong_data.get("last_name", ""),
            },
        )

        assert result.status_code == 422
        assert "detail" in result.json()
        errors = result.json()["detail"]
        assert any(
            error["msg"] == expected_error["msg"]
            and error["loc"] == expected_error["loc"]
            for error in errors
        )
        assert not mock_update_user_service.called

    def test_update_user_not_found(
        self,
        http_client,
        mock_update_user_service,
        user_data,
    ):
        """Test updating a user that does not exist."""

        mock_update_user_service.side_effect = ObjectsNotFoundException(
            "User not found"
        )

        result = http_client.put(
            f"/users/{user_data['id']}",
            json={
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
            },
        )

        assert result.status_code == 404
        assert result.json() == {"detail": "User not found"}
        assert mock_update_user_service.called
