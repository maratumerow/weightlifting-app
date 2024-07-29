# type: ignore
from unittest.mock import Mock

import pytest

import app.api.routes.users
from app.exceptions.exc_404 import ObjectsNotFoundException


@pytest.fixture
def mock_delete_user_service(monkeypatch) -> Mock:
    mock_service = Mock()
    mock_cls = Mock(return_value=mock_service)
    monkeypatch.setattr(app.api.routes.users, "UserDeleteService", mock_cls)
    return mock_service


class TestDeleteUserApi:
    """Test cases for deleting a user."""

    def test_delete_user_success(
        self, http_client, mock_delete_user_service, user_data
    ):
        """Test deleting a user."""

        mock_delete_user_service.return_value = None

        result = http_client.delete(f"/users/{user_data['id']}")

        assert result.status_code == 204
        assert mock_delete_user_service.called

    def test_delete_user_not_found(
        self, http_client, mock_delete_user_service, user_data
    ):
        """Test deleting a user that does not exist."""

        mock_delete_user_service.side_effect = ObjectsNotFoundException(
            "User not found"
        )

        result = http_client.delete(f"/users/{user_data['id']}")

        assert result.status_code == 404
        assert result.json() == {"detail": "User not found"}
        assert mock_delete_user_service.called
