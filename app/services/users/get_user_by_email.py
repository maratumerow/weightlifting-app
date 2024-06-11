from app.data.repositories.user import UserRepository
from app.exceptions.exc_403 import ObjectsForbiddenException
from app.exceptions.exc_404 import ObjectsNotFoundException
from app.schemas.user import User


def get_user_by_email_service(
    user_repo: UserRepository, user_email: str
) -> User:

    user = user_repo.get_user_by_email(user_email)

    if user is None:
        raise ObjectsNotFoundException(
            detail="User with this email does not exist"
        )
    if not user.is_active:
        raise ObjectsForbiddenException(
            detail="User with this email is not active"
        )
    return user
