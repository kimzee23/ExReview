from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from exreview.application.ports.user_repository import UserRepository
from exreview.domain.entities.user import User
from exreview.infrastructure.database.base import Base
from exreview.infrastructure.models.user_model import UserModel
from exreview.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


@pytest.fixture
def repository():
    engine = create_engine("sqlite+pysqlite:///:memory:")

    Base.metadata.create_all(bind=engine)

    test_session = sessionmaker(bind=engine)
    session = test_session()

    repo = SQLAlchemyUserRepository(session)

    yield repo

    session.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_save_user(repository):
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        display_name="Test User",
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )

    saved_user = repository.save(user)

    assert saved_user.id == user.id
    assert saved_user.email == user.email
    assert saved_user.display_name == user.display_name


def test_find_by_email(repository):
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        display_name="Test User",
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )

    repository.save(user)

    found_user = repository.find_by_email("test@example.com")

    assert found_user is not None
    assert found_user.id == user.id


def test_find_by_id(repository):
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        display_name="Test User",
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )

    repository.save(user)

    found_user = repository.find_by_id(user.id)

    assert found_user is not None
    assert found_user.email == user.email


def test_find_nonexistent_user(repository):
    found_user = repository.find_by_email("unknown@example.com")

    assert found_user is None