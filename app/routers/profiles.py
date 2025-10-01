from fastapi import APIRouter, HTTPException, Request
from app.models import Profile
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/profiles/", response_model=Profile)
async def create_profile(profile: Profile, request: Request):
    db = request.app.state.db
    profile_dict = profile.dict(exclude_unset=True)

    existing = await db["profiles"].find_one({"user_id": profile_dict["user_id"]})
    if existing:
        existing["id"] = str(existing["_id"])
        return Profile(**existing)

    result = await db["profiles"].insert_one(profile_dict)
    profile_dict["id"] = str(result.inserted_id)
    return Profile(**profile_dict)

@router.get("/profiles/", response_model=List[Profile])
async def list_profiles(request: Request, email: str = None):
    db = request.app.state.db
    query = {}
    if email:
        query["email"] = {"$regex": email, "$options": "i"}

    cursor = db["profiles"].find(query).limit(20)
    profiles = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        profiles.append(Profile(**doc))
    return profiles

@router.get("/profiles/user/{user_id}", response_model=Profile)
async def get_profile_by_user_id(user_id: str, request: Request):
    db = request.app.state.db
    doc = await db["profiles"].find_one({"user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    doc["id"] = str(doc["_id"])
    return Profile(**doc)

@router.get("/profiles/{profile_id}", response_model=Profile)
async def get_profile(profile_id: str, request: Request):
    db = request.app.state.db
    try:
        doc = await db["profiles"].find_one({"_id": ObjectId(profile_id)})
    except:
        doc = await db["profiles"].find_one({"_id": profile_id})

    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    doc["id"] = str(doc["_id"])
    return Profile(**doc)

@router.put("/profiles/{profile_id}", response_model=Profile)
async def update_profile(profile_id: str, profile: Profile, request: Request):
    db = request.app.state.db
    profile_dict = profile.dict(exclude_unset=True, exclude={"id", "created_at"})

    try:
        oid = ObjectId(profile_id)
        await db["profiles"].update_one({"_id": oid}, {"$set": profile_dict})
        doc = await db["profiles"].find_one({"_id": oid})
    except:
        await db["profiles"].update_one({"_id": profile_id}, {"$set": profile_dict})
        doc = await db["profiles"].find_one({"_id": profile_id})

    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    doc["id"] = str(doc["_id"])
    return Profile(**doc)
