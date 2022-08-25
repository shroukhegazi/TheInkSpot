import pytest
from rest_framework.test import APIClient

from theinkspot.category.models import Category
from theinkspot.users.models import User


@pytest.fixture()
def sports_category(db) -> Category:
    return Category.objects.create(name="sports")


@pytest.fixture()
def cs_category(db) -> Category:
    return Category.objects.create(name="computer science")


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(
        name="user name",
        username="username",
        email="test@email.com",
        password="Am0123456789123456",
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def client():
    client = APIClient()
    return client
