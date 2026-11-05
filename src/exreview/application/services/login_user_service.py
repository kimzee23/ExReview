
from datetime import datetime, timedelta, timezone

from exreview.application.dto.requests.login_user_request import (
    LoginUserRequest,
)
from exreview.application.dto.responses.login_user_response import (
    LoginUserResponse,
)
from exreview.application.ports.password_hasher import PasswordHasher
from exreview.application.ports.refresh_token_repository import (
    RefreshTokenRepository,
)
from exreview.application.ports.token_hasher import TokenHasher
from exreview.application.ports.token_provider import TokenProvider
from exreview.application.ports.user_repository import UserRepository
from exreview.domain.entities.refresh_token import RefreshToken
from exreview.domain.exceptions.invalid_credentials import (
    InvalidCredentialsError,
)
from exreview.infrastructure.security.token_hasher import (
    SHA256TokenHasher,
)


class LoginUserService:

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_provider: TokenProvider,
        refresh_token_repository: RefreshTokenRepository,
        token_hasher: TokenHasher,
        access_token_expire_seconds: int,
        refresh_token_expire_seconds: int,
    ) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_provider = token_provider
        self.refresh_token_repository = refresh_token_repository
        self.token_hasher = token_hasher
        self.access_token_expire_seconds = access_token_expire_seconds
        self.refresh_token_expire_seconds = refresh_token_expire_seconds

    def login(self, request: LoginUserRequest) -> LoginUserResponse:
        email = request.email.strip().lower()
        user = self.user_repository.find_by_email(email)

        if (
            user is None
            or not user.is_active
            or not self.password_hasher.verify(
                request.password,
                user.password_hash,
            )
        ):
            raise InvalidCredentialsError()

        subject = str(user.id)
        now = datetime.now(timezone.utc)

        access_token = self.token_provider.create_access_token(subject)
        refresh_token = self.token_provider.create_refresh_token(subject)

        self.refresh_token_repository.save(
            RefreshToken(
                user_id=user.id,
                token_hash=self.token_hasher.hash(refresh_token),
                expires_at=now + timedelta(
                    seconds=self.refresh_token_expire_seconds
                ),
            )
        )

        return LoginUserResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=self.access_token_expire_seconds,
        )
