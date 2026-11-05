from exreview.application.ports.refresh_token_repository import (
    RefreshTokenRepository,
)
from exreview.application.ports.token_hasher import TokenHasher
from exreview.application.ports.token_provider import TokenProvider
from exreview.domain.exceptions.invalid_refresh_token import (
    InvalidRefreshTokenError,
)


class LogoutUserService:

    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepository,
        token_provider: TokenProvider,
        token_hasher: TokenHasher,
    ) -> None:
        self.refresh_token_repository = refresh_token_repository
        self.token_provider = token_provider
        self.token_hasher = token_hasher

    def logout(self, refresh_token: str) -> None:
        subject = self.token_provider.get_refresh_token_subject(
            refresh_token
        )

        if subject is None:
            raise InvalidRefreshTokenError()

        token_hash = self.token_hasher.hash(refresh_token)

        revoked = self.refresh_token_repository.revoke(token_hash)

        if not revoked:
            raise InvalidRefreshTokenError()