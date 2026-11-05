from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LoginUserRequest:
    email: str
    password: str