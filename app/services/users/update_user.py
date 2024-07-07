from app.exceptions.exc_404 import ObjectsNotFoundException
from app.schemas.user import User as UserSchema
from app.schemas.user import UserUpdate
from app.services.interfaces.users import IUserUpdateService


class UserUpdateService(IUserUpdateService):
    """Service for updating a user."""

    def __call__(
        self, user_id: int, user_update_data: UserUpdate
    ) -> UserSchema | None:
        """Update a user by ID."""

        db_user = self.user_repo.get_user_by_id(user_id=user_id)
        if not db_user:
            raise ObjectsNotFoundException("User not found")

        user = self.user_repo.update_user(
            db_user=db_user, user_update_data=user_update_data
        )

        return user
