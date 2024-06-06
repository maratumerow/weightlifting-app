from unittest.mock import Mock

import pytest

import app.api.routes.users
from app.schemas.auth import TokenInfo


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
        monkeypatch,
        access_token,
        refresh_token,
        username,
        password,
    ):
        login_result = TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )
        auth_mock = Mock(return_value=login_result)
        monkeypatch.setattr(
            app.api.routes.users,
            "get_authentication_tokens_service",
            auth_mock,
        )

        result = http_client.post(
            self.LOGIN_URL,
            data={"username": username, "password": password},
        )
        
        # res_json = result.json()

        assert result.status_code == 200
        auth_mock.assert_called()
        assert TokenInfo(**result.json()) == login_result

    @pytest.mark.parametrize(
        "data",
        [
            {},
            {"username": "a"},
            {"password": "a"},
        ],
    )
    def test_login_invalid(self, http_client, monkeypatch, data):
        auth_mock = Mock()
        monkeypatch.setattr(
            app.api.routes.users,
            "get_authentication_tokens_service",
            auth_mock,
        )

        result = http_client.post(
            self.LOGIN_URL,
            data=data,
        )
        # res_json = result.json()

        assert result.status_code == 422
        auth_mock.assert_not_called()
