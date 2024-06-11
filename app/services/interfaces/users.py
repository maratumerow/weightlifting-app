import abc

from app.data.repositories.interfaces import IUserRepository
from app.schemas.user import UserCreate, User


class IUserCreateService(abc.ABC):

    def __init__(self,  user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self,  user: UserCreate) -> User | None:
        """Create a user"""
