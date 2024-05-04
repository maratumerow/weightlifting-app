from fastapi import HTTPException

from app.data.repositories.user import UserRepository
from app.schemas.user import User, UserUpdate


def update_user_service(
    user_id: int, user_update_data: UserUpdate, user_repo: UserRepository
) -> User | None:
    """Update a user by ID."""

    db_user = user_repo.get_user_by_id(user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_update_data = user_update_data.model_validate(user_update_data)

    user = user_repo.update_user(
        db_user=db_user, user_update_data=user_update_data
    )

    return user
