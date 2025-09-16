from fastapi import APIRouter, HTTPException, Request
from app.models import Rule
from typing import List

router = APIRouter()

@router.post("/rules/", response_model=Rule)
async def create_rule(rule: Rule, request: Request):
    db = request.app.state.db
    rule_dict = rule.dict(exclude_unset=True)
    result = await db["rules"].insert_one(rule_dict)
    rule_dict["id"] = str(result.inserted_id)
    return Rule(**rule_dict)

@router.get("/rules/", response_model=List[Rule])
async def list_rules(request: Request):
    db = request.app.state.db
    cursor = db["rules"].find()
    rules = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        rules.append(Rule(**doc))
    return rules

@router.get("/rules/{rule_id}", response_model=Rule)
async def get_rule(rule_id: str, request: Request):
    db = request.app.state.db
    doc = await db["rules"].find_one({"_id": rule_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Rule not found")
    doc["id"] = str(doc["_id"])
    return Rule(**doc)

@router.put("/rules/{rule_id}", response_model=Rule)
async def update_rule(rule_id: str, rule: Rule, request: Request):
    db = request.app.state.db
    rule_dict = rule.dict(exclude_unset=True)
    await db["rules"].update_one({"_id": rule_id}, {"$set": rule_dict})
    doc = await db["rules"].find_one({"_id": rule_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Rule not found")
    doc["id"] = str(doc["_id"])
    return Rule(**doc)

@router.delete("/rules/{rule_id}")
async def delete_rule(rule_id: str, request: Request):
    db = request.app.state.db
    result = await db["rules"].delete_one({"_id": rule_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"message": "Rule deleted"}
