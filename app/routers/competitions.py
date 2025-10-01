from fastapi import APIRouter, HTTPException, Request
from app.models import Competition
from typing import List

router = APIRouter()

# Default free media repositories
DEFAULT_PHOTO_REPOSITORIES = [
    "https://images.pexels.com/photos/274422/pexels-photo-274422.jpeg",  # Soccer ball
    "https://images.pexels.com/photos/1171084/pexels-photo-1171084.jpeg",  # Basketball court
    "https://images.pexels.com/photos/209977/pexels-photo-209977.jpeg",  # Tennis court
    "https://images.pexels.com/photos/1618269/pexels-photo-1618269.jpeg",  # Football field
    "https://images.pexels.com/photos/1884574/pexels-photo-1884574.jpeg",  # Baseball field
    "https://images.pexels.com/photos/1752757/pexels-photo-1752757.jpeg",  # Swimming pool
    "https://images.pexels.com/photos/863988/pexels-photo-863988.jpeg",  # Running track
    "https://images.pexels.com/photos/1263348/pexels-photo-1263348.jpeg"  # Gym equipment
]

DEFAULT_VIDEO_REPOSITORIES = [
    "https://videos.pexels.com/video-files/3195394/3195394-uhd_2560_1440_25fps.mp4",  # Soccer training
    "https://videos.pexels.com/video-files/4753987/4753987-uhd_2560_1440_25fps.mp4",  # Basketball game
    "https://videos.pexels.com/video-files/6253919/6253919-uhd_2560_1440_25fps.mp4",  # Tennis match
    "https://videos.pexels.com/video-files/3195330/3195330-uhd_2560_1440_25fps.mp4",  # Football practice
    "https://videos.pexels.com/video-files/4754007/4754007-uhd_2560_1440_25fps.mp4",  # Baseball game
    "https://videos.pexels.com/video-files/4754146/4754146-uhd_2560_1440_25fps.mp4",  # Swimming
    "https://videos.pexels.com/video-files/4754095/4754095-uhd_2560_1440_25fps.mp4",  # Running
    "https://videos.pexels.com/video-files/4754020/4754020-uhd_2560_1440_25fps.mp4"   # Gym workout
]

@router.post("/competitions/", response_model=Competition)
async def create_competition(competition: Competition, request: Request):
    db = request.app.state.db
    comp_dict = competition.dict(exclude_unset=True)

    if not comp_dict.get("default_photo_repositories"):
        comp_dict["default_photo_repositories"] = DEFAULT_PHOTO_REPOSITORIES
    if not comp_dict.get("default_video_repositories"):
        comp_dict["default_video_repositories"] = DEFAULT_VIDEO_REPOSITORIES

    result = await db["competitions"].insert_one(comp_dict)
    competition_id = str(result.inserted_id)
    comp_dict["id"] = competition_id

    if comp_dict.get("owner_id"):
        await db["competition_members"].insert_one({
            "competition_id": competition_id,
            "user_id": comp_dict["owner_id"],
            "role": "owner"
        })

    return Competition(**comp_dict)

@router.get("/competitions/", response_model=List[Competition])
async def list_competitions(request: Request, owner_id: str = None, member_id: str = None):
    db = request.app.state.db

    if owner_id:
        cursor = db["competitions"].find({"owner_id": owner_id})
    elif member_id:
        member_competitions = []
        async for member in db["competition_members"].find({"user_id": member_id}):
            member_competitions.append(member["competition_id"])
        cursor = db["competitions"].find({"id": {"$in": member_competitions}})
    else:
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
