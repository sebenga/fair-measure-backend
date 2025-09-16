from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class Rule(BaseModel):
    name: str
    description: str

class ScoringCategory(BaseModel):
    name: str
    description: str
    points: int

class PointAccumulation(BaseModel):
    win: int
    lose: int
    draw: int

class Team(BaseModel):
    id: Optional[str]
    competition_id: Optional[str]
    name: str
    description: Optional[str]
    picture_location: Optional[str]

class FixtureTeam(BaseModel):
    team_id: str
    score: int
    details: Optional[Dict] = None

class ScoringEvent(BaseModel):
    team_id: str
    category: str
    points: int
    player: Optional[str]
    time: Optional[str]

class Fixture(BaseModel):
    id: Optional[str]
    competition_id: str
    date_time: datetime
    day: str
    location: str
    is_complete: bool
    teams: List[FixtureTeam]
    scoring_events: List[ScoringEvent]

class LeagueTable(BaseModel):
    id: Optional[str]
    competition_id: str
    team_id: str
    mp: int
    w: int
    d: int
    l: int
    gf: int
    ga: int
    gd: int
    pts: int

class Reply(BaseModel):
    author: str
    date: datetime
    description: str

class Post(BaseModel):
    id: Optional[str]
    competition_id: str
    author: str
    date: datetime
    description: str
    replies: List[Reply]
    media: List[str]

class Media(BaseModel):
    id: Optional[str]
    competition_id: str
    type: str
    date: datetime
    location: Optional[str]
    url: Optional[str]

class Competition(BaseModel):
    id: Optional[str]
    name: str
    author: str
    date_created: datetime
    logo_location: Optional[str]
    is_private: bool
    type: str
    rules: List[Rule]
    scoring_categories: List[ScoringCategory]
    point_accumulation: PointAccumulation
    participants: List[str] = []
    fixtures: List[str] = []
    league_table: List[str] = []
    posts: List[str] = []
    photos: List[str] = []
    videos: List[str] = []
