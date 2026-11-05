from pydantic import BaseModel, ConfigDict

class LoginUserResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int