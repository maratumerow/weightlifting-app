from app.api.schemas.user import UserCreateApi
from app.data.repositories.user import UserRepository
from app.exceptions.exc_400 import ObjectsAlreadyCreated
from app.schemas.user import User
from app.services.gateways.email import push_user_email_service
from app.tools.security import generate_password_digest


def create_user_service(
    user: UserCreateApi, user_repo: UserRepository
) -> User:
    """Сервис создания пользователя"""

    user = user.model_validate(user)

    db_user_by_email = user_repo.get_user_by_email(email=user.email)
    db_user_by_username = user_repo.get_user_by_username(
        username=user.username
    )

    if db_user_by_email:
        raise ObjectsAlreadyCreated(
            detail="User with this email already registered"
        )
    if db_user_by_username:
        raise ObjectsAlreadyCreated(
            detail="User with this username already registered"
        )

    user.password = generate_password_digest(user.password).hex()

    user = user_repo.create_user(user=user)

    push_user_email_service(email=user.email)
    return user
