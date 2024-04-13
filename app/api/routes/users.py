from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.shemas.user import UserCreateApi
from app.api.dependencies import get_db, user_repo_dep
from app.data import crud
from app.data.repositories.user import UserRepository
from app.schemas.user import UserCreate, User
from app.services.users import create_user_service

router = APIRouter(tags=["Users"])


@router.post("/users/", response_model=User, summary="Создание пользователя")
def create_user_router(
        user: UserCreateApi,
        user_repo: UserRepository = Depends(user_repo_dep)
):
    return create_user_service(
        user=UserCreate.parse_obj(user),
        user_repo=user_repo,
    )


@router.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Read all users with optional skipping and limiting"""

    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Read a user by user ID"""

    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
