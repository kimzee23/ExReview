from pydantic import BaseModel, Field


class LogoutRequestSchema(BaseModel):
    refresh_token: str = Field(min_length=1)