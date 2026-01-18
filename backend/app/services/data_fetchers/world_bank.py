"""
World Bank Data Fetcher
Fetches data from World Bank API using wbgapi
"""
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
import wbgapi as wb
from app.services.data_fetchers.base import BaseDataFetcher


class WorldBankFetcher(BaseDataFetcher):
    """
    Fetcher for World Bank data
    Uses wbgapi library for API access
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize World Bank fetcher"""
        super().__init__(api_key)

    def fetch_indicator(
        self,
        country_code: str,
        indicator_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Fetch World Bank indicator data for a country

        Args:
            country_code: ISO 3166-1 alpha-3 country code
            indicator_code: World Bank indicator code (e.g., 'NY.GDP.MKTP.CD')
            start_date: Start date
            end_date: End date

        Returns:
            DataFrame with columns: date, value
        """
        try:
            # Convert dates to years if provided
            start_year = start_date.year if start_date else None
            end_year = end_date.year if end_date else None

            # Fetch data using wbgapi
            data = wb.data.DataFrame(
                indicator_code,
                country_code,
                time=range(start_year, end_year + 1) if start_year and end_year else None,
                skipBlanks=True,
                numericTimeKeys=True
            )

            # Convert to our standard format
            df = pd.DataFrame({
                'date': pd.to_datetime([f'{year}-12-31' for year in data.columns]),
                'value': data.iloc[0].values
            })

            return self.clean_data(df)

        except Exception as e:
            print(f"Error fetching World Bank data for {country_code}, {indicator_code}: {e}")
            return pd.DataFrame(columns=['date', 'value'])

    def fetch_multiple_countries(
        self,
        country_codes: List[str],
        indicator_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch World Bank data for multiple countries

        Args:
            country_codes: List of country codes
            indicator_code: World Bank indicator code
            start_date: Start date
            end_date: End date

        Returns:
            Dictionary mapping country codes to DataFrames
        """
        result = {}

        for country_code in country_codes:
            result[country_code] = self.fetch_indicator(
                country_code,
                indicator_code,
                start_date,
                end_date
            )

        return result

    def search_indicators(self, search_term: str) -> pd.DataFrame:
        """
        Search for World Bank indicators

        Args:
            search_term: Search query

        Returns:
            DataFrame with indicator information
        """
        try:
            results = wb.series.info(q=search_term)
            return pd.DataFrame(results)
        except Exception as e:
            print(f"Error searching indicators: {e}")
            return pd.DataFrame()
