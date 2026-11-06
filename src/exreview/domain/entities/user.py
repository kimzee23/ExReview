from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class User:
    id: UUID
    email: str
    password_hash: str
    display_name: str
    is_active: bool
    created_at: datetime
    username: str| None = None