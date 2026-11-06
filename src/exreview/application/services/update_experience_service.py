from uuid import UUID

from exreview.application.ports.experience_repository import ExperienceRepository
from exreview.domain.entities.experience import Experience
from exreview.domain.enums.experience_category import ExperienceCategory


class UpdateExperienceService:
    def __init__(self, repository: ExperienceRepository) -> None:
        self.repository = repository

    def update(
        self,
        experience_id: UUID,
        user_id: UUID,
        title: str,
        story: str,
        lesson: str,
        category: ExperienceCategory,
    ) -> Experience | None:
        experience = self.repository.find_by_id_and_user(
            experience_id,
            user_id,
        )

        if experience is None:
            return None

        experience.update_content(
            title=title.strip(),
            story=story.strip(),
            lesson=lesson.strip(),
            category=category,
        )

        return self.repository.save(experience)