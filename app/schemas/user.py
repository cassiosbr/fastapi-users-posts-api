from pydantic import BaseModel, EmailStr, Field

from app.schemas.post import PostResponse

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserPostResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    posts: list[PostResponse]

    class Config:
        from_attributes = True