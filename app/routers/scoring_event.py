from fastapi import APIRouter, HTTPException, Request
from app.models import ScoringEvent
from typing import List

router = APIRouter()

@router.post("/scoring_events/", response_model=ScoringEvent)
async def create_scoring_event(event: ScoringEvent, request: Request):
    db = request.app.state.db
    event_dict = event.dict(exclude_unset=True)
    result = await db["scoring_events"].insert_one(event_dict)
    event_dict["id"] = str(result.inserted_id)
    return ScoringEvent(**event_dict)

@router.get("/scoring_events/", response_model=List[ScoringEvent])
async def list_scoring_events(request: Request):
    db = request.app.state.db
    cursor = db["scoring_events"].find()
    events = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        events.append(ScoringEvent(**doc))
    return events

@router.get("/scoring_events/{event_id}", response_model=ScoringEvent)
async def get_scoring_event(event_id: str, request: Request):
    db = request.app.state.db
    doc = await db["scoring_events"].find_one({"_id": event_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Scoring event not found")
    doc["id"] = str(doc["_id"])
    return ScoringEvent(**doc)

@router.put("/scoring_events/{event_id}", response_model=ScoringEvent)
async def update_scoring_event(event_id: str, event: ScoringEvent, request: Request):
    db = request.app.state.db
    event_dict = event.dict(exclude_unset=True)
    await db["scoring_events"].update_one({"_id": event_id}, {"$set": event_dict})
    doc = await db["scoring_events"].find_one({"_id": event_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Scoring event not found")
    doc["id"] = str(doc["_id"])
    return ScoringEvent(**doc)

@router.delete("/scoring_events/{event_id}")
async def delete_scoring_event(event_id: str, request: Request):
    db = request.app.state.db
    result = await db["scoring_events"].delete_one({"_id": event_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Scoring event not found")
    return {"message": "Scoring event deleted"}
