
from app.api.schemas.user import UserUpdateApi
from app.data.repositories.user import UserRepository
from app.schemas.user import User
from app.tools.security import get_password_hash


def update_user_service(
    user_id: int, user_update_data: UserUpdateApi, user_repo: UserRepository
) -> User | None:
    """Сервис обновления пользователя"""

    user_update_data = user_update_data.model_validate(user_update_data)
    user_update_data.password = get_password_hash(user_update_data.password)

    user = user_repo.update_user(
        user_id=user_id, user_update_data=user_update_data
    )

    return user
