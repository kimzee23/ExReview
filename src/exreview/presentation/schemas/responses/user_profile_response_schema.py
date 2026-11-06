from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserProfileResponseSchema(BaseModel):
    id: UUID
    email: str
    username: str | None
    display_name: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)