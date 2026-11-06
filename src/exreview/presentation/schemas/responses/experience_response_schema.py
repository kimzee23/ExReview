from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from exreview.domain.enums.experience_category import ExperienceCategory
from exreview.domain.enums.experience_status import ExperienceStatus


class ExperienceResponseSchema(BaseModel):
    id: UUID
    title: str
    story: str
    lesson: str
    category: ExperienceCategory
    status: ExperienceStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExperienceListResponseSchema(BaseModel):
    items: list[ExperienceResponseSchema]
    total: int
    page: int
    page_size: int
    total_pages: int