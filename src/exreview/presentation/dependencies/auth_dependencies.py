
from fastapi import Depends
from sqlalchemy.orm import Session

from exreview.application.services.login_user_service import LoginUserService
from exreview.application.services.refresh_token_service import (
    RefreshTokenService,
)
from exreview.application.services.logout_user_service import (
    LogoutUserService,
)
from exreview.infrastructure.config.settings import get_settings
from exreview.infrastructure.database.connection import get_db
from exreview.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from exreview.infrastructure.repositories.sqlalchemy_refresh_token_repository import (
    SQLAlchemyRefreshTokenRepository,
)
from exreview.infrastructure.security.argon2_password_hasher import (
    Argon2PasswordHasher,
)
from exreview.infrastructure.security.jwt_token_provider import (
    PyJWTTokenProvider,
)
from exreview.infrastructure.security.token_hasher import (
    SHA256TokenHasher,
)


def get_token_provider() -> PyJWTTokenProvider:
    return PyJWTTokenProvider(get_settings())


def get_token_hasher() -> SHA256TokenHasher:
    return SHA256TokenHasher()


def get_login_user_service(
    session: Session = Depends(get_db),
) -> LoginUserService:
    settings = get_settings()

    return LoginUserService(
        user_repository=SQLAlchemyUserRepository(session),
        password_hasher=Argon2PasswordHasher(),
        token_provider=PyJWTTokenProvider(settings),
        refresh_token_repository=SQLAlchemyRefreshTokenRepository(session),
        token_hasher=SHA256TokenHasher(),
        access_token_expire_seconds=(
            settings.access_token_expire_minutes * 60
        ),
        refresh_token_expire_seconds=(
            settings.refresh_token_expire_days * 24 * 60 * 60
        ),
    )


def get_refresh_token_service(
    session: Session = Depends(get_db),
) -> RefreshTokenService:
    settings = get_settings()

    return RefreshTokenService(
        refresh_token_repository=SQLAlchemyRefreshTokenRepository(session),
        user_repository=SQLAlchemyUserRepository(session),
        token_provider=PyJWTTokenProvider(settings),
        token_hasher=SHA256TokenHasher(),
        refresh_token_expire_seconds=(
            settings.refresh_token_expire_days * 24 * 60 * 60
        ),
        access_token_expire_seconds=(
            settings.access_token_expire_minutes * 60
        ),
    )


def get_logout_user_service(
    session: Session = Depends(get_db),
) -> LogoutUserService:
    settings = get_settings()

    return LogoutUserService(
        refresh_token_repository=SQLAlchemyRefreshTokenRepository(session),
        token_provider=PyJWTTokenProvider(settings),
        token_hasher=SHA256TokenHasher(),
    )
 