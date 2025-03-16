from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field, EmailStr
from typing import List

class User(Document):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str
    bio: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    bio: str | None = None

class UserResponse(BaseModel):
    username: str
    email: EmailStr
    bio: str

class Comment(BaseModel):
    author: str  
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

class BlogPost(Document):
    image_url: str | None = None
    title: str = Field(..., max_length=100)
    content: str
    author: str 
    tags: List[str] = []
    comments: List[Comment] = [] 
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None

    class Settings:
        name = "posts"