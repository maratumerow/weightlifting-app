import logging

from app.exceptions.exc_403 import ObjectsForbiddenException
from app.exceptions.exc_404 import ObjectsNotFoundException
from app.schemas.user import User as UserSchema
from app.services.interfaces.users import IUserGetByEmailService


class UserGetByEmailService(IUserGetByEmailService):
    """Service for getting a user by email."""

    def __call__(self, user_email: str) -> UserSchema | None:
        user = self.user_repo.get_user_by_email(user_email)

        if user is None:
            logging.error(f"User with EMAIL={user_email} not found")
            raise ObjectsNotFoundException(
                detail="User with this email does not exist"
            )
        if not user.is_active:
            logging.error(f"User with EMAIL={user_email} is not active")
            raise ObjectsForbiddenException(
                detail="User with this email is not active"
            )
        return user
