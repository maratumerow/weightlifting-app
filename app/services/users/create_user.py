from app.schemas.user import UserCreate, User

from app.exceptions.exc_400 import ObjectsAlreadyCreated
from app.services.gateways.email import push_user_email_service


def create_user_service(user: UserCreate, user_repo) -> User:
    """Сервис создания пользователя"""

    db_user = user_repo.get_user_by_email(email=user.email)
    if db_user:
        raise ObjectsAlreadyCreated(
            detail="User already registered"
        )

    user = user_repo.create_user(user=user)

    push_user_email_service(email=user.email)
    return user
