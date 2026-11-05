from fastapi import Depends
from sqlalchemy.orm import Session

from exreview.application.services.register_user_service import (
    RegisterUserService,
)
from exreview.infrastructure.database.connection import get_db
from exreview.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from exreview.infrastructure.security.argon2_password_hasher import (
    Argon2PasswordHasher,
)


def get_register_user_service(
    session: Session = Depends(get_db),
) -> RegisterUserService:

    user_repository = SQLAlchemyUserRepository(session)
    password_hasher = Argon2PasswordHasher()

    return RegisterUserService(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )