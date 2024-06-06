from faker import Faker
import pytest


@pytest.fixture
def user_data(faker: Faker) -> dict:
    """Return a user data."""

    return {
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


@pytest.fixture
def user_data_list(faker: Faker) -> list:
    """Return a list of user data."""

    users = []
    for _ in range(10):
        user = {
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
        users.append(user)
    return users
