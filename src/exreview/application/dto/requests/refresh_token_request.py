
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RefreshTokenRequest:
    refresh_token: str
