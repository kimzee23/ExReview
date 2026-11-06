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
from exreview.application.ports.refresh_token_repository import (
    RefreshTokenRepository,
)
from exreview.application.ports.token_hasher import TokenHasher

from exreview.domain.entities.user import User
from exreview.domain.entities.refresh_token import RefreshToken
from exreview.domain.exceptions.invalid_credentials import (
    InvalidCredentialsError,
)


class FakeRepository(UserRepository):

    def __init__(self, user):
        self.user = user

    def save(self, user: User) -> User:
        self.user = user
        return user

    def find_by_id(self, user_id):
        return self.user if self.user.id == user_id else None

    def find_by_email(self, email):
        return self.user if self.user.email == email else None

    def find_by_username(self, username: str) -> User | None:
        if (
            self.user.username is not None
            and self.user.username.lower() == username.lower()
        ):
            return self.user

        return None

    def search_by_username(
        self,
        username: str,
        page: int,
        page_size: int,
    ) -> tuple[list[User], int]:

        if (
            self.user.is_active
            and self.user.username is not None
            and username.lower() in self.user.username.lower()
        ):
            return [self.user], 1

        return [], 0

class FakeHasher(PasswordHasher):

    def hash(self, password):
        return f"hashed::{password}"

    def verify(self, password, hashed_password):
        return hashed_password == f"hashed::{password}"


class FakeTokenProvider(TokenProvider):

    def create_access_token(self, subject: str) -> str:
        return f"access::{subject}"

    def create_refresh_token(self, subject: str) -> str:
        return f"refresh::{subject}"

    def get_access_token_subject(self, token: str) -> str:
        return token.replace("access::", "")

    def get_refresh_token_subject(self, token: str) -> str:
        return token.replace("refresh::", "")


class FakeTokenHasher(TokenHasher):

    def hash(self, token: str) -> str:
        return f"token-hash::{token}"


class FakeRefreshTokenRepository(RefreshTokenRepository):

    def __init__(self):
        self.saved_tokens = []

    def save(self, refresh_token: RefreshToken) -> None:
        self.saved_tokens.append(refresh_token)

    def find_by_hash(self, token_hash: str):
        return next(
            (
                token
                for token in self.saved_tokens
                if token.token_hash == token_hash
            ),
            None,
        )

    def rotate(self, old_token_hash: str, new_refresh_token: RefreshToken):
        return False

    def revoke(self, token_hash: str):
        return False


@pytest.fixture
def service():
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed::Password123!",
        display_name="Test User",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        username="testuser",
    )
    refresh_token_repository = FakeRefreshTokenRepository()

    login_service = LoginUserService(
        user_repository=FakeRepository(user),
        password_hasher=FakeHasher(),
        token_provider=FakeTokenProvider(),
        refresh_token_repository=refresh_token_repository,
        token_hasher=FakeTokenHasher(),
        access_token_expire_seconds=900,
        refresh_token_expire_seconds=604800,
    )

    return login_service, refresh_token_repository, user


def test_login_successfully(service):
    login_service, refresh_repository, user = service

    response = login_service.login(
        LoginUserRequest(
            email="TEST@example.com",
            password="Password123!",
        )
    )

    assert response.access_token == f"access::{user.id}"
    assert response.refresh_token == f"refresh::{user.id}"
    assert response.token_type == "bearer"
    assert response.expires_in == 900

    assert len(refresh_repository.saved_tokens) == 1

    saved_token = refresh_repository.saved_tokens[0]

    assert saved_token.user_id == user.id
    assert saved_token.token_hash == (
        f"token-hash::refresh::{user.id}"
    )
    assert saved_token.expires_at > datetime.now(timezone.utc)


def test_login_with_wrong_password(service):
    login_service, refresh_repository, _ = service

    with pytest.raises(InvalidCredentialsError):
        login_service.login(
            LoginUserRequest(
                email="test@example.com",
                password="WrongPassword123!",
            )
        )

    assert len(refresh_repository.saved_tokens) == 0


def test_login_with_unknown_email(service):
    login_service, refresh_repository, _ = service

    with pytest.raises(InvalidCredentialsError):
        login_service.login(
            LoginUserRequest(
                email="unknown@example.com",
                password="Password123!",
            )
        )

    assert len(refresh_repository.saved_tokens) == 0