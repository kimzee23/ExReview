from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequestSchema(BaseModel):

    email: EmailStr

    password: str = Field(
        description="Must contain at least 8 characters, uppercase, lowercase, number and special character."
    )

    display_name: str = Field(
        min_length=1,
        max_length=50
    )