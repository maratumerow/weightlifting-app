# type: ignore
from unittest.mock import Mock

from app.services.users.get_users import UsersGetService


class TestGetUsersService:

    def test_get_users(self, get_fake_users):
        """Test service for getting users."""

        users = get_fake_users(10)

        user_repo = Mock(get_users=Mock(return_value=users))

        result = UsersGetService(user_repo)(skip=0, limit=10)

        assert result == users
        user_repo.get_users.assert_called_once_with(skip=0, limit=10)

    def test_get_users_empty(self):
        """Test service for getting users with empty result."""

        user_repo = Mock(get_users=Mock(return_value=[]))

        result = UsersGetService(user_repo)(skip=0, limit=10)

        assert result == []
        user_repo.get_users.assert_called_once_with(skip=0, limit=10)
