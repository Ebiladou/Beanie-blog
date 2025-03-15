from fastapi import status, HTTPException, APIRouter, Depends
from beanie import PydanticObjectId
from models import User, UserResponse
from typing import List

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(**user.model_dump())
    await new_user.insert()
    return new_user

@router.get("/", response_model=UserResponse)
async def get_users():
    users = await User.find_all().to_list()
    return users

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: PydanticObjectId) -> User:
    user = await User.get(id)
    return user