from uuid import UUID

from exreview.application.dto.requests.create_experience_request import (
    CreateExperienceRequest,
)
from exreview.application.ports.experience_repository import (
    ExperienceRepository,
)
from exreview.domain.entities.experience import Experience


class CreateExperienceService:

    def __init__(
        self,
        experience_repository: ExperienceRepository,
    ) -> None:
        self.experience_repository = experience_repository

    def create(
        self,
        user_id: UUID,
        request: CreateExperienceRequest,
    ) -> Experience:

        experience = Experience(
            user_id=user_id,
            title=request.title.strip(),
            story=request.story.strip(),
            lesson=request.lesson.strip(),
            category=request.category,
        )

        if request.publish:
            experience.publish()

        return self.experience_repository.save(experience)