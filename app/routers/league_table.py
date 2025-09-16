from fastapi import APIRouter, HTTPException, Request
from app.models import LeagueTable
from typing import List

router = APIRouter()

@router.post("/league_table/", response_model=LeagueTable)
async def create_league_table(entry: LeagueTable, request: Request):
    db = request.app.state.db
    entry_dict = entry.dict(exclude_unset=True)
    result = await db["league_table"].insert_one(entry_dict)
    entry_dict["id"] = str(result.inserted_id)
    return LeagueTable(**entry_dict)

@router.get("/league_table/", response_model=List[LeagueTable])
async def list_league_table(request: Request):
    db = request.app.state.db
    cursor = db["league_table"].find()
    entries = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        entries.append(LeagueTable(**doc))
    return entries

@router.get("/league_table/{entry_id}", response_model=LeagueTable)
async def get_league_table(entry_id: str, request: Request):
    db = request.app.state.db
    doc = await db["league_table"].find_one({"_id": entry_id})
    if not doc:
        raise HTTPException(status_code=404, detail="League table entry not found")
    doc["id"] = str(doc["_id"])
    return LeagueTable(**doc)

@router.put("/league_table/{entry_id}", response_model=LeagueTable)
async def update_league_table(entry_id: str, entry: LeagueTable, request: Request):
    db = request.app.state.db
    entry_dict = entry.dict(exclude_unset=True)
    await db["league_table"].update_one({"_id": entry_id}, {"$set": entry_dict})
    doc = await db["league_table"].find_one({"_id": entry_id})
    if not doc:
        raise HTTPException(status_code=404, detail="League table entry not found")
    doc["id"] = str(doc["_id"])
    return LeagueTable(**doc)

@router.delete("/league_table/{entry_id}")
async def delete_league_table(entry_id: str, request: Request):
    db = request.app.state.db
    result = await db["league_table"].delete_one({"_id": entry_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="League table entry not found")
    return {"message": "League table entry deleted"}
