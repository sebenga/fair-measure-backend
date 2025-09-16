from fastapi import APIRouter, HTTPException, Request
from app.models import Reply
from typing import List

router = APIRouter()

@router.post("/replies/", response_model=Reply)
async def create_reply(reply: Reply, request: Request):
    db = request.app.state.db
    reply_dict = reply.dict(exclude_unset=True)
    result = await db["replies"].insert_one(reply_dict)
    reply_dict["id"] = str(result.inserted_id)
    return Reply(**reply_dict)

@router.get("/replies/", response_model=List[Reply])
async def list_replies(request: Request):
    db = request.app.state.db
    cursor = db["replies"].find()
    replies = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        replies.append(Reply(**doc))
    return replies

@router.get("/replies/{reply_id}", response_model=Reply)
async def get_reply(reply_id: str, request: Request):
    db = request.app.state.db
    doc = await db["replies"].find_one({"_id": reply_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Reply not found")
    doc["id"] = str(doc["_id"])
    return Reply(**doc)

@router.put("/replies/{reply_id}", response_model=Reply)
async def update_reply(reply_id: str, reply: Reply, request: Request):
    db = request.app.state.db
    reply_dict = reply.dict(exclude_unset=True)
    await db["replies"].update_one({"_id": reply_id}, {"$set": reply_dict})
    doc = await db["replies"].find_one({"_id": reply_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Reply not found")
    doc["id"] = str(doc["_id"])
    return Reply(**doc)

@router.delete("/replies/{reply_id}")
async def delete_reply(reply_id: str, request: Request):
    db = request.app.state.db
    result = await db["replies"].delete_one({"_id": reply_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Reply not found")
    return {"message": "Reply deleted"}
