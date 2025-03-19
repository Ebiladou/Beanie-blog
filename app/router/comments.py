from fastapi import status, HTTPException, APIRouter, Depends, Query
from beanie import PydanticObjectId
from models import BlogPost, Comment, UpdateComment
from oauth import verify_token_optional

router = APIRouter(
    prefix="/post",
    tags=['Comments']
)

@router.post("/{post_id}/comment", status_code=status.HTTP_201_CREATED)
async def add_comment(post_id: PydanticObjectId, comment: Comment, logged_user=Depends(verify_token_optional)):
    post = await BlogPost.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if logged_user:
        comment.author = logged_user.username
    elif not comment.author:  
        raise HTTPException(status_code=400, detail="Author name required")
    post.comments.append(comment)
    await post.save()
    return comment

@router.post("/{post_id}/comment/{comment_id}", status_code=status.HTTP_201_CREATED)
async def reply_to_comment(post_id: PydanticObjectId, comment_id: PydanticObjectId, reply: Comment, logged_user=Depends(verify_token_optional)):
    post = await BlogPost.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    def find_comment(comments):
        for comment in comments:
            if comment.id == comment_id:
                return comment
            found = find_comment(comment.replies) 
            if found:
                return found
        return None
    parent_comment = find_comment(post.comments)
    if not parent_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if logged_user:
        reply.author = logged_user.username  
    parent_comment.replies.append(reply)
    await post.save()
    return reply

@router.get("/{post_id}/comments")
async def get_comments(post_id: PydanticObjectId):
    post = await BlogPost.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post.comments

@router.delete("/{post_id}/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(post_id: PydanticObjectId, comment_id: PydanticObjectId, author_name: str = Query(None), logged_user=Depends(verify_token_optional)):
    post = await BlogPost.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    def find_and_remove_comment(comments):
        for i, comment in enumerate(comments):
            if comment.id == comment_id:
                if logged_user and logged_user.username == comment.author:
                    del comments[i]
                    return True
                if logged_user and logged_user.username == post.author:
                    del comments[i]
                    return True
                if not logged_user and author_name and author_name == comment.author:
                    del comments[i]
                    return True
                raise HTTPException(status_code=403, detail="Unauthorized to delete this comment")

            if find_and_remove_comment(comment.replies):
                return True
        return False

    if not find_and_remove_comment(post.comments):
        raise HTTPException(status_code=404, detail="Comment not found")
    await post.save()
    return

@router.patch("/{post_id}/comment/{comment_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_comment(post_id: PydanticObjectId, comment_id: PydanticObjectId, update_data: UpdateComment, author_name: str = Query(None), logged_user=Depends(verify_token_optional),):
    post = await BlogPost.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    def find_comment(comments):
        for comment in comments:
            if comment.id == comment_id:
                return comment
            found = find_comment(comment.replies)
            if found:
                return found
        return None
    comment = find_comment(post.comments)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if logged_user and logged_user.username == comment.author:
        comment.content = update_data.content
    elif not logged_user and author_name and comment.author == author_name:
        comment.content = update_data.content
    else:
        raise HTTPException(status_code=403, detail="Unauthorized to edit this comment")
    await post.save()
    return comment