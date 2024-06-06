from app.data.repositories.user import UserRepository
from app.exceptions.exc_404 import ObjectsNotFoundException
from app.schemas.user import User, UserUpdate


def update_user_service(
    user_id: int, user_update_data: UserUpdate, user_repo: UserRepository
) -> User | None:
    """Update a user by ID."""

    user_update_data = user_update_data.model_validate(user_update_data)

    db_user = user_repo.get_user_by_id(user_id=user_id)
    if not db_user:
        raise ObjectsNotFoundException("User not found")

    user = user_repo.update_user(
        db_user=db_user, user_update_data=user_update_data
    )

    return user
