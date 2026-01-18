"""
FRED Data Fetcher
Fetches data from Federal Reserve Economic Data (FRED) API
"""
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
from fredapi import Fred
from app.services.data_fetchers.base import BaseDataFetcher


class FREDFetcher(BaseDataFetcher):
    """
    Fetcher for FRED data
    Uses fredapi library for API access
    """

    def __init__(self, api_key: str):
        """
        Initialize FRED fetcher

        Args:
            api_key: FRED API key (required)
        """
        super().__init__(api_key)
        if not api_key:
            raise ValueError("FRED API key is required")
        self.fred = Fred(api_key=api_key)

    def fetch_indicator(
        self,
        country_code: str,
        indicator_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Fetch FRED indicator data

        Note: FRED series codes are not country-specific, so country_code
        should be embedded in the indicator_code if needed

        Args:
            country_code: Not used directly (included for interface compatibility)
            indicator_code: FRED series ID (e.g., 'GDPC1', 'CPIAUCSL')
            start_date: Start date
            end_date: End date

        Returns:
            DataFrame with columns: date, value
        """
        try:
            # Fetch data from FRED
            series = self.fred.get_series(
                indicator_code,
                observation_start=start_date,
                observation_end=end_date
            )

            # Convert to DataFrame
            df = pd.DataFrame({
                'date': series.index,
                'value': series.values
            })

            return self.clean_data(df)

        except Exception as e:
            print(f"Error fetching FRED data for {indicator_code}: {e}")
            return pd.DataFrame(columns=['date', 'value'])

    def fetch_multiple_countries(
        self,
        country_codes: List[str],
        indicator_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch FRED data for multiple countries

        Note: For FRED, country_codes should contain series IDs, not ISO codes

        Args:
            country_codes: List of FRED series IDs
            indicator_code: Not used (included for interface compatibility)
            start_date: Start date
            end_date: End date

        Returns:
            Dictionary mapping series IDs to DataFrames
        """
        result = {}

        for series_id in country_codes:
            result[series_id] = self.fetch_indicator(
                series_id,
                series_id,  # Use series_id as indicator_code
                start_date,
                end_date
            )

        return result

    def search_series(self, search_term: str, limit: int = 10) -> pd.DataFrame:
        """
        Search for FRED series

        Args:
            search_term: Search query
            limit: Maximum number of results

        Returns:
            DataFrame with series information
        """
        try:
            results = self.fred.search(search_term, limit=limit)
            return results
        except Exception as e:
            print(f"Error searching FRED series: {e}")
            return pd.DataFrame()
