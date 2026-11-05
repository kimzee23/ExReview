from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from exreview.application.ports.token_provider import TokenProvider
from exreview.domain.entities.user import User
from exreview.domain.exceptions.invalid_access_token import (
    InvalidAccessTokenError,
)
from exreview.infrastructure.database.connection import get_db
from exreview.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from exreview.presentation.dependencies.auth_dependencies import (
    get_token_provider,
)


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: Session = Depends(get_db),
    token_provider: TokenProvider = Depends(get_token_provider),
) -> User:

    if credentials is None:
        raise InvalidAccessTokenError()

    subject = token_provider.get_access_token_subject(
        credentials.credentials
    )

    if subject is None:
        raise InvalidAccessTokenError()

    try:
        user_id = UUID(subject)
    except ValueError as exception:
        raise InvalidAccessTokenError() from exception

    user = SQLAlchemyUserRepository(session).find_by_id(user_id)

    if user is None or not user.is_active:
        raise InvalidAccessTokenError()

    return user