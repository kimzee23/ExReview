from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RegisterUserResponse:
    id: UUID
    email: str
    display_name: str
    is_active: bool
    created_at: datetime