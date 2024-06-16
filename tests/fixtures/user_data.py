from typing import Any, Callable

import pytest
from faker import Faker


@pytest.fixture
def user_data_fabric(faker: Faker):
    def wrap(**kwargs):
        user_data = {
            "id": faker.random_int(),
            "email": faker.email(),
            "username": faker.name(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "image": faker.image_url(),
            "is_active": faker.boolean(),
            "email_subscribe": faker.boolean(),
            "created_at": faker.date_time().isoformat(),
            "updated_at": faker.date_time().isoformat(),
        }
        user_data.update(kwargs)
        return user_data

    return wrap


@pytest.fixture
def user_data(user_data_fabric) -> dict:
    """Return a user data."""

    return user_data_fabric()


@pytest.fixture
def get_fake_users(user_data_fabric) -> Callable:
    """Return a list of user data."""

    def wrap(count=10) -> list[dict[str, Any]]:
        users = []
        for _ in range(count):
            users.append(user_data_fabric())
        return users

    return wrap
