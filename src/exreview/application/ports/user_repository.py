from abc import ABC, abstractmethod
from uuid import UUID

from exreview.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        pass


    @abstractmethod
    def find_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    def search_by_username(
            self,
            username: str,
            page: int,
            page_size: int,
    ) -> tuple[list[User], int]:
        pass