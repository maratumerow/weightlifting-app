from fastapi import HTTPException

from app.data.repositories.user import UserRepository


def delete_user_service(user_id: int, user_repo: UserRepository) -> bool:
    """Сервис удаления пользователя"""

    db_user = user_repo.get_user_by_id(user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    status = user_repo.delete_user(user=db_user)

    return status
