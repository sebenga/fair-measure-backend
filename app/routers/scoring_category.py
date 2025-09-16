from fastapi import APIRouter, HTTPException, Request
from app.models import ScoringCategory
from typing import List

router = APIRouter()

@router.post("/scoring_categories/", response_model=ScoringCategory)
async def create_scoring_category(category: ScoringCategory, request: Request):
    db = request.app.state.db
    category_dict = category.dict(exclude_unset=True)
    result = await db["scoring_categories"].insert_one(category_dict)
    category_dict["id"] = str(result.inserted_id)
    return ScoringCategory(**category_dict)

@router.get("/scoring_categories/", response_model=List[ScoringCategory])
async def list_scoring_categories(request: Request):
    db = request.app.state.db
    cursor = db["scoring_categories"].find()
    categories = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        categories.append(ScoringCategory(**doc))
    return categories

@router.get("/scoring_categories/{category_id}", response_model=ScoringCategory)
async def get_scoring_category(category_id: str, request: Request):
    db = request.app.state.db
    doc = await db["scoring_categories"].find_one({"_id": category_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Scoring category not found")
    doc["id"] = str(doc["_id"])
    return ScoringCategory(**doc)

@router.put("/scoring_categories/{category_id}", response_model=ScoringCategory)
async def update_scoring_category(category_id: str, category: ScoringCategory, request: Request):
    db = request.app.state.db
    category_dict = category.dict(exclude_unset=True)
    await db["scoring_categories"].update_one({"_id": category_id}, {"$set": category_dict})
    doc = await db["scoring_categories"].find_one({"_id": category_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Scoring category not found")
    doc["id"] = str(doc["_id"])
    return ScoringCategory(**doc)

@router.delete("/scoring_categories/{category_id}")
async def delete_scoring_category(category_id: str, request: Request):
    db = request.app.state.db
    result = await db["scoring_categories"].delete_one({"_id": category_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Scoring category not found")
    return {"message": "Scoring category deleted"}
