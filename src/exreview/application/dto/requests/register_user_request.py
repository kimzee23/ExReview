from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterUserRequest:
    email: str
    username: str
    password: str
    display_name: str
