from datetime import datetime, timezone
from uuid import uuid4

import pytest

from exreview.application.dto.requests.login_user_request import (
    LoginUserRequest,
)
from exreview.application.services.login_user_service import LoginUserService
from exreview.application.ports.user_repository import UserRepository
from exreview.application.ports.password_hasher import PasswordHasher
from exreview.application.ports.token_provider import TokenProvider
from exreview.domain.entities.user import User
from exreview.domain.exceptions.invalid_credentials import (
    InvalidCredentialsError,
)


class FakeRepository(UserRepository):

    def __init__(self, user):
        self.user = user

    def save(self, user):
        self.user = user
        return user

    def find_by_id(self, user_id):
        return self.user if self.user.id == user_id else None

    def find_by_email(self, email):
        return self.user if self.user.email == email else None


class FakeHasher(PasswordHasher):

    def hash(self, password):
        return f"hashed::{password}"

    def verify(self, password, hashed_password):
        return hashed_password == f"hashed::{password}"


class FakeTokenProvider(TokenProvider):

    def create_access_token(self, subject):
        return f"access::{subject}"

    def create_refresh_token(self, subject):
        return f"refresh::{subject}"

    def get_access_token_subject(self, token: str) -> str | None:
        return None

@pytest.fixture
def service():
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed::Password123!",
        display_name="Test User",
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )

    return LoginUserService(
        user_repository=FakeRepository(user),
        password_hasher=FakeHasher(),
        token_provider=FakeTokenProvider(),
        access_token_expire_seconds=900,
    )


def test_login_successfully(service):
    response = service.login(
        LoginUserRequest(
            email="TEST@example.com",
            password="Password123!",
        )
    )

    assert response.access_token.startswith("access::")
    assert response.refresh_token.startswith("refresh::")
    assert response.token_type == "bearer"
    assert response.expires_in == 900


def test_login_with_wrong_password(service):
    with pytest.raises(InvalidCredentialsError):
        service.login(
            LoginUserRequest(
                email="test@example.com",
                password="WrongPassword123!",
            )
        )


def test_login_with_unknown_email(service):
    with pytest.raises(InvalidCredentialsError):
        service.login(
            LoginUserRequest(
                email="unknown@example.com",
                password="Password123!",
            )
        )

