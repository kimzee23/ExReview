from pydantic import BaseModel, ConfigDict, Field, field_validator

from exreview.domain.validators.username_validator import (
    normalize_username,
    validate_username,
)


class UpdateUserProfileRequestSchema(BaseModel):
    username: str | None = Field(default=None)
    display_name: str | None = Field(default=None)

    model_config = ConfigDict(extra="forbid")

    @field_validator("username")
    @classmethod
    def validate_username_field(cls, value):
        if value is None:
            return None

        normalized = normalize_username(value)
        validate_username(normalized)
        return normalized

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, value):
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Display name cannot be empty.")

        if len(value) > 50:
            raise ValueError("Display name cannot exceed 50 characters.")

        return value