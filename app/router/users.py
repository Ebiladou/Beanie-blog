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
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_data = user.model_dump(exclude={"password"})
    new_user = User(**user_data, password=hash_password(user.password))
    await new_user.insert()
    return new_user

@router.get("/", response_model=list[UserResponse])
async def get_users(logged_user = Depends(verify_token)):
    users = await User.find().to_list()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: PydanticObjectId) -> User:
    user = await User.get(id)
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: PydanticObjectId):
    user = await User.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    await user.delete()
    return

@router.put("/{id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_user(id: PydanticObjectId, user: UserUpdate):
    existing_user = await User.get(id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.model_dump(exclude_unset=True)
    await existing_user.update({"$set": update_data})
    updated_user = await User.get(id)
    return updated_user