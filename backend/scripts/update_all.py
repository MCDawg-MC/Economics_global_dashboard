"""
Complete Data Update Pipeline
Orchestrates: data fetching → score calculation → database update
"""
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from scripts.fetch_data import DataFetchOrchestrator
from scripts.calculate_scores import ScoreCalculationPipeline


def run_complete_update():
    """
    Run the complete data update pipeline:
    1. Fetch latest data from external APIs
    2. Calculate momentum scores
    3. Update rankings
    """
    print("=" * 60)
    print("COUNTRY MOMENTUM INDEX - DATA UPDATE PIPELINE")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    db = SessionLocal()

    try:
        # Step 1: Fetch Data
        print("\n" + "=" * 60)
        print("STEP 1: FETCHING DATA FROM EXTERNAL SOURCES")
        print("=" * 60)

        fetch_orchestrator = DataFetchOrchestrator(db)
        fetch_orchestrator.fetch_all_indicators()

        print("\n✓ Data fetching completed")

        # Step 2: Calculate Scores
        print("\n" + "=" * 60)
        print("STEP 2: CALCULATING MOMENTUM SCORES")
        print("=" * 60)

        calc_pipeline = ScoreCalculationPipeline(db)
        calc_pipeline.calculate_all_scores()

        print("\n✓ Score calculation completed")

        # Step 3: Summary
        print("\n" + "=" * 60)
        print("UPDATE SUMMARY")
        print("=" * 60)

        from app.models import Country, IndicatorValue, MomentumScore
        from sqlalchemy import func

        # Count statistics
        num_countries = db.query(Country).filter(Country.is_active == True).count()
        num_indicators = db.query(IndicatorValue.indicator_id).distinct().count()
        num_values = db.query(IndicatorValue).count()
        num_scores = db.query(MomentumScore).count()

        latest_date = db.query(func.max(MomentumScore.date)).scalar()

        print(f"\nActive Countries: {num_countries}")
        print(f"Indicators Tracked: {num_indicators}")
        print(f"Total Data Points: {num_values}")
        print(f"Momentum Scores: {num_scores}")
        print(f"Latest Score Date: {latest_date}")

        # Get top 5 countries
        if latest_date:
            top_countries = db.query(
                MomentumScore,
                Country
            ).join(
                Country,
                MomentumScore.country_code == Country.code
            ).filter(
                MomentumScore.date == latest_date
            ).order_by(
                MomentumScore.global_rank
            ).limit(5).all()

            print("\nTop 5 Countries by Momentum:")
            for score, country in top_countries:
                print(f"  {score.global_rank}. {country.name} - {score.momentum_score:.1f} ({score.classification})")

        print("\n" + "=" * 60)
        print("✓ PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print("\n" + "=" * 60)
        print("✗ ERROR DURING UPDATE")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    run_complete_update()
