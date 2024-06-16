from app.data.models.user import User
from app.exceptions.exc_404 import ObjectsNotFoundException
from app.services.interfaces.users import IUserGetService


class UserGetService(IUserGetService):
    """Service for getting a user by ID."""

    def __call__(self, user_id: int) -> User | None:
        """Get a user by ID."""

        db_user = self.user_repo.get_user_by_id(user_id=user_id)
        if not db_user:
            raise ObjectsNotFoundException("User not found")
        return db_user
