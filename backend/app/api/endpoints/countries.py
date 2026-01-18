"""
Countries API Endpoints
"""
from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.schemas.country import Country, CountryDetail
from app.models.country import Country as CountryModel
from app.models.momentum import MomentumScore

router = APIRouter()


@router.get("/", response_model=List[Country])
async def get_countries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get list of all countries with basic info
    """
    countries = db.query(CountryModel).filter(
        CountryModel.is_active == True
    ).offset(skip).limit(limit).all()

    return countries


@router.get("/{country_code}", response_model=CountryDetail)
async def get_country_detail(
    country_code: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information for a specific country
    """
    # Get country
    country = db.query(CountryModel).filter(
        CountryModel.code == country_code.upper()
    ).first()

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # Get latest momentum score
    latest_score = db.query(MomentumScore).filter(
        MomentumScore.country_code == country_code.upper()
    ).order_by(desc(MomentumScore.date)).first()

    # Build response
    country_dict = {
        "code": country.code,
        "name": country.name,
        "region": country.region,
        "income_group": country.income_group,
        "latitude": country.latitude,
        "longitude": country.longitude,
        "is_active": country.is_active,
        "created_at": country.created_at,
        "updated_at": country.updated_at,
        "latest_momentum_score": latest_score.momentum_score if latest_score else None,
        "latest_classification": latest_score.classification if latest_score else None,
        "global_rank": latest_score.global_rank if latest_score else None
    }

    return country_dict


@router.get("/{country_code}/momentum-history")
async def get_country_momentum_history(
    country_code: str,
    months: int = 12,
    db: Session = Depends(get_db)
):
    """
    Get historical momentum scores for a country
    """
    # Verify country exists
    country = db.query(CountryModel).filter(
        CountryModel.code == country_code.upper()
    ).first()

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # Calculate date threshold
    cutoff_date = datetime.utcnow() - timedelta(days=months * 30)

    # Get historical scores
    scores = db.query(MomentumScore).filter(
        MomentumScore.country_code == country_code.upper(),
        MomentumScore.date >= cutoff_date
    ).order_by(MomentumScore.date).all()

    # Format response
    history = [
        {
            "date": score.date.isoformat(),
            "momentum_score": score.momentum_score,
            "structural_score": score.structural_score,
            "combined_score": score.combined_score,
            "classification": score.classification,
            "global_rank": score.global_rank
        }
        for score in scores
    ]

    return {
        "country_code": country_code.upper(),
        "country_name": country.name,
        "history": history
    }
