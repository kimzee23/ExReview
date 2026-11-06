from pydantic import BaseModel, EmailStr, Field, field_validator

from exreview.domain.validators.username_validator import (
    normalize_username,
    validate_username,
)


class RegisterUserRequestSchema(BaseModel):

    email: EmailStr

    username: str = Field(
        min_length=3,
        max_length=30,
        examples=["userone"],
    )

    password: str = Field(
        description=(
            "Must contain at least 8 characters, uppercase, "
            "lowercase, number and special character."
        )
    )

    display_name: str = Field(
        min_length=1,
        max_length=50,
    )

    @field_validator("username")
    @classmethod
    def validate_username_field(cls, value: str) -> str:
        validate_username(value)
        return normalize_username(value)