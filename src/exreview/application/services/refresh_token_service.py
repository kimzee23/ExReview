from uuid import UUID

from exreview.application.dto.requests.refresh_token_request import (
    RefreshTokenRequest,
)
from exreview.application.dto.responses.login_user_response import (
    LoginUserResponse,
)
from exreview.application.ports.refresh_token_repository import (
    RefreshTokenRepository,
)
from exreview.application.ports.token_provider import TokenProvider
from exreview.application.ports.user_repository import UserRepository
from exreview.domain.entities.refresh_token import RefreshToken
from exreview.domain.exceptions.invalid_refresh_token import (
    InvalidRefreshTokenError,
)
from exreview.infrastructure.security.token_hasher import (
    SHA256TokenHasher,
)

from datetime import datetime, timezone, timedelta

class RefreshTokenService:

    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepository,
        user_repository: UserRepository,
        token_hasher: TokenHasher,
        token_provider: TokenProvider,
        refresh_token_expire_seconds: int,
        access_token_expire_seconds: int,

    ) -> None:
        self.refresh_token_repository = refresh_token_repository
        self.user_repository = user_repository
        self.token_hasher = token_hasher
        self.token_provider = token_provider
        self.refresh_token_expire_seconds = refresh_token_expire_seconds
        self.access_token_expire_seconds = access_token_expire_seconds

    def refresh(self, request: RefreshTokenRequest) -> LoginUserResponse:
        raw_token = request.refresh_token

        subject = self.token_provider.get_refresh_token_subject(raw_token)

        if subject is None:
            raise InvalidRefreshTokenError()

        try:
            user_id = UUID(subject)
        except ValueError as exception:
            raise InvalidRefreshTokenError() from exception

        old_hash = self.token_hasher.hash(raw_token)
        stored_token = self.refresh_token_repository.find_by_hash(old_hash)

        if stored_token is None:
            raise InvalidRefreshTokenError()

        now = datetime.now(timezone.utc)

        expires_at = stored_token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if (
                stored_token.user_id != user_id
                or stored_token.revoked_at is not None
                or expires_at <= now
        ):
            raise InvalidRefreshTokenError()

        user = self.user_repository.find_by_id(user_id)

        if user is None or not user.is_active:
            raise InvalidRefreshTokenError()

        new_access_token = self.token_provider.create_access_token(subject)
        new_refresh_token = self.token_provider.create_refresh_token(subject)

        new_record = RefreshToken(
            user_id=user_id,
            token_hash=self.token_hasher.hash(new_refresh_token),
            expires_at=now + timedelta(
                seconds=self.refresh_token_expire_seconds
            ),
        )

        rotated = self.refresh_token_repository.rotate(
            old_token_hash=old_hash,
            new_refresh_token=new_record,
        )

        if not rotated:
            raise InvalidRefreshTokenError()

        return LoginUserResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=self.access_token_expire_seconds,
        )
