from uuid import UUID

from exreview.application.ports.experience_repository import ExperienceRepository


class DeleteExperienceService:
    def __init__(self, repository: ExperienceRepository) -> None:
        self.repository = repository

    def delete(self, experience_id: UUID, user_id: UUID) -> bool:
        experience = self.repository.find_by_id_and_user(
            experience_id,
            user_id,
        )

        if experience is None:
            return False

        self.repository.delete(experience_id)
        return True