from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.models.user import User
from app.data.repositories.interfaces import IUserRepository
from app.schemas.user import User as UserSchema
from app.schemas.user import (UserAuthenticate, UserCreate, UserExists,
                              UserUpdate)
from app.tools.security import hash_password


class UserRepository(IUserRepository):
    """User repository."""

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> UserSchema | None:
        user_db = self.db.query(User).filter(User.id == user_id).first()
        if not user_db:
            return None
        return UserSchema.model_validate(user_db, from_attributes=True)

    def get_user_by_email(self, email: str) -> UserSchema | None:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        return UserSchema.model_validate(user, from_attributes=True)

    def get_user_by_username(self, username: str) -> UserAuthenticate | None:
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return None
        return UserAuthenticate.model_validate(user, from_attributes=True)

    def get_username_and_email_exists(self, username: str, email: str) -> UserExists:
        subq_username = (
            select(User.username).where(User.username == username)
        ).exists()
        subq_email = (select(User.email).where(User.email == email)).exists()

        result = self.db.execute(
            select(subq_username.label("u_name"), subq_email.label("u_email")).limit(1),
        ).first()

        is_username = result.u_name if result else False
        is_email = result.u_email if result else False

        return UserExists(
            is_username=is_username,
            is_email=is_email,
        )

    def get_users(self, skip: int = 0, limit: int = 100) -> list[UserSchema]:
        users_db = self.db.query(User).offset(skip).limit(limit).all()
        return [
            UserSchema.model_validate(user, from_attributes=True) for user in users_db
        ]

    def create_user(self, user: UserCreate) -> UserSchema:
        user = User(
            email=user.email,
            username=user.username,
            password=hash_password(user.password),
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return UserSchema.model_validate(user, from_attributes=True)

    def update_user(
        self, user_id: int, user_update_data: UserUpdate
    ) -> UserSchema | None:

        user_db = self.db.query(User).filter(User.id == user_id).first()
        if not user_db:
            return None
        for field, value in user_update_data.model_dump().items():
            if value is not None:
                setattr(user_db, field, value)

        self.db.commit()
        self.db.refresh(user_db)
        return UserSchema.model_validate(user_db, from_attributes=True)

    def delete_user(self, user_id: int) -> bool:
        user_db = self.db.query(User).filter(User.id == user_id).first()
        if user_db:
            self.db.delete(user_db)
            self.db.commit()
            return True
        return False
