from app.exceptions.exc_404 import ObjectsNotFoundException
from app.services.interfaces.users import IUserDeleteService


class UserDeleteService(IUserDeleteService):
    """Service for deleting a user."""

    def __call__(self, user_id: int) -> None:
        """Delete a user by ID."""

        db_user = self.user_repo.get_user_by_id(user_id=user_id)
        if not db_user:
            raise ObjectsNotFoundException(
                detail="User Not Found",
            )

        self.user_repo.delete_user(user=db_user)
