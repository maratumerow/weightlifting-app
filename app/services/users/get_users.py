from app.schemas.user import User as UserSchema
from app.services.interfaces.users import IUsersGetService


class UsersGetService(IUsersGetService):
    """Service to get users."""

    def __call__(self, skip: int, limit: int) -> list[UserSchema]:
        """Get a list of users with optional skipping and limiting."""

        return self.user_repo.get_users(skip=skip, limit=limit)
