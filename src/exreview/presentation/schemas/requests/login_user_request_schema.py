from pydantic import BaseModel, EmailStr


class LoginUserRequestSchema(BaseModel):
    email: EmailStr
    password: str