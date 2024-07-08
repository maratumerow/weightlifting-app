from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.api.dependencies.auth import get_token_subject
from app.api.dependencies.db import user_repo_dep
from app.api.schemas.user import UserCreateApi, UserUpdateApi
from app.data.repositories.interfaces import IUserRepository
from app.schemas.auth import TokenInfo
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth.get_authentication_tokens import \
    GetAuthenticationTokensService
from app.services.users import (UserCreateService, UserDeleteService,
                                UserGetByEmailService, UserGetService,
                                UsersGetService, UserUpdateService)

router = APIRouter(tags=["Users"])


@router.get(
    "/me",
    summary="Get details of currently logged in user",
    response_model=UserSchema,
)
def get_me(
    email: EmailStr = Depends(get_token_subject),
    user_repo: IUserRepository = Depends(user_repo_dep),
):
    service = UserGetByEmailService(user_repo=user_repo)
    return service(user_email=email)


@router.post(
    "/login",
    response_model=TokenInfo,
    summary="Create access and refresh tokens for user",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: IUserRepository = Depends(user_repo_dep),
):
    service = GetAuthenticationTokensService(user_repo=user_repo)
    return service(form_data=form_data)


@router.post(
    "/users/register",
    response_model=UserSchema,
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
)
def create_user_router(
    user: UserCreateApi,
    user_repo: IUserRepository = Depends(user_repo_dep),
):
    service = UserCreateService(user_repo=user_repo)
    return service(user=UserCreate.model_validate(user, from_attributes=True))


@router.get(
    "/users",
    response_model=list[UserSchema],
    summary="Get a list of users with optional skipping and limiting",
)
def get_users_route(
    skip: int = 0,
    limit: int = 100,
    user_repo: IUserRepository = Depends(user_repo_dep),
):
    service = UsersGetService(user_repo)
    return service(skip=skip, limit=limit)


@router.get(
    "/users/{user_id}",
    response_model=UserSchema,
    summary="Get a user by ID",
)
def get_user_route(
    user_id: int,
    user_repo: IUserRepository = Depends(user_repo_dep),
):
    service = UserGetService(user_repo)
    return service(user_id=user_id)


@router.put(
    "/users/{user_id}",
    response_model=UserSchema,
    summary="Update a user (first_name and last_name) by ID",
)
def update_user_router(
    user_id: int,
    user_update_data: UserUpdateApi,
    user_repo: IUserRepository = Depends(user_repo_dep),
):
    service = UserUpdateService(user_repo)
    return service(
        user_id=user_id,
        user_update_data=UserUpdate.model_validate(
            user_update_data, from_attributes=True
        ),
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
    user_repo: IUserRepository = Depends(user_repo_dep),
):
    service = UserDeleteService(user_repo=user_repo)
    service(user_id=user_id)
    return Response(status_code=204)
