from pydantic import BaseModel, ConfigDict


class PublicUserSearchItemSchema(BaseModel):
    username: str
    display_name: str

    model_config = ConfigDict(from_attributes=True)


class PublicUserProfileSchema(BaseModel):
    username: str
    display_name: str
    published_experiences: int


class PublicUserSearchResponseSchema(BaseModel):
    items: list[PublicUserSearchItemSchema]
    total: int
    page: int
    page_size: int
    total_pages: int