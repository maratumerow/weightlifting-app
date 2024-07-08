from app.exceptions.exc_404 import ObjectsNotFoundException
from app.schemas.user import User as UserSchema
from app.services.interfaces.users import IUserGetService


class UserGetService(IUserGetService):
    """Service for getting a user by ID."""

    def __call__(self, user_id: int) -> UserSchema | None:
        """Get a user by ID."""

        db_user = self.user_repo.get_user_by_id(user_id=user_id)
        if not db_user:
            raise ObjectsNotFoundException("User not found")
        return db_user
