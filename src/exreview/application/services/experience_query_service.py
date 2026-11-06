from math import ceil
from uuid import UUID

from exreview.application.ports.experience_repository import ExperienceRepository
from exreview.domain.entities.experience import Experience
from exreview.domain.enums.experience_status import ExperienceStatus


class ExperienceQueryService:
    def __init__(self, experience_repository: ExperienceRepository) -> None:
        self.experience_repository = experience_repository

    def get_published(
        self, page: int, page_size: int
    ) -> tuple[list[Experience], int]:
        return self.experience_repository.find_published(page, page_size)

    def get_my_experiences(
        self, user_id: UUID, page: int, page_size: int
    ) -> tuple[list[Experience], int]:
        return self.experience_repository.find_by_user(
            user_id, page, page_size
        )

    def get_published_by_id(self, experience_id: UUID) -> Experience | None:
        experience = self.experience_repository.find_by_id(experience_id)

        if experience is None:
            return None

        if experience.status != ExperienceStatus.PUBLISHED:
            return None

        return experience

    @staticmethod
    def total_pages(total: int, page_size: int) -> int:
        return ceil(total / page_size) if total else 0