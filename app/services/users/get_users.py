from app.data.repositories.user import UserRepository


def get_users_service(
    user_repo: UserRepository, skip: int = 0, limit: int = 100
):
    """Сервис получения списка пользователей"""

    return user_repo.get_users(skip=skip, limit=limit)
