from fastapi import APIRouter, Depends, HTTPException
from app.models import Competition, Team, Fixture, LeagueTable, Post, Media
from fastapi import Request
from typing import List

router = APIRouter()

# Fixture CRUD endpoints
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

# LeagueTable CRUD endpoints
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

# Post CRUD endpoints
@router.post("/posts/", response_model=Post)
async def create_post(post: Post, request: Request):
    db = request.app.state.db
    post_dict = post.dict(exclude_unset=True)
    result = await db["posts"].insert_one(post_dict)
    post_dict["id"] = str(result.inserted_id)
    return Post(**post_dict)

@router.get("/posts/", response_model=List[Post])
async def list_posts(request: Request):
    db = request.app.state.db
    cursor = db["posts"].find()
    posts = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        posts.append(Post(**doc))
    return posts

@router.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: str, request: Request):
    db = request.app.state.db
    doc = await db["posts"].find_one({"_id": post_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Post not found")
    doc["id"] = str(doc["_id"])
    return Post(**doc)

@router.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: str, post: Post, request: Request):
    db = request.app.state.db
    post_dict = post.dict(exclude_unset=True)
    await db["posts"].update_one({"_id": post_id}, {"$set": post_dict})
    doc = await db["posts"].find_one({"_id": post_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Post not found")
    doc["id"] = str(doc["_id"])
    return Post(**doc)

@router.delete("/posts/{post_id}")
async def delete_post(post_id: str, request: Request):
    db = request.app.state.db
    result = await db["posts"].delete_one({"_id": post_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted"}

# Media CRUD endpoints
@router.post("/media/", response_model=Media)
async def create_media(media: Media, request: Request):
    db = request.app.state.db
    media_dict = media.dict(exclude_unset=True)
    result = await db["media"].insert_one(media_dict)
    media_dict["id"] = str(result.inserted_id)
    return Media(**media_dict)

@router.get("/media/", response_model=List[Media])
async def list_media(request: Request):
    db = request.app.state.db
    cursor = db["media"].find()
    media_items = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        media_items.append(Media(**doc))
    return media_items

@router.get("/media/{media_id}", response_model=Media)
async def get_media(media_id: str, request: Request):
    db = request.app.state.db
    doc = await db["media"].find_one({"_id": media_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Media not found")
    doc["id"] = str(doc["_id"])
    return Media(**doc)

@router.put("/media/{media_id}", response_model=Media)
async def update_media(media_id: str, media: Media, request: Request):
    db = request.app.state.db
    media_dict = media.dict(exclude_unset=True)
    await db["media"].update_one({"_id": media_id}, {"$set": media_dict})
    doc = await db["media"].find_one({"_id": media_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Media not found")
    doc["id"] = str(doc["_id"])
    return Media(**doc)

@router.delete("/media/{media_id}")
async def delete_media(media_id: str, request: Request):
    db = request.app.state.db
    result = await db["media"].delete_one({"_id": media_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Media not found")
    return {"message": "Media deleted"}

from fastapi import APIRouter, Depends, HTTPException
from app.models import Competition, Team, Fixture, LeagueTable, Post, Media
from fastapi import Request
from typing import List

router = APIRouter()

def get_db(request: Request):
    return request.app.state.db


# Competition CRUD endpoints ...existing code...

# Team CRUD endpoints
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
