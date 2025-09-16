from fastapi import APIRouter, HTTPException, Request
from app.models import Post
from typing import List

router = APIRouter()

@router.post("/posts/", response_model=Post)
async def create_post(post: Post, request: Request):
    db = request.app.state.db
    post_dict = post.dict(exclude_unset=True)
    result = await db["posts"].insert_one(post_dict)
    post_dict["id"] = str(result.inserted_id)
    return Post(**post_dict)

@router.get("/posts/", response_model=List[Post])
async def list_posts(request: Request):
    db = request.app.state.db
    cursor = db["posts"].find()
    posts = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        posts.append(Post(**doc))
    return posts

@router.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: str, request: Request):
    db = request.app.state.db
    doc = await db["posts"].find_one({"_id": post_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Post not found")
    doc["id"] = str(doc["_id"])
    return Post(**doc)

@router.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: str, post: Post, request: Request):
    db = request.app.state.db
    post_dict = post.dict(exclude_unset=True)
    await db["posts"].update_one({"_id": post_id}, {"$set": post_dict})
    doc = await db["posts"].find_one({"_id": post_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Post not found")
    doc["id"] = str(doc["_id"])
    return Post(**doc)

@router.delete("/posts/{post_id}")
async def delete_post(post_id: str, request: Request):
    db = request.app.state.db
    result = await db["posts"].delete_one({"_id": post_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted"}
