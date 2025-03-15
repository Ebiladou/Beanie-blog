from fastapi import status, HTTPException, APIRouter, UploadFile
from beanie import PydanticObjectId
from models import BlogPost
from typing import List
import cloudinary.uploader

router = APIRouter(
    prefix="/post",
    tags=['Post']
)

async def cloudinary_upload(image: UploadFile) -> str:
    try:
        result = cloudinary.uploader.upload(image.file)
        return result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")
    
@router.post("/", response_model=BlogPost)
async def create_blogpost(blog_post: BlogPost, image: UploadFile = None):
    if image:
        blog_post.image_url = await cloudinary_upload(image)
    await blog_post.insert()  
    return blog_post 
