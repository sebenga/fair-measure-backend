from fastapi import APIRouter, HTTPException, Request
from app.models import CompetitionMember
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/members/", response_model=CompetitionMember)
async def add_member(member: CompetitionMember, request: Request):
    db = request.app.state.db
    member_dict = member.dict(exclude_unset=True)

    existing = await db["competition_members"].find_one({
        "competition_id": member_dict["competition_id"],
        "user_id": member_dict["user_id"]
    })
    if existing:
        raise HTTPException(status_code=400, detail="User is already a member of this competition")

    result = await db["competition_members"].insert_one(member_dict)
    member_dict["id"] = str(result.inserted_id)
    return CompetitionMember(**member_dict)

@router.get("/members/competition/{competition_id}", response_model=List[dict])
async def get_competition_members(competition_id: str, request: Request):
    db = request.app.state.db

    pipeline = [
        {"$match": {"competition_id": competition_id}},
        {
            "$lookup": {
                "from": "profiles",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "user"
            }
        },
        {"$unwind": "$user"}
    ]

    cursor = db["competition_members"].aggregate(pipeline)
    members = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc["user"]["id"] = str(doc["user"]["_id"])
        members.append(doc)
    return members

@router.get("/members/user/{user_id}", response_model=List[CompetitionMember])
async def get_user_memberships(user_id: str, request: Request):
    db = request.app.state.db
    cursor = db["competition_members"].find({"user_id": user_id})
    members = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        members.append(CompetitionMember(**doc))
    return members

@router.delete("/members/{member_id}")
async def remove_member(member_id: str, request: Request):
    db = request.app.state.db
    try:
        oid = ObjectId(member_id)
        result = await db["competition_members"].delete_one({"_id": oid})
    except:
        result = await db["competition_members"].delete_one({"_id": member_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member removed successfully"}

@router.get("/members/check/{competition_id}/{user_id}")
async def check_membership(competition_id: str, user_id: str, request: Request):
    db = request.app.state.db
    member = await db["competition_members"].find_one({
        "competition_id": competition_id,
        "user_id": user_id
    })
    return {
        "is_member": member is not None,
        "role": member.get("role") if member else None
    }
