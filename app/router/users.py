from fastapi import status, HTTPException, APIRouter, Depends
from beanie import PydanticObjectId
from models import User, UserResponse, UserUpdate
from utils import hash_password
from oauth import verify_token

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    existing_email = await User.find_one(User.email == user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_username = await User.find_one(User.username == user.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username is already taken")
    user_data = user.model_dump(exclude={"password"})
    new_user = User(**user_data, password=hash_password(user.password))
    await new_user.insert()
    return new_user

@router.get("/", response_model=list[UserResponse])
async def get_users():
    users = await User.find().to_list()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: PydanticObjectId) -> User:
    user = await User.get(id)
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: PydanticObjectId, logged_user = Depends(verify_token)):
    user = await User.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if user.id != logged_user.id:
        raise HTTPException(status_code=403, detail="cannot perform this action")
    await user.delete()
    return

@router.put("/{id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_user(id: PydanticObjectId, user: UserUpdate, logged_user = Depends(verify_token)):
    existing_user = await User.get(id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    if existing_user.id != logged_user.id:
        raise HTTPException(status_code=403, detail="cannot perform this action")
    update_data = user.model_dump(exclude_unset=True)
    await existing_user.update({"$set": update_data})
    updated_user = await User.get(id)
    return updated_user