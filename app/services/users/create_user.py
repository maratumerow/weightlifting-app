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

    check_user = user_repo.get_username_and_email_exists(
        username=user.username,
        email=user.email,
    )
    error_msgs = []
    if check_user.is_email:
        error_msgs.append("User with this email already registered")
    if check_user.is_username:
        error_msgs.append("User with this username already registered")

    if error_msgs:
        raise ObjectsAlreadyCreated(detail=error_msgs)

    user.password = generate_password_digest(user.password).hex()
    user = user_repo.create_user(user=user)
    push_user_email_service(email=user.email)
    return user
