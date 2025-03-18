from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field, EmailStr
from beanie.odm.fields import Indexed
from typing import List, Annotated
from beanie import PydanticObjectId

class User(Document):
    username: Annotated[str, Indexed(unique=True)] = Field(max_length=50)
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
    id: PydanticObjectId
    username: str
    email: EmailStr
    bio: str

class Comment(BaseModel):
    author: str  
    content: str
    replies: List["Comment"] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

class BlogPost(Document):
    image_url: str | None = None
    title: str = Field(..., max_length=100)
    content: str
    author: str | None = None
    tags: List[str] = Field(default_factory=list)  
    comments: List[Comment] = Field(default_factory=list) 
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None

    class Settings:
        name = "posts"

class PostUpdate(BaseModel):
    image_url: str | None = None
    title: str | None = None
    content: str | None = None
    tags: List[str] | None = Field(default_factory=list)  
    updated_at: datetime = Field(default_factory=datetime.now)

class PostResponse(BaseModel):
    id: PydanticObjectId
    title: str
    content: str
    author:str
    created_at: datetime