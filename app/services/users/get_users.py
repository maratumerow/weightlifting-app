from app.data.repositories.user import UserRepository


def get_users_service(
    user_repo: UserRepository, skip: int = 0, limit: int = 100
):
    """Get a list of users with optional skipping and limiting."""

    return user_repo.get_users(skip=skip, limit=limit)
