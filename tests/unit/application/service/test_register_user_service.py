import pytest

from exreview.application.dto.requests.register_user_request import (
    RegisterUserRequest,
)
from exreview.application.ports.password_hasher import PasswordHasher
from exreview.application.ports.user_repository import UserRepository
from exreview.application.services.register_user_service import (
    RegisterUserService,
)
from exreview.domain.entities.user import User
from exreview.domain.exceptions.user_already_exists import (
    UserAlreadyExistsError,
)


class FakeUserRepository(UserRepository):

    def __init__(self):
        self.users: list[User] = []

    def save(self, user: User) -> User:
        self.users.append(user)
        return user

    def find_by_id(self, user_id):
        return next(
            (user for user in self.users if user.id == user_id),
            None,
        )

    def find_by_email(self, email: str):
        return next(
            (user for user in self.users if user.email == email),
            None,
        )

    def find_by_username(self, username: str) -> User | None:
        return next(
            (
                user for user in self.users
                if user.username is not None
                and user.username.lower() == username.lower()
            ),
            None,
        )

    def search_by_username(
        self,
        username: str,
        page: int,
        page_size: int,
    ) -> tuple[list[User], int]:

        matches = [
            user for user in self.users
            if user.is_active
            and user.username is not None
            and username.lower() in user.username.lower()
        ]

        total = len(matches)
        start = (page - 1) * page_size

        return matches[start:start + page_size], total

class FakePasswordHasher(PasswordHasher):

    def hash(self, password: str) -> str:
        return f"hashed::{password}"

    def verify(self, password: str, hashed_password: str) -> bool:
        return hashed_password == f"hashed::{password}"


@pytest.fixture
def repository():
    return FakeUserRepository()


@pytest.fixture
def password_hasher():
    return FakePasswordHasher()


@pytest.fixture
def service(repository, password_hasher):
    return RegisterUserService(repository, password_hasher)


def test_register_user_successfully(service, repository):
    request = RegisterUserRequest(
    email="test@example.com",
    username="testuser",
    password="Password123!",
    display_name="Test User",
)

    response = service.register(request)

    assert response.email == "test@example.com"
    assert response.display_name == "Test User"
    assert response.is_active is True
    assert len(repository.users) == 1
    assert repository.users[0].password_hash == "hashed::Password123!"

    assert not hasattr(response, "password_hash")


def test_register_user_with_existing_email(service, repository):
    request = RegisterUserRequest(
    email="test@example.com",
    username="testuser",
    password="Password123!",
    display_name="Test User",
)

    service.register(request)

    with pytest.raises(UserAlreadyExistsError):
        service.register(request)

    assert len(repository.users) == 1


def test_register_user_with_invalid_password(service, repository):
    request = RegisterUserRequest(
    email="test@example.com",
    username="testuser",
    password="password1",
    display_name="Test User",
)

    with pytest.raises(ValueError):
        service.register(request)

    assert len(repository.users) == 0