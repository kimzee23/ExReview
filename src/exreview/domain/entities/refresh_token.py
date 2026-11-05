
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RefreshToken:
    user_id: UUID
    token_hash: str
    expires_at: datetime
    id: UUID | None = None
    revoked_at: datetime | None = None
