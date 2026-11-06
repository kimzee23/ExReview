from abc import ABC, abstractmethod
from uuid import UUID

from exreview.domain.entities.experience import Experience


class ExperienceRepository(ABC):

    @abstractmethod
    def save(self, experience: Experience) -> Experience:
        pass

    @abstractmethod
    def find_by_id(self, experience_id: UUID) -> Experience | None:
        pass

    @abstractmethod
    def find_by_id_and_user(
        self,
        experience_id: UUID,
        user_id: UUID,
    ) -> Experience | None:
        pass

    @abstractmethod
    def find_published(
        self,
        page: int,
        page_size: int,
    ) -> tuple[list[Experience], int]:
        pass

    @abstractmethod
    def find_by_user(
        self,
        user_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[Experience], int]:
        pass

    @abstractmethod
    def delete(self, experience_id: UUID) -> None:
        pass

    @abstractmethod
    def find_published_by_user(
            self,
            user_id: UUID,
            page: int,
            page_size: int,
    ) -> tuple[list[Experience], int]:
        pass

    @abstractmethod
    def count_published_by_user(self, user_id: UUID) -> int:
        pass