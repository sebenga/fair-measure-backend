from fastapi import APIRouter, HTTPException, Request
from app.models import Media
from typing import List

router = APIRouter()

@router.post("/media/", response_model=Media)
async def create_media(media: Media, request: Request):
    db = request.app.state.db
    media_dict = media.dict(exclude_unset=True)
    result = await db["media"].insert_one(media_dict)
    media_dict["id"] = str(result.inserted_id)
    return Media(**media_dict)

@router.get("/media/", response_model=List[Media])
async def list_media(request: Request):
    db = request.app.state.db
    cursor = db["media"].find()
    media_items = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        media_items.append(Media(**doc))
    return media_items

@router.get("/media/{media_id}", response_model=Media)
async def get_media(media_id: str, request: Request):
    db = request.app.state.db
    doc = await db["media"].find_one({"_id": media_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Media not found")
    doc["id"] = str(doc["_id"])
    return Media(**doc)

@router.put("/media/{media_id}", response_model=Media)
async def update_media(media_id: str, media: Media, request: Request):
    db = request.app.state.db
    media_dict = media.dict(exclude_unset=True)
    await db["media"].update_one({"_id": media_id}, {"$set": media_dict})
    doc = await db["media"].find_one({"_id": media_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Media not found")
    doc["id"] = str(doc["_id"])
    return Media(**doc)

@router.delete("/media/{media_id}")
async def delete_media(media_id: str, request: Request):
    db = request.app.state.db
    result = await db["media"].delete_one({"_id": media_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Media not found")
    return {"message": "Media deleted"}
