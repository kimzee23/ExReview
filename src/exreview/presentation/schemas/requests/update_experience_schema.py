from pydantic import BaseModel, ConfigDict, Field

from exreview.domain.enums.experience_category import ExperienceCategory


class UpdateExperienceSchema(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    story: str = Field(min_length=1, max_length=10_000)
    lesson: str = Field(min_length=1, max_length=3_000)
    category: ExperienceCategory

    model_config = ConfigDict(str_strip_whitespace=True)