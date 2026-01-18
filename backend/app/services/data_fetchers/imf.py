"""
IMF Data Fetcher
Fetches data from IMF International Financial Statistics (IFS) and Monetary & Financial Statistics (MFS)
"""
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
import requests
from app.services.data_fetchers.base import BaseDataFetcher


class IMFFetcher(BaseDataFetcher):
    """
    Fetcher for IMF data (IFS and MFS)
    Uses IMF JSON RESTful API
    """

    BASE_URL = "http://dataservices.imf.org/REST/SDMX_JSON.svc"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize IMF fetcher"""
        super().__init__(api_key)
        self.session = requests.Session()

    def fetch_indicator(
        self,
        country_code: str,
        indicator_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        database: str = "IFS"
    ) -> pd.DataFrame:
        """
        Fetch IMF indicator data for a country

        Args:
            country_code: ISO 3166-1 alpha-2 country code (IMF uses alpha-2)
            indicator_code: IMF indicator code
            start_date: Start date
            end_date: End date
            database: IMF database ('IFS' or 'MFS')

        Returns:
            DataFrame with columns: date, value
        """
        try:
            # Format date range
            start_period = start_date.strftime('%Y') if start_date else '2010'
            end_period = end_date.strftime('%Y') if end_date else datetime.now().strftime('%Y')

            # Build API URL
            # Format: {BASE_URL}/CompactData/{database}/{freq}.{country}.{indicator}?startPeriod={start}&endPeriod={end}
            freq = 'M'  # Monthly frequency
            url = f"{self.BASE_URL}/CompactData/{database}/{freq}.{country_code}.{indicator_code}"

            params = {
                'startPeriod': start_period,
                'endPeriod': end_period
            }

            # Make request
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Parse IMF JSON structure
            df = self._parse_imf_response(data)

            return self.clean_data(df)

        except Exception as e:
            print(f"Error fetching IMF data for {country_code}, {indicator_code}: {e}")
            return pd.DataFrame(columns=['date', 'value'])

    def _parse_imf_response(self, data: dict) -> pd.DataFrame:
        """
        Parse IMF API JSON response

        Args:
            data: JSON response from IMF API

        Returns:
            DataFrame with date and value columns
        """
        try:
            # Navigate IMF JSON structure
            obs_list = data.get('CompactData', {}).get('DataSet', {}).get('Series', {}).get('Obs', [])

            if not obs_list:
                return pd.DataFrame(columns=['date', 'value'])

            # Extract dates and values
            dates = []
            values = []

            for obs in obs_list:
                time_period = obs.get('@TIME_PERIOD', '')
                obs_value = obs.get('@OBS_VALUE', None)

                if time_period and obs_value:
                    # Convert period to datetime
                    # Format is usually YYYY-MM for monthly data
                    date = pd.to_datetime(time_period, format='%Y-%m')
                    dates.append(date)
                    values.append(float(obs_value))

            return pd.DataFrame({
                'date': dates,
                'value': values
            })

        except Exception as e:
            print(f"Error parsing IMF response: {e}")
            return pd.DataFrame(columns=['date', 'value'])

    def fetch_multiple_countries(
        self,
        country_codes: List[str],
        indicator_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        database: str = "IFS"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch IMF data for multiple countries

        Args:
            country_codes: List of country codes
            indicator_code: IMF indicator code
            start_date: Start date
            end_date: End date
            database: IMF database ('IFS' or 'MFS')

        Returns:
            Dictionary mapping country codes to DataFrames
        """
        result = {}

        for country_code in country_codes:
            result[country_code] = self.fetch_indicator(
                country_code,
                indicator_code,
                start_date,
                end_date,
                database
            )

        return result
