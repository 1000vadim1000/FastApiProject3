from pydantic import BaseModel


class UserScheme(BaseModel):
    id: int
    name: str
    email: str


class PostScheme(BaseModel):
    content: str
    title: str
    user_id: int
    post_id: int
