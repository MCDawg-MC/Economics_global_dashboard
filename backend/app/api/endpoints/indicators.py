"""
Indicators API Endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.db.session import get_db
from app.schemas.indicator import Indicator, IndicatorValue
from app.models.indicator import Indicator as IndicatorModel
from app.models.indicator import IndicatorValue as IndicatorValueModel
from app.models.country import Country

router = APIRouter()


@router.get("/", response_model=List[Indicator])
async def get_all_indicators(
    db: Session = Depends(get_db)
):
    """
    Get list of all indicators used in the CMI
    """
    indicators = db.query(IndicatorModel).order_by(
        IndicatorModel.pillar,
        IndicatorModel.code
    ).all()

    return indicators


@router.get("/{country_code}/latest")
async def get_country_indicators(
    country_code: str,
    db: Session = Depends(get_db)
):
    """
    Get latest indicator values for a specific country
    """
    # Verify country exists
    country = db.query(Country).filter(
        Country.code == country_code.upper()
    ).first()

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # Get all indicators
    indicators = db.query(IndicatorModel).all()

    # Build response
    indicator_data = {}

    for indicator in indicators:
        # Get latest value for this indicator and country
        latest_value = db.query(IndicatorValueModel).filter(
            IndicatorValueModel.country_code == country_code.upper(),
            IndicatorValueModel.indicator_id == indicator.id
        ).order_by(desc(IndicatorValueModel.date)).first()

        if latest_value:
            indicator_data[indicator.code] = {
                "indicator_name": indicator.name,
                "pillar": indicator.pillar,
                "raw_value": latest_value.raw_value,
                "calculated_value": latest_value.calculated_value,
                "percentile_rank": latest_value.percentile_rank,
                "z_score": latest_value.z_score,
                "date": latest_value.date.isoformat() if latest_value.date else None,
                "unit": indicator.unit
            }

    return {
        "country_code": country_code.upper(),
        "country_name": country.name,
        "indicators": indicator_data
    }


def run_data_refresh():
    """Background task to refresh data"""
    # This would trigger the data fetching pipeline
    # For now, just a placeholder
    import subprocess
    import sys
    from pathlib import Path

    script_path = Path(__file__).resolve().parents[3] / "scripts" / "fetch_data.py"
    subprocess.Popen([sys.executable, str(script_path)])


@router.post("/refresh")
async def refresh_indicators(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger a manual refresh of indicator data
    (Admin endpoint - should be protected in production)
    """
    # Add refresh task to background
    background_tasks.add_task(run_data_refresh)

    return {
        "status": "refresh_started",
        "message": "Data refresh job initiated. This may take several minutes."
    }
