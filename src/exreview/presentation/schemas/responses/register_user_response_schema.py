from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RegisterUserResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    username: str | None
    display_name: str
    is_active: bool
    created_at: datetime