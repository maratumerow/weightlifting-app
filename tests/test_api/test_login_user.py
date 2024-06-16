# type: ignore
from unittest.mock import Mock

import pytest

import app.api.routes.users
from app.schemas.auth import TokenInfo


@pytest.fixture
def mock_auth_service(monkeypatch) -> Mock:
    mock_service = Mock()

    mock_cls = Mock(return_value=mock_service)

    monkeypatch.setattr(
        app.api.routes.users,
        "GetAuthenticationTokensService",
        mock_cls,
    )
    return mock_service


class TestLoginUsersAPI:
    """Test cases for logging in a user."""

    LOGIN_URL = "/login"

    @pytest.mark.parametrize(
        "username, password",
        [("a", "1234"), ("a", "1")],
    )
    @pytest.mark.parametrize(
        "access_token, refresh_token",
        [
            ("", ""),
            ("A", "A"),
            ("B", "C"),
        ],
    )
    def test_login_valid(
        self,
        http_client,
        access_token,
        refresh_token,
        username,
        password,
        mock_auth_service,
    ):
        login_result = TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )
        mock_auth_service.return_value = login_result

        result = http_client.post(
            self.LOGIN_URL,
            data={"username": username, "password": password},
        )

        assert result.status_code == 200
        mock_auth_service.assert_called()
        assert TokenInfo(**result.json()) == login_result

    @pytest.mark.parametrize(
        "data",
        [
            {},
            {"username": "a"},
            {"password": "a"},
        ],
    )
    def test_login_invalid(
        self, http_client, mock_auth_service, data
    ):
        mock_auth_service.return_value = None

        result = http_client.post(
            self.LOGIN_URL,
            data=data,
        )
        # res_json = result.json()

        assert result.status_code == 422
        mock_auth_service.assert_not_called()
