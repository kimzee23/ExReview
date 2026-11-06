from dataclasses import dataclass

from exreview.domain.enums.experience_category import ExperienceCategory


@dataclass(frozen=True, slots=True)
class CreateExperienceRequest:
    title: str
    story: str
    lesson: str
    category: ExperienceCategory
    publish: bool = False