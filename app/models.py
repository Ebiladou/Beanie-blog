from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class User(Document):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str
    bio: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"

class UserResponse(BaseModel):
    username: str
    email: EmailStr
    bio: str

class Comment(BaseModel):
    author: str  
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

class BlogPost(Document):
    image_url: Optional[str] = None
    title: str = Field(..., max_length=100)
    content: str
    author: str 
    tags: List[str] = []
    comments: List[Comment] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "posts"