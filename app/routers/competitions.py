from fastapi import APIRouter, HTTPException, Request
from app.models import Competition
from typing import List

router = APIRouter()

@router.post("/competitions/", response_model=Competition)
async def create_competition(competition: Competition, request: Request):
    db = request.app.state.db
    comp_dict = competition.dict(exclude_unset=True)
    result = await db["competitions"].insert_one(comp_dict)
    comp_dict["id"] = str(result.inserted_id)
    return Competition(**comp_dict)

@router.get("/competitions/", response_model=List[Competition])
async def list_competitions(request: Request):
    db = request.app.state.db
    cursor = db["competitions"].find()
    competitions = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        competitions.append(Competition(**doc))
    return competitions

@router.get("/competitions/{competition_id}", response_model=Competition)
async def get_competition(competition_id: str, request: Request):
    db = request.app.state.db
    doc = await db["competitions"].find_one({"_id": competition_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Competition not found")
    doc["id"] = str(doc["_id"])
    return Competition(**doc)

@router.put("/competitions/{competition_id}", response_model=Competition)
async def update_competition(competition_id: str, competition: Competition, request: Request):
    db = request.app.state.db
    comp_dict = competition.dict(exclude_unset=True)
    await db["competitions"].update_one({"_id": competition_id}, {"$set": comp_dict})
    doc = await db["competitions"].find_one({"_id": competition_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Competition not found")
    doc["id"] = str(doc["_id"])
    return Competition(**doc)

@router.delete("/competitions/{competition_id}")
async def delete_competition(competition_id: str, request: Request):
    db = request.app.state.db
    result = await db["competitions"].delete_one({"_id": competition_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Competition not found")
    return {"message": "Competition deleted"}
