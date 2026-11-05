
from abc import ABC, abstractmethod

from exreview.domain.entities.refresh_token import RefreshToken


class RefreshTokenRepository(ABC):

    @abstractmethod
    def save(self, refresh_token: RefreshToken) -> None:
        pass

    @abstractmethod
    def find_by_hash(self, token_hash: str) -> RefreshToken | None:
        pass

    @abstractmethod
    def rotate(
        self,
        old_token_hash: str,
        new_refresh_token: RefreshToken
    ) -> bool:
        pass

    @abstractmethod
    def revoke(self, token_hash: str) -> bool:
        pass
