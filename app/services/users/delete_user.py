import logging

from app.exceptions.exc_404 import ObjectsNotFoundException
from app.services.interfaces.users import IUserDeleteService


class UserDeleteService(IUserDeleteService):
    """Service for deleting a user."""

    def __call__(self, user_id: int) -> None:
        """Delete a user by ID."""

        success = self.user_repo.delete_user(user_id=user_id)
        if not success:
            logging.error(f"User with ID={user_id} Not Found")
            raise ObjectsNotFoundException(
                detail="User Not Found",
            )
        logging.info(f"User with ID={user_id} deleted")
        return None
