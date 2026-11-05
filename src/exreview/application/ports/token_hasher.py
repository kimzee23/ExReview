from abc import ABC, abstractmethod


class TokenHasher(ABC):

    @abstractmethod
    def hash(self, token: str) -> str:
        pass