"""
Momentum Scores API Endpoints
"""
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.db.session import get_db
from app.schemas.momentum import MomentumScore, MomentumLeaderboard, CountryMomentumSummary
from app.models.momentum import MomentumScore as MomentumScoreModel
from app.models.country import Country

router = APIRouter()


@router.get("/latest", response_model=List[MomentumScore])
async def get_latest_momentum_scores(
    db: Session = Depends(get_db)
):
    """
    Get the latest momentum scores for all countries
    """
    # Get the most recent date
    latest_date = db.query(func.max(MomentumScoreModel.date)).scalar()

    if not latest_date:
        return []

    # Get all scores for that date
    scores = db.query(MomentumScoreModel).filter(
        MomentumScoreModel.date == latest_date
    ).order_by(MomentumScoreModel.global_rank).all()

    return scores


@router.get("/leaderboard", response_model=MomentumLeaderboard)
async def get_momentum_leaderboard(
    period: str = Query("1m", regex="^(1m|3m|6m)$"),
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get top improvers and decliners
    period: 1m, 3m, or 6m
    """
    # Map period to score change column
    period_map = {
        "1m": "score_change_1m",
        "3m": "score_change_3m",
        "6m": "score_change_6m"
    }

    change_column = period_map[period]

    # Get latest date
    latest_date = db.query(func.max(MomentumScoreModel.date)).scalar()

    if not latest_date:
        return {
            "period": period,
            "improvers": [],
            "decliners": []
        }

    # Get scores with change values
    scores = db.query(
        MomentumScoreModel,
        Country
    ).join(
        Country,
        MomentumScoreModel.country_code == Country.code
    ).filter(
        MomentumScoreModel.date == latest_date
    ).all()

    # Build list with change values
    countries_with_change = []
    for score, country in scores:
        change_value = getattr(score, change_column)
        if change_value is not None:
            countries_with_change.append({
                "country_code": country.code,
                "country_name": country.name,
                "momentum_score": score.momentum_score,
                "score_change": change_value,
                "classification": score.classification,
                "global_rank": score.global_rank
            })

    # Sort by change (descending for improvers, ascending for decliners)
    countries_with_change.sort(key=lambda x: x["score_change"], reverse=True)

    # Get top improvers and decliners
    improvers = countries_with_change[:limit]
    decliners = countries_with_change[-limit:][::-1]  # Reverse to get worst first

    return {
        "period": period,
        "improvers": improvers,
        "decliners": decliners
    }


@router.get("/map-data")
async def get_map_data(
    include_structural: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get momentum data formatted for map visualization
    Returns GeoJSON with country scores
    """
    # Get latest date
    latest_date = db.query(func.max(MomentumScoreModel.date)).scalar()

    if not latest_date:
        return {
            "type": "FeatureCollection",
            "features": []
        }

    # Get scores with country info
    scores = db.query(
        MomentumScoreModel,
        Country
    ).join(
        Country,
        MomentumScoreModel.country_code == Country.code
    ).filter(
        MomentumScoreModel.date == latest_date,
        Country.latitude.isnot(None),
        Country.longitude.isnot(None)
    ).all()

    # Helper function to get color based on classification
    def get_color(classification):
        color_map = {
            "Strongly Improving": "#2E7D32",  # Dark green
            "Improving": "#66BB6A",  # Green
            "Neutral": "#FDD835",  # Yellow
            "Deteriorating": "#FB8C00",  # Orange
            "Strongly Deteriorating": "#D32F2F"  # Red
        }
        return color_map.get(classification, "#9E9E9E")  # Gray default

    # Build GeoJSON features
    features = []
    for score, country in scores:
        score_value = score.combined_score if include_structural else score.momentum_score

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [country.longitude, country.latitude]
            },
            "properties": {
                "country_code": country.code,
                "country_name": country.name,
                "momentum_score": score.momentum_score,
                "structural_score": score.structural_score,
                "combined_score": score.combined_score,
                "classification": score.classification,
                "global_rank": score.global_rank,
                "color": get_color(score.classification),
                "score": score_value  # The score to display
            }
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }
