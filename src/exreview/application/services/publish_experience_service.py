from uuid import UUID

from exreview.application.ports.experience_repository import ExperienceRepository
from exreview.domain.entities.experience import Experience


class PublishExperienceService:
    def __init__(self, repository: ExperienceRepository) -> None:
        self.repository = repository

    def publish(
        self,
        experience_id: UUID,
        user_id: UUID,
    ) -> Experience | None:
        experience = self.repository.find_by_id_and_user(
            experience_id,
            user_id,
        )

        if experience is None:
            return None

        experience.publish()

        return self.repository.save(experience)