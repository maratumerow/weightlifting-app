# type: ignore
from unittest.mock import Mock

import pytest

import app.api.routes.users
from app.exceptions.exc_404 import ObjectsNotFoundException
from app.schemas.user import User as UserSchema


@pytest.fixture
def mock_update_user_service(monkeypatch) -> Mock:

    mock_service = Mock()

    mock_cls = Mock(return_value=mock_service)

    monkeypatch.setattr(app.api.routes.users, "UserUpdateService", mock_cls)
    return mock_service


class TestUpdateUserApi:
    """Test cases for updating a user."""

    def test_update_user_success(
        self, http_client, mock_update_user_service, user_data
    ):
        """Test updating a user."""

        service_response = UserSchema(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            username=user_data["username"],
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"],
            image=user_data["image"],
            email_subscribe=user_data["email_subscribe"],
            is_active=user_data["is_active"],
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
        response_json = result.json()

        # Convert datetime fields to isoformat for comparison
        service_response_dict = service_response.model_dump()
        service_response_dict["created_at"] = service_response_dict[
            "created_at"
        ].isoformat()
        service_response_dict["updated_at"] = service_response_dict[
            "updated_at"
        ].isoformat()

        assert response_json == service_response_dict
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

        res_json = result.json()
        assert any(
            error["msg"] == expected_error["msg"]
            and error["loc"] == expected_error["loc"]
            for error in res_json["detail"]
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
