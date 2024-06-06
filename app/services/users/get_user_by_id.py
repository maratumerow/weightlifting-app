from app.data.models.user import User
from app.data.repositories.user import UserRepository
from app.exceptions.exc_404 import ObjectsNotFoundException


def get_user_service(user_id: int, user_repo: UserRepository) -> User | None:
    """Get a user by ID."""

    db_user = user_repo.get_user_by_id(user_id=user_id)
    if not db_user:
        raise ObjectsNotFoundException("User not found")
    return db_user
