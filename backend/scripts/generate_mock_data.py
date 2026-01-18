"""
Generate Mock Data for Testing
Creates realistic mock data for all indicators and countries
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import Country, Indicator, IndicatorValue


def generate_mock_data(months: int = 24):
    """
    Generate mock indicator data for testing

    Args:
        months: Number of months of historical data to generate
    """
    print(f"Generating {months} months of mock data...")

    db = SessionLocal()

    try:
        # Get all countries and indicators
        countries = db.query(Country).filter(Country.is_active == True).all()
        indicators = db.query(Indicator).all()

        print(f"Countries: {len(countries)}")
        print(f"Indicators: {len(indicators)}")

        # Generate data for each month
        end_date = datetime.now()
        dates = [end_date - timedelta(days=30*i) for i in range(months)]
        dates.reverse()  # Chronological order

        total_values = 0

        for date in dates:
            print(f"\nGenerating data for {date.strftime('%Y-%m')}...")

            for country in countries:
                for indicator in indicators:
                    # Generate realistic mock value based on indicator
                    raw_value = generate_realistic_value(indicator, country)

                    # Check if value already exists
                    existing = db.query(IndicatorValue).filter(
                        IndicatorValue.country_code == country.code,
                        IndicatorValue.indicator_id == indicator.id,
                        IndicatorValue.date == date
                    ).first()

                    if existing:
                        continue

                    # Create indicator value
                    value = IndicatorValue(
                        country_code=country.code,
                        indicator_id=indicator.id,
                        date=date,
                        raw_value=raw_value,
                        calculated_value=raw_value  # Will be recalculated
                    )

                    db.add(value)
                    total_values += 1

            # Commit after each month
            db.commit()
            print(f"  Added {len(countries) * len(indicators)} values")

        print(f"\n✓ Generated {total_values} mock data points")

    except Exception as e:
        print(f"Error generating mock data: {e}")
        db.rollback()
        raise

    finally:
        db.close()


def generate_realistic_value(indicator: Indicator, country: Country) -> float:
    """
    Generate realistic mock value for an indicator

    Args:
        indicator: Indicator model
        country: Country model

    Returns:
        Mock value
    """
    # Base values by indicator type
    indicator_ranges = {
        # External sector
        'fx_momentum': (-10, 10),  # % change
        'fx_reserves_change': (-15, 20),  # % change
        'export_growth_momentum': (-5, 15),  # % acceleration

        # Inflation
        'cpi_acceleration': (-3, 5),  # % acceleration
        'core_cpi_acceleration': (-2, 4),  # % acceleration

        # Real activity
        'industrial_production_acceleration': (-10, 15),  # % acceleration
        'pmi': (40, 60),  # Index (50 = neutral)

        # Monetary/Financial
        'policy_rate_change': (-2, 2),  # % change
        'balance_sheet_growth': (-10, 30),  # % change
        'credit_growth': (-5, 20),  # % YoY

        # Structural
        'education_index': (0.4, 0.95),  # Index 0-1
        'industry_composition': (10, 40),  # % of GDP
        'diversification': (0.3, 0.8),  # Index 0-1
    }

    # Get range for this indicator
    min_val, max_val = indicator_ranges.get(
        indicator.code,
        (0, 100)  # Default range
    )

    # Add country-specific bias
    country_bias = hash(country.code) % 20 - 10  # -10 to +10

    # Generate value with some randomness
    base_value = random.uniform(min_val, max_val)

    # Add trend (slight upward or downward)
    trend = (random.random() - 0.5) * 0.1 * (max_val - min_val)

    value = base_value + (country_bias * 0.1) + trend

    # Clamp to range
    value = max(min_val, min(max_val, value))

    return round(value, 2)


def main():
    """Main function"""
    print("=" * 60)
    print("MOCK DATA GENERATOR")
    print("=" * 60)

    # Generate 24 months of data
    generate_mock_data(months=24)

    print("\n✓ Mock data generation completed!")
    print("\nNext steps:")
    print("  1. Run: python scripts/calculate_scores.py")
    print("  2. Start API: uvicorn app.main:app --reload")
    print("  3. Visit: http://localhost:8000/api/v1/docs")


if __name__ == "__main__":
    main()
