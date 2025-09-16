from fastapi import APIRouter, HTTPException, Request
from app.models import FixtureTeam
from typing import List

router = APIRouter()

@router.post("/fixture_teams/", response_model=FixtureTeam)
async def create_fixture_team(fixture_team: FixtureTeam, request: Request):
    db = request.app.state.db
    ft_dict = fixture_team.dict(exclude_unset=True)
    result = await db["fixture_teams"].insert_one(ft_dict)
    ft_dict["id"] = str(result.inserted_id)
    return FixtureTeam(**ft_dict)

@router.get("/fixture_teams/", response_model=List[FixtureTeam])
async def list_fixture_teams(request: Request):
    db = request.app.state.db
    cursor = db["fixture_teams"].find()
    fixture_teams = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        fixture_teams.append(FixtureTeam(**doc))
    return fixture_teams

@router.get("/fixture_teams/{ft_id}", response_model=FixtureTeam)
async def get_fixture_team(ft_id: str, request: Request):
    db = request.app.state.db
    doc = await db["fixture_teams"].find_one({"_id": ft_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Fixture team not found")
    doc["id"] = str(doc["_id"])
    return FixtureTeam(**doc)

@router.put("/fixture_teams/{ft_id}", response_model=FixtureTeam)
async def update_fixture_team(ft_id: str, fixture_team: FixtureTeam, request: Request):
    db = request.app.state.db
    ft_dict = fixture_team.dict(exclude_unset=True)
    await db["fixture_teams"].update_one({"_id": ft_id}, {"$set": ft_dict})
    doc = await db["fixture_teams"].find_one({"_id": ft_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Fixture team not found")
    doc["id"] = str(doc["_id"])
    return FixtureTeam(**doc)

@router.delete("/fixture_teams/{ft_id}")
async def delete_fixture_team(ft_id: str, request: Request):
    db = request.app.state.db
    result = await db["fixture_teams"].delete_one({"_id": ft_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Fixture team not found")
    return {"message": "Fixture team deleted"}
