from unittest.mock import Mock

import pytest
from fastapi.security import OAuth2PasswordRequestForm
from passlib.exc import UnknownHashError

from app.exceptions.exc_404 import ObjectsNotFoundException
from app.services.auth import get_authentication_tokens_service


class TestGetAuthenticationTokensService:

    def test_with_object_not_found(self):
        user_repo = Mock(get_user_by_username=Mock(return_value=None))
        with pytest.raises(
            ObjectsNotFoundException, match="Incorrect username or password"
        ):
            get_authentication_tokens_service(
                OAuth2PasswordRequestForm(username="username", password="password"),
                user_repo,
            )

    def test_with_invalid_password(self):
        fake_user = Mock(password=str(hash("test")))
        user_repo = Mock(get_user_by_username=Mock(return_value=fake_user))
        with pytest.raises(UnknownHashError):
            result = get_authentication_tokens_service(
                OAuth2PasswordRequestForm(username="username", password="password"),
                user_repo,
            )
