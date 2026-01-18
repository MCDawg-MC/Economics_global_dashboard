"""
Data Fetching Script
Fetches data from all sources and updates database
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import Country, Indicator, IndicatorValue
from app.services.data_fetchers.world_bank import WorldBankFetcher
from app.services.data_fetchers.fred import FREDFetcher
from app.services.data_fetchers.imf import IMFFetcher
from app.services.calculators.momentum import MomentumCalculator
from app.core.config import settings


class DataFetchOrchestrator:
    """
    Orchestrates data fetching from multiple sources
    """

    def __init__(self, db: Session):
        """
        Initialize orchestrator

        Args:
            db: Database session
        """
        self.db = db
        self.wb_fetcher = WorldBankFetcher()
        self.imf_fetcher = IMFFetcher()

        # Initialize FRED fetcher if API key available
        if settings.FRED_API_KEY:
            self.fred_fetcher = FREDFetcher(api_key=settings.FRED_API_KEY)
        else:
            self.fred_fetcher = None
            print("Warning: FRED API key not configured")

        self.calculator = MomentumCalculator()

    def fetch_all_indicators(self):
        """
        Fetch all indicators for all active countries
        """
        # Get active countries
        countries = self.db.query(Country).filter(Country.is_active == True).all()
        print(f"Fetching data for {len(countries)} countries")

        # Get all indicators
        indicators = self.db.query(Indicator).all()
        print(f"Fetching {len(indicators)} indicators")

        # Date range (last 5 years)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5*365)

        # Fetch data for each indicator
        for indicator in indicators:
            print(f"\nFetching {indicator.code} ({indicator.name})...")

            for country in countries:
                try:
                    self.fetch_indicator_for_country(
                        country,
                        indicator,
                        start_date,
                        end_date
                    )
                except Exception as e:
                    print(f"  Error fetching {indicator.code} for {country.code}: {e}")

        print("\nData fetching completed!")

    def fetch_indicator_for_country(
        self,
        country: Country,
        indicator: Indicator,
        start_date: datetime,
        end_date: datetime
    ):
        """
        Fetch specific indicator data for a country

        Args:
            country: Country model
            indicator: Indicator model
            start_date: Start date
            end_date: End date
        """
        # Select appropriate fetcher
        fetcher = None
        if indicator.source == 'World Bank':
            fetcher = self.wb_fetcher
        elif indicator.source == 'IMF':
            fetcher = self.imf_fetcher
        elif indicator.source == 'FRED' and self.fred_fetcher:
            fetcher = self.fred_fetcher
        else:
            print(f"  No fetcher available for {indicator.source}")
            return

        # Fetch raw data
        # Note: This is a placeholder - actual series IDs need to be mapped
        if indicator.source_series_id:
            df = fetcher.fetch_indicator(
                country.code,
                indicator.source_series_id,
                start_date,
                end_date
            )

            if not df.empty:
                print(f"  Fetched {len(df)} observations for {country.code}")
                self.process_and_store(country, indicator, df)
            else:
                print(f"  No data available for {country.code}")

    def process_and_store(self, country: Country, indicator: Indicator, df):
        """
        Process data and store in database

        Args:
            country: Country model
            indicator: Indicator model
            df: DataFrame with raw data
        """
        # Calculate momentum based on calculation method
        if indicator.calculation_method == 'yoy_acceleration':
            df = self.calculator.calculate_yoy_acceleration(df)
        elif indicator.calculation_method == 'pct_change_6m':
            df = self.calculator.calculate_pct_change(df, periods=6)
        elif indicator.calculation_method == 'pct_change_12m':
            df = self.calculator.calculate_pct_change(df, periods=12)
        elif indicator.calculation_method == 'absolute_change_12m':
            df = self.calculator.calculate_absolute_change(df, periods=12)
        elif indicator.calculation_method == 'raw_value':
            df['momentum'] = df['value']

        # Store in database
        for _, row in df.iterrows():
            # Check if record exists
            existing = self.db.query(IndicatorValue).filter(
                IndicatorValue.country_code == country.code,
                IndicatorValue.indicator_id == indicator.id,
                IndicatorValue.date == row['date']
            ).first()

            if existing:
                # Update existing
                existing.raw_value = row['value']
                existing.calculated_value = row.get('momentum')
            else:
                # Create new
                value = IndicatorValue(
                    country_code=country.code,
                    indicator_id=indicator.id,
                    date=row['date'],
                    raw_value=row['value'],
                    calculated_value=row.get('momentum')
                )
                self.db.add(value)

        self.db.commit()


def main():
    """Main function"""
    print("Starting data fetch...")

    db = SessionLocal()

    try:
        orchestrator = DataFetchOrchestrator(db)
        orchestrator.fetch_all_indicators()

    except Exception as e:
        print(f"Error: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
