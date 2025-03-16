from fastapi import status, HTTPException, APIRouter, UploadFile, Depends
from beanie import PydanticObjectId
from models import BlogPost
from typing import List
import cloudinary.uploader
from oauth import verify_token

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
async def create_blogpost(blog_post: BlogPost, image: UploadFile = None, logged_user = Depends(verify_token)):
    blog_data = blog_post.model_dump()  
    new_blog = BlogPost(**blog_data)  
    if image:
        new_blog.image_url = await cloudinary_upload(image)
    await new_blog.insert()
    return new_blog