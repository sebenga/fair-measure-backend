from fastapi import APIRouter, HTTPException, Request
from app.models import Fixture
from typing import List

router = APIRouter()

@router.post("/fixtures/", response_model=Fixture)
async def create_fixture(fixture: Fixture, request: Request):
    db = request.app.state.db
    fixture_dict = fixture.dict(exclude_unset=True)
    result = await db["fixtures"].insert_one(fixture_dict)
    fixture_dict["id"] = str(result.inserted_id)
    return Fixture(**fixture_dict)

@router.get("/fixtures/", response_model=List[Fixture])
async def list_fixtures(request: Request):
    db = request.app.state.db
    cursor = db["fixtures"].find()
    fixtures = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        fixtures.append(Fixture(**doc))
    return fixtures

@router.get("/fixtures/{fixture_id}", response_model=Fixture)
async def get_fixture(fixture_id: str, request: Request):
    db = request.app.state.db
    doc = await db["fixtures"].find_one({"_id": fixture_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Fixture not found")
    doc["id"] = str(doc["_id"])
    return Fixture(**doc)

@router.put("/fixtures/{fixture_id}", response_model=Fixture)
async def update_fixture(fixture_id: str, fixture: Fixture, request: Request):
    db = request.app.state.db
    fixture_dict = fixture.dict(exclude_unset=True)
    await db["fixtures"].update_one({"_id": fixture_id}, {"$set": fixture_dict})
    doc = await db["fixtures"].find_one({"_id": fixture_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Fixture not found")
    doc["id"] = str(doc["_id"])
    return Fixture(**doc)

@router.delete("/fixtures/{fixture_id}")
async def delete_fixture(fixture_id: str, request: Request):
    db = request.app.state.db
    result = await db["fixtures"].delete_one({"_id": fixture_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Fixture not found")
    return {"message": "Fixture deleted"}
