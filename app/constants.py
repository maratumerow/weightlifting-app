from enum import Enum


class UserGroupType(str, Enum):
    """
    Enum representing user group types such as 'user', 'admin', 'moderator'.
    """

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"
