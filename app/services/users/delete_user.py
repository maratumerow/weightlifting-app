from app.data.repositories.user import UserRepository
from app.exceptions.exc_404 import ObjectsNotFoundException


def delete_user_service(user_id: int, user_repo: UserRepository) -> None:
    """Delete a user by ID."""

    db_user = user_repo.get_user_by_id(user_id=user_id)
    if not db_user:
        raise ObjectsNotFoundException(
            detail="User Not Found",
        )

    user_repo.delete_user(user=db_user)
