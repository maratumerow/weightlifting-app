from unittest.mock import Mock

import bcrypt
import pytest
from fastapi.security import OAuth2PasswordRequestForm

from app.exceptions.exc_404 import ObjectsNotFoundException
from app.services.auth import GetAuthenticationTokensService


class TestGetAuthenticationTokensService:

    def test_with_object_not_found(self):
        user_repo = Mock(get_user_by_username=Mock(return_value=None))

        with pytest.raises(
            ObjectsNotFoundException, match="Incorrect username or password"
        ):
            GetAuthenticationTokensService(user_repo=user_repo)(
                form_data=OAuth2PasswordRequestForm(
                    username="username", password="password"
                )
            )

    def test_with_invalid_password(self):
        password = "test".encode()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        fake_user = Mock(
            password=hashed_password.decode(),
            username="username",
        )
        user_repo = Mock(get_user_by_username=Mock(return_value=fake_user))
        with pytest.raises(
            ObjectsNotFoundException, match="Incorrect username or password"
        ):
            GetAuthenticationTokensService(user_repo=user_repo)(
                form_data=OAuth2PasswordRequestForm(
                    username="username", password="password"
                )
            )

    def test_success(self):
        password = "test".encode()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        fake_user = Mock(
            password=hashed_password.decode(),
            username="username",
            email="email",
        )
        user_repo = Mock(get_user_by_username=Mock(return_value=fake_user))
        result = GetAuthenticationTokensService(user_repo=user_repo)(
            form_data=OAuth2PasswordRequestForm(username="username", password="test")
        )
        assert result.access_token
        assert result.refresh_token
