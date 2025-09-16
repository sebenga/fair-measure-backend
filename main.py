
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.routers.fixtures import router as fixtures_router
from app.routers.league_table import router as league_table_router
from app.routers.teams import router as teams_router
from app.routers.competitions import router as competitions_router
from app.routers.posts import router as posts_router
from app.routers.media import router as media_router
from app.routers.rules import router as rules_router
from app.routers.scoring_category import router as scoring_category_router
from app.routers.point_accumulation import router as point_accumulation_router
from app.routers.fixture_team import router as fixture_team_router
from app.routers.scoring_event import router as scoring_event_router
from app.routers.reply import router as reply_router

app = FastAPI(title="Fair Measure Competition API", description="Dynamic backend for custom competitions", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(fixtures_router)
app.include_router(league_table_router)
app.include_router(teams_router)
app.include_router(competitions_router)
app.include_router(posts_router)
app.include_router(media_router)
app.include_router(rules_router)
app.include_router(scoring_category_router)
app.include_router(point_accumulation_router)
app.include_router(fixture_team_router)
app.include_router(scoring_event_router)
app.include_router(reply_router)

# MongoDB connection
MONGO_URL = "mongodb+srv://fair-measure:fairmeasure321@fair-measure-db.rkujgqk.mongodb.net/?retryWrites=true&w=majority&appName=fair-measure-db"
client = AsyncIOMotorClient(MONGO_URL)

# Set up MongoDB connection on FastAPI startup
@app.on_event("startup")
async def startup_db_client():
    app.state.db = client["fair_measure_db"]

@app.get("/")
async def root():
    return {"message": "Fair Measure API is running"}
