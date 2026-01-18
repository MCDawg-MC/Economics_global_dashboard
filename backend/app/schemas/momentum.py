"""
Momentum Score Pydantic Schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class PillarScoreBase(BaseModel):
    """Base pillar score schema"""
    country_code: str
    date: datetime
    pillar_name: str
    raw_score: Optional[float] = None
    percentile_rank: Optional[float] = None


class PillarScore(PillarScoreBase):
    """Pillar score schema for API responses"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MomentumScoreBase(BaseModel):
    """Base momentum score schema"""
    country_code: str
    date: datetime
    momentum_score: float
    structural_score: Optional[float] = None
    combined_score: Optional[float] = None
    classification: Optional[str] = None
    global_rank: Optional[int] = None
    score_change_1m: Optional[float] = None
    score_change_3m: Optional[float] = None
    score_change_6m: Optional[float] = None


class MomentumScore(MomentumScoreBase):
    """Momentum score schema for API responses"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MomentumScoreWithPillars(MomentumScore):
    """Momentum score with pillar breakdown"""
    pillar_scores: List[PillarScore] = []


class CountryMomentumSummary(BaseModel):
    """Summary of country momentum for leaderboard"""
    country_code: str
    country_name: str
    momentum_score: float
    score_change: float
    classification: str
    global_rank: int


class MomentumLeaderboard(BaseModel):
    """Leaderboard of top improvers and decliners"""
    period: str  # 1m, 3m, 6m
    improvers: List[CountryMomentumSummary]
    decliners: List[CountryMomentumSummary]
