from fastapi import APIRouter, Depends

from app.api.dependencies import user_repo_dep
from app.api.schemas.user import UserCreateApi, UserUpdateApi
from app.data.repositories.user import UserRepository
from app.schemas.user import DeleteUserResponse, User
from app.services.users import (
    create_user_service,
    delete_user_service,
    get_user_service,
    get_users_service,
    update_user_service,
)

router = APIRouter(tags=["Users"])


@router.post(
    "/users/",
    response_model=User,
    summary="Создание пользователя",
)
def create_user_router(
    user: UserCreateApi,
    user_repo: UserRepository = Depends(user_repo_dep),
):
    return create_user_service(user=user, user_repo=user_repo)


@router.get(
    "/users/",
    response_model=list[User],
    summary="Получение списка пользователей",
)
def get_users_route(
    skip: int = 0,
    limit: int = 100,
    user_repo: UserRepository = Depends(user_repo_dep),
):
    return get_users_service(skip=skip, limit=limit, user_repo=user_repo)


@router.get(
    "/users/{user_id}",
    response_model=User,
    summary="Получение пользователя",
)
def get_user_route(
    user_id: int,
    user_repo: UserRepository = Depends(user_repo_dep),
):
    return get_user_service(user_id=user_id, user_repo=user_repo)


@router.put(
    "/users/{user_id}",
    response_model=User,
    summary="Обновление данных пользователя",
)
def update_user_router(
    user_id: int,
    user_update_data: UserUpdateApi,
    user_repo: UserRepository = Depends(user_repo_dep),
):
    return update_user_service(
        user_id=user_id, user_update_data=user_update_data, user_repo=user_repo
    )


@router.delete(
    "/users/{user_id}",
    response_model=DeleteUserResponse,
    summary="Удаление пользователя",
)
def delete_user_router(
    user_id: int,
    user_repo: UserRepository = Depends(user_repo_dep),
):
    status = delete_user_service(user_id=user_id, user_repo=user_repo)
    return DeleteUserResponse(detail="User deleted", status=status)
