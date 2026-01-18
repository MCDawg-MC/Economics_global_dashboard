"""
Score Calculation Pipeline
Calculates momentum scores from indicator values
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models import Country, Indicator, IndicatorValue, MomentumScore, PillarScore
from app.services.calculators.momentum import MomentumCalculator
from app.services.calculators.pillar import PillarCalculator


class ScoreCalculationPipeline:
    """
    Pipeline for calculating momentum scores
    """

    def __init__(self, db: Session):
        """
        Initialize pipeline

        Args:
            db: Database session
        """
        self.db = db
        self.momentum_calc = MomentumCalculator()
        self.pillar_calc = PillarCalculator()

    def calculate_all_scores(self, calculation_date: datetime = None):
        """
        Calculate scores for all countries

        Args:
            calculation_date: Date to calculate scores for (default: latest)
        """
        if calculation_date is None:
            # Get the most recent date with indicator data
            calculation_date = self.db.query(
                func.max(IndicatorValue.date)
            ).scalar()

            if not calculation_date:
                print("No indicator data found")
                return

        print(f"\nCalculating scores for date: {calculation_date}")

        # Get active countries
        countries = self.db.query(Country).filter(
            Country.is_active == True
        ).all()

        print(f"Processing {len(countries)} countries...")

        for country in countries:
            try:
                self.calculate_country_scores(country, calculation_date)
            except Exception as e:
                print(f"Error calculating scores for {country.code}: {e}")

        print("\nScore calculation completed!")

    def calculate_country_scores(self, country: Country, date: datetime):
        """
        Calculate scores for a specific country

        Args:
            country: Country model
            date: Calculation date
        """
        print(f"\n  Processing {country.code} - {country.name}")

        # Step 1: Get all indicator values for this country and date
        indicator_values = self.get_indicator_values(country.code, date)

        if not indicator_values:
            print(f"    No indicator data available")
            return

        # Step 2: Calculate cross-country percentiles
        percentile_scores = self.calculate_percentiles(date)

        # Step 3: Get percentile scores for this country
        country_percentiles = {
            code: percentile_scores.get(code, {}).get(country.code)
            for code in indicator_values.keys()
        }

        # Filter out None values
        country_percentiles = {
            k: v for k, v in country_percentiles.items() if v is not None
        }

        print(f"    Found {len(country_percentiles)} indicator percentiles")

        # Step 4: Calculate pillar scores
        pillar_scores = self.pillar_calc.calculate_all_pillars(country_percentiles)

        # Store pillar scores
        for pillar_name, score in pillar_scores.items():
            if score is not None:
                self.store_pillar_score(country.code, date, pillar_name, score)

        print(f"    Calculated {len([s for s in pillar_scores.values() if s is not None])} pillar scores")

        # Step 5: Calculate final momentum score (excluding structural)
        momentum_score = self.pillar_calc.calculate_momentum_score(
            pillar_scores,
            exclude_structural=True
        )

        # Step 6: Get structural score separately
        structural_score = pillar_scores.get('structural')

        # Step 7: Calculate combined score if both exist
        combined_score = None
        if momentum_score and structural_score:
            combined_score = self.pillar_calc.calculate_combined_score(
                momentum_score,
                structural_score
            )

        # Step 8: Classify momentum
        classification = None
        if momentum_score:
            classification = self.momentum_calc.classify_momentum(momentum_score)

        # Step 9: Calculate score changes
        score_changes = self.calculate_score_changes(country.code, date, momentum_score)

        # Step 10: Store momentum score
        if momentum_score:
            self.store_momentum_score(
                country.code,
                date,
                momentum_score,
                structural_score,
                combined_score,
                classification,
                score_changes
            )

            print(f"    Momentum Score: {momentum_score:.2f} ({classification})")
            if combined_score:
                print(f"    Combined Score: {combined_score:.2f}")

    def get_indicator_values(self, country_code: str, date: datetime) -> Dict:
        """
        Get indicator values for a country on a specific date

        Args:
            country_code: Country code
            date: Date

        Returns:
            Dictionary mapping indicator codes to values
        """
        # Get values within a 30-day window of the date
        date_start = date - timedelta(days=30)
        date_end = date + timedelta(days=30)

        values = self.db.query(
            IndicatorValue,
            Indicator
        ).join(
            Indicator,
            IndicatorValue.indicator_id == Indicator.id
        ).filter(
            IndicatorValue.country_code == country_code,
            IndicatorValue.date >= date_start,
            IndicatorValue.date <= date_end
        ).all()

        # Get the closest value for each indicator
        indicator_values = {}
        for value, indicator in values:
            if indicator.code not in indicator_values:
                indicator_values[indicator.code] = value.calculated_value

        return indicator_values

    def calculate_percentiles(self, date: datetime) -> Dict[str, Dict[str, float]]:
        """
        Calculate cross-country percentiles for all indicators

        Args:
            date: Calculation date

        Returns:
            Nested dictionary: {indicator_code: {country_code: percentile}}
        """
        date_start = date - timedelta(days=30)
        date_end = date + timedelta(days=30)

        # Get all indicator values for this date
        values = self.db.query(
            IndicatorValue,
            Indicator
        ).join(
            Indicator,
            IndicatorValue.indicator_id == Indicator.id
        ).filter(
            IndicatorValue.date >= date_start,
            IndicatorValue.date <= date_end
        ).all()

        # Group by indicator
        indicator_values = {}
        for value, indicator in values:
            if indicator.code not in indicator_values:
                indicator_values[indicator.code] = {}

            # Store value for this country
            if value.calculated_value is not None:
                indicator_values[indicator.code][value.country_code] = value.calculated_value

        # Calculate percentiles for each indicator
        percentiles = {}
        for indicator_code, country_values in indicator_values.items():
            if len(country_values) >= 3:  # Need at least 3 countries
                # Create series and calculate percentiles
                import pandas as pd
                series = pd.Series(country_values)
                percentile_series = self.momentum_calc.calculate_percentile_rank(series)
                percentiles[indicator_code] = percentile_series.to_dict()

                # Update database with percentile ranks
                for country_code, percentile in percentile_series.items():
                    self.db.query(IndicatorValue).filter(
                        IndicatorValue.country_code == country_code,
                        IndicatorValue.indicator_id == self.db.query(Indicator).filter(
                            Indicator.code == indicator_code
                        ).first().id,
                        IndicatorValue.date >= date_start,
                        IndicatorValue.date <= date_end
                    ).update({"percentile_rank": percentile})

        self.db.commit()

        return percentiles

    def calculate_score_changes(
        self,
        country_code: str,
        current_date: datetime,
        current_score: float
    ) -> Dict:
        """
        Calculate score changes over different periods

        Args:
            country_code: Country code
            current_date: Current date
            current_score: Current momentum score

        Returns:
            Dictionary with 1m, 3m, 6m changes
        """
        changes = {
            "1m": None,
            "3m": None,
            "6m": None
        }

        if not current_score:
            return changes

        # Define time periods
        periods = {
            "1m": 30,
            "3m": 90,
            "6m": 180
        }

        for period_name, days in periods.items():
            past_date = current_date - timedelta(days=days)

            # Get score from that period
            past_score = self.db.query(MomentumScore).filter(
                MomentumScore.country_code == country_code,
                MomentumScore.date >= past_date - timedelta(days=15),
                MomentumScore.date <= past_date + timedelta(days=15)
            ).order_by(MomentumScore.date.desc()).first()

            if past_score:
                changes[period_name] = current_score - past_score.momentum_score

        return changes

    def store_pillar_score(
        self,
        country_code: str,
        date: datetime,
        pillar_name: str,
        score: float
    ):
        """
        Store pillar score in database

        Args:
            country_code: Country code
            date: Date
            pillar_name: Pillar name
            score: Score value
        """
        # Check if exists
        existing = self.db.query(PillarScore).filter(
            PillarScore.country_code == country_code,
            PillarScore.date == date,
            PillarScore.pillar_name == pillar_name
        ).first()

        if existing:
            existing.raw_score = score
            existing.percentile_rank = score  # Already a percentile
        else:
            pillar_score = PillarScore(
                country_code=country_code,
                date=date,
                pillar_name=pillar_name,
                raw_score=score,
                percentile_rank=score
            )
            self.db.add(pillar_score)

        self.db.commit()

    def store_momentum_score(
        self,
        country_code: str,
        date: datetime,
        momentum_score: float,
        structural_score: float,
        combined_score: float,
        classification: str,
        score_changes: Dict
    ):
        """
        Store momentum score in database

        Args:
            country_code: Country code
            date: Date
            momentum_score: Momentum score
            structural_score: Structural score
            combined_score: Combined score
            classification: Classification
            score_changes: Dictionary of score changes
        """
        # Check if exists
        existing = self.db.query(MomentumScore).filter(
            MomentumScore.country_code == country_code,
            MomentumScore.date == date
        ).first()

        if existing:
            existing.momentum_score = momentum_score
            existing.structural_score = structural_score
            existing.combined_score = combined_score
            existing.classification = classification
            existing.score_change_1m = score_changes.get("1m")
            existing.score_change_3m = score_changes.get("3m")
            existing.score_change_6m = score_changes.get("6m")
        else:
            score = MomentumScore(
                country_code=country_code,
                date=date,
                momentum_score=momentum_score,
                structural_score=structural_score,
                combined_score=combined_score,
                classification=classification,
                score_change_1m=score_changes.get("1m"),
                score_change_3m=score_changes.get("3m"),
                score_change_6m=score_changes.get("6m")
            )
            self.db.add(score)

        self.db.commit()

        # Update global ranks
        self.update_global_ranks(date)

    def update_global_ranks(self, date: datetime):
        """
        Update global ranks for all countries on a specific date

        Args:
            date: Date
        """
        # Get all scores for this date
        scores = self.db.query(MomentumScore).filter(
            MomentumScore.date == date
        ).order_by(MomentumScore.momentum_score.desc()).all()

        # Update ranks
        for rank, score in enumerate(scores, 1):
            score.global_rank = rank

        self.db.commit()


def main():
    """Main function"""
    print("Starting score calculation pipeline...")

    db = SessionLocal()

    try:
        pipeline = ScoreCalculationPipeline(db)
        pipeline.calculate_all_scores()

        print("\n✓ Score calculation completed successfully!")

    except Exception as e:
        print(f"\n✗ Error during calculation: {e}")
        import traceback
        traceback.print_exc()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
