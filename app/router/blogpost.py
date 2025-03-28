from fastapi import status, HTTPException, APIRouter, UploadFile, Depends, Body
from beanie import PydanticObjectId
from app.models import BlogPost
from app.schemas import PostResponse, PostUpdate
from typing import List
import cloudinary.uploader
from app.oauth import verify_token

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
    
@router.post("/", response_model=BlogPost, status_code=status.HTTP_201_CREATED)
async def create_blogpost(blog_post: BlogPost, logged_user = Depends(verify_token)):
    blog_data = blog_post.model_dump(exclude={"author"})  
    new_blog = BlogPost(**blog_data, author = logged_user.username) 
    await new_blog.insert()
    return new_blog

@router.get("/", response_model=list[PostResponse])
async def get_posts():
    posts = await BlogPost.find().to_list()
    if not posts:
        raise HTTPException(status_code=400, detail="no posts available")
    return posts

@router.get("/{id}", response_model=PostResponse)
async def get_post (id: PydanticObjectId) -> BlogPost:
    post = await BlogPost.get(id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: PydanticObjectId, logged_user = Depends(verify_token)):
    post = await BlogPost.get(id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    if post.author != logged_user.username:
        raise HTTPException(status_code=403, detail="unauthorized to delete post")
    await post.delete()
    return

@router.put("/{id}", response_model=PostResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_post(id:PydanticObjectId, post: PostUpdate, logged_user = Depends(verify_token)):
    userpost = await BlogPost.get(id)
    if not userpost:
        raise HTTPException(status_code=404, detail="post not found")
    if userpost.author != logged_user.username:
        raise HTTPException(status_code=403, detail="unauthorized to update post")
    update_data = {k: v for k, v in post.model_dump(exclude_unset=True).items() if v is not None}
    await BlogPost.find_one(BlogPost.id == id).update({"$set": update_data})
    updated_post = await BlogPost.get(id)
    return updated_post