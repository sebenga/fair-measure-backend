from fastapi import APIRouter, HTTPException, Request
from app.models import Team
from typing import List

router = APIRouter()

@router.post("/teams/", response_model=Team)
async def create_team(team: Team, request: Request):
    db = request.app.state.db
    team_dict = team.dict(exclude_unset=True)
    result = await db["teams"].insert_one(team_dict)
    team_dict["id"] = str(result.inserted_id)
    return Team(**team_dict)

@router.get("/teams/", response_model=List[Team])
async def list_teams(request: Request):
    db = request.app.state.db
    cursor = db["teams"].find()
    teams = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        teams.append(Team(**doc))
    return teams

@router.get("/teams/{team_id}", response_model=Team)
async def get_team(team_id: str, request: Request):
    db = request.app.state.db
    doc = await db["teams"].find_one({"_id": team_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Team not found")
    doc["id"] = str(doc["_id"])
    return Team(**doc)

@router.put("/teams/{team_id}", response_model=Team)
async def update_team(team_id: str, team: Team, request: Request):
    db = request.app.state.db
    team_dict = team.dict(exclude_unset=True)
    await db["teams"].update_one({"_id": team_id}, {"$set": team_dict})
    doc = await db["teams"].find_one({"_id": team_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Team not found")
    doc["id"] = str(doc["_id"])
    return Team(**doc)

@router.delete("/teams/{team_id}")
async def delete_team(team_id: str, request: Request):
    db = request.app.state.db
    result = await db["teams"].delete_one({"_id": team_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Team deleted"}
