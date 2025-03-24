from datetime import datetime
from beanie import Document,  before_event, Insert, Link
from pydantic import Field, EmailStr
from beanie.odm.fields import Indexed
from typing import List, Annotated, Optional
from app.utils import hash_password
from beanie import PydanticObjectId

class User(Document):
    username: Annotated[str, Indexed(unique=True)] = Field(max_length=50)
    email: EmailStr
    password: str
    bio: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"

    @before_event(Insert)
    def hash_userpassword(self):
        self.password = hash_password(self.password)

class Comment(Document):
    #id: PydanticObjectId
    author: str | None = None
    content: str
    replies: List[Link["Comment"]]= []
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "comments"

class BlogPost(Document):
    image_url: str | None = None
    title: str = Field(..., max_length=100)
    content: str
    author: str | None = None
    tags: List[str] = Field(default_factory=list)  
    comments: List[Link[Comment]] = []
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "posts"