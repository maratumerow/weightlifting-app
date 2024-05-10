from app.data.models.user import User
from app.data.repositories.user import UserRepository


def get_user_service(
    user_id: int, user_repo: UserRepository
) -> User | None:
    """Get a user by ID."""

    return user_repo.get_user_by_id(user_id=user_id)
