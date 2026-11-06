from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from exreview.domain.enums.experience_category import ExperienceCategory
from exreview.domain.enums.experience_status import ExperienceStatus


@dataclass(slots=True)
class Experience:

    user_id: UUID
    title: str
    story: str
    lesson: str
    category: ExperienceCategory

    id: UUID = None
    status: ExperienceStatus = ExperienceStatus.DRAFT
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = uuid4()

        now = datetime.now(timezone.utc)

        if self.created_at is None:
            self.created_at = now

        if self.updated_at is None:
            self.updated_at = now

        self.validate()

    def validate(self) -> None:
        if not self.title.strip():
            raise ValueError("Experience title is required.")

        if len(self.title.strip()) > 150:
            raise ValueError("Experience title cannot exceed 150 characters.")

        if not self.story.strip():
            raise ValueError("Experience story is required.")

        if len(self.story) > 10000:
            raise ValueError("Experience story cannot exceed 10,000 characters.")

        if not self.lesson.strip():
            raise ValueError("Experience lesson is required.")

        if len(self.lesson) > 3000:
            raise ValueError("Experience lesson cannot exceed 3,000 characters.")

    def publish(self) -> None:
        self.validate()
        self.status = ExperienceStatus.PUBLISHED
        self.updated_at = datetime.now(timezone.utc)

    def update_content(
        self,
        title: str,
        story: str,
        lesson: str,
        category: ExperienceCategory,
    ) -> None:
        self.title = title
        self.story = story
        self.lesson = lesson
        self.category = category
        self.updated_at = datetime.now(timezone.utc)
        self.validate()