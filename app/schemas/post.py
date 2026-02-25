from pydantic import BaseModel, Field

class PostCreate(BaseModel):
    title: str = Field(..., max_length=200)
    content: str

class PostResponse(BaseModel):
    title: str
    content: str
    user_id: str

    class Config:
        from_attributes = True