from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.blog import Blog
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/")
async def get_all_blogs():
    blogs = await Blog.find_all().sort("-created_at").to_list()
    return blogs

@router.post("/")
async def create_blog(blog_data: dict, current_user: User = Depends(get_current_user)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can post blogs")
        
    new_blog = Blog(
        title=blog_data.get("title"),
        category=blog_data.get("category"),
        content=blog_data.get("content"),
        author_id=str(current_user.id),
        author_name=f"Dr. {current_user.first_name} {current_user.last_name}"
    )
    await new_blog.insert()
    return new_blog
