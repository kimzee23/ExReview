
from abc import ABC, abstractmethod


class TokenProvider(ABC):

    @abstractmethod
    def create_access_token(self, subject: str) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, subject: str) -> str:
        pass

    @abstractmethod
    def get_access_token_subject(self, token: str) -> str | None:
        pass

    @abstractmethod
    def get_refresh_token_subject(self, token: str) -> str | None:
        pass
