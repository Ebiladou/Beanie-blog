from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models import User
import oauth, utils
from typing import Annotated

router = APIRouter(tags=['Authentication'])

@router.post('/login')
async def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await User.find_one(User.email == user_credentials.username)
    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth.create_access_token(data={"sub": user.email})
   
    return {"access_token": access_token, "token_type": "bearer"}