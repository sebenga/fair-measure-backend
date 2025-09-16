from fastapi import APIRouter, HTTPException, Request
from app.models import PointAccumulation
from typing import List

router = APIRouter()

@router.post("/point_accumulations/", response_model=PointAccumulation)
async def create_point_accumulation(point_accumulation: PointAccumulation, request: Request):
    db = request.app.state.db
    pa_dict = point_accumulation.dict(exclude_unset=True)
    result = await db["point_accumulations"].insert_one(pa_dict)
    pa_dict["id"] = str(result.inserted_id)
    return PointAccumulation(**pa_dict)

@router.get("/point_accumulations/", response_model=List[PointAccumulation])
async def list_point_accumulations(request: Request):
    db = request.app.state.db
    cursor = db["point_accumulations"].find()
    point_accumulations = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        point_accumulations.append(PointAccumulation(**doc))
    return point_accumulations

@router.get("/point_accumulations/{pa_id}", response_model=PointAccumulation)
async def get_point_accumulation(pa_id: str, request: Request):
    db = request.app.state.db
    doc = await db["point_accumulations"].find_one({"_id": pa_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Point accumulation not found")
    doc["id"] = str(doc["_id"])
    return PointAccumulation(**doc)

@router.put("/point_accumulations/{pa_id}", response_model=PointAccumulation)
async def update_point_accumulation(pa_id: str, point_accumulation: PointAccumulation, request: Request):
    db = request.app.state.db
    pa_dict = point_accumulation.dict(exclude_unset=True)
    await db["point_accumulations"].update_one({"_id": pa_id}, {"$set": pa_dict})
    doc = await db["point_accumulations"].find_one({"_id": pa_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Point accumulation not found")
    doc["id"] = str(doc["_id"])
    return PointAccumulation(**doc)

@router.delete("/point_accumulations/{pa_id}")
async def delete_point_accumulation(pa_id: str, request: Request):
    db = request.app.state.db
    result = await db["point_accumulations"].delete_one({"_id": pa_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Point accumulation not found")
    return {"message": "Point accumulation deleted"}
