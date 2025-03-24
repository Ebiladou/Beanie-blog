from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from beanie.odm.fields import Indexed
from typing import List, Optional
from beanie import PydanticObjectId

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

class UpdateComment(BaseModel):
    content: str | None = None
    author_name: str | None = None 

class PostUpdate(BaseModel):
    image_url: str | None = None
    title: str | None = None
    content: str | None = None
    tags: List[str] | None = Field(default_factory=list)  

class PostResponse(BaseModel):
    id: PydanticObjectId
    title: str
    content: str
    author:str
    created_at: datetime
