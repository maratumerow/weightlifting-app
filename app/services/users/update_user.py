from app.exceptions.exc_404 import ObjectsNotFoundException
from app.schemas.user import UserUpdate, User as UserSchema
from app.services.interfaces.users import IUserUpdateService


class UserUpdateService(IUserUpdateService):
    """Service for updating a user."""

    def __call__(
        self, user_id: int, user_update_data: UserUpdate
    ) -> UserSchema | None:
        """Update a user by ID."""

        user = self.user_repo.update_user(
            user_id=user_id, user_update_data=user_update_data
        )
        if not user:
            raise ObjectsNotFoundException("User not found")
        return user
