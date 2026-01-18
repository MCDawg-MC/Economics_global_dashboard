"""
Base Data Fetcher
Abstract class for all data source fetchers
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime


class BaseDataFetcher(ABC):
    """
    Abstract base class for data fetchers
    All data source fetchers should inherit from this class
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the data fetcher

        Args:
            api_key: Optional API key for authenticated data sources
        """
        self.api_key = api_key

    @abstractmethod
    def fetch_indicator(
        self,
        country_code: str,
        indicator_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Fetch data for a specific indicator and country

        Args:
            country_code: ISO 3166-1 alpha-3 country code
            indicator_code: Source-specific indicator code
            start_date: Start date for data retrieval
            end_date: End date for data retrieval

        Returns:
            DataFrame with columns: date, value
        """
        pass

    @abstractmethod
    def fetch_multiple_countries(
        self,
        country_codes: List[str],
        indicator_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple countries

        Args:
            country_codes: List of ISO 3166-1 alpha-3 country codes
            indicator_code: Source-specific indicator code
            start_date: Start date for data retrieval
            end_date: End date for data retrieval

        Returns:
            Dictionary mapping country codes to DataFrames
        """
        pass

    def validate_country_code(self, country_code: str) -> bool:
        """
        Validate country code format

        Args:
            country_code: Country code to validate

        Returns:
            True if valid, False otherwise
        """
        return len(country_code) == 3 and country_code.isupper()

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize data

        Args:
            df: Raw data DataFrame

        Returns:
            Cleaned DataFrame
        """
        # Remove duplicates
        df = df.drop_duplicates(subset=['date'])

        # Sort by date
        df = df.sort_values('date')

        # Remove null values
        df = df.dropna(subset=['value'])

        return df
