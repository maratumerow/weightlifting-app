from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import user_repo_dep
from app.api.schemas.user import UserApi, UserCreateApi, UserUpdateApi
from app.data.repositories.user import UserRepository
from app.schemas.user import TokenInfo, User, UserUpdate
from app.services.users import (create_user_service, delete_user_service,
                                get_current_and_active_user, get_user_service,
                                get_users_service, login_service,
                                update_user_service)

router = APIRouter(tags=["Users"])


@router.get(
    "/me/",
    summary="Get details of currently logged in user",
    response_model=User,
)
def get_me(
    user: UserApi = Depends(get_current_and_active_user),
):
    return user


@router.post(
    "/login/",
    response_model=TokenInfo,
    summary="Create access and refresh tokens for user",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(user_repo_dep),
):
    return login_service(form_data=form_data, user_repo=user_repo)


@router.post(
    "/users/",
    response_model=User,
    summary="Create a new user",
)
def create_user_router(
    user: UserCreateApi,
    user_repo: UserRepository = Depends(user_repo_dep),
):
    return create_user_service(user=user, user_repo=user_repo)


@router.get(
    "/users/",
    response_model=list[User],
    summary="Get a list of users with optional skipping and limiting",
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
    summary="Get a user by ID",
)
def get_user_route(
    user_id: int,
    user_repo: UserRepository = Depends(user_repo_dep),
):
    return get_user_service(user_id=user_id, user_repo=user_repo)


@router.put(
    "/users/{user_id}",
    response_model=UserUpdate,
    summary="Update a user (first_name and last_name) by ID",
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
    status_code=204,
    summary="Delete a user by ID",
    responses={
        204: {"description": "No Content"},
    },
    response_class=Response,
)
def delete_user_router(
    user_id: int,
    user_repo: UserRepository = Depends(user_repo_dep),
):
    delete_user_service(user_id=user_id, user_repo=user_repo)
    return Response(status_code=204)
