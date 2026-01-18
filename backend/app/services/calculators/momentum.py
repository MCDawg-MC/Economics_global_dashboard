"""
Momentum Calculator
Calculates momentum indicators from raw time series data
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict
from scipy import stats


class MomentumCalculator:
    """
    Calculates various momentum metrics from time series data
    """

    @staticmethod
    def calculate_yoy_acceleration(df: pd.DataFrame, value_col: str = 'value') -> pd.DataFrame:
        """
        Calculate year-over-year acceleration
        Acceleration = YoY(t) - YoY(t-6m)

        Args:
            df: DataFrame with 'date' and value column
            value_col: Name of the value column

        Returns:
            DataFrame with additional 'momentum' column
        """
        df = df.copy()
        df = df.sort_values('date')

        # Calculate YoY change
        df['yoy'] = df[value_col].pct_change(periods=12) * 100

        # Calculate acceleration (change in YoY)
        df['momentum'] = df['yoy'] - df['yoy'].shift(6)

        return df

    @staticmethod
    def calculate_pct_change(
        df: pd.DataFrame,
        periods: int = 6,
        value_col: str = 'value'
    ) -> pd.DataFrame:
        """
        Calculate percentage change over specified periods

        Args:
            df: DataFrame with 'date' and value column
            periods: Number of periods to look back
            value_col: Name of the value column

        Returns:
            DataFrame with additional 'momentum' column
        """
        df = df.copy()
        df = df.sort_values('date')

        df['momentum'] = df[value_col].pct_change(periods=periods) * 100

        return df

    @staticmethod
    def calculate_absolute_change(
        df: pd.DataFrame,
        periods: int = 6,
        value_col: str = 'value'
    ) -> pd.DataFrame:
        """
        Calculate absolute change over specified periods

        Args:
            df: DataFrame with 'date' and value column
            periods: Number of periods to look back
            value_col: Name of the value column

        Returns:
            DataFrame with additional 'momentum' column
        """
        df = df.copy()
        df = df.sort_values('date')

        df['momentum'] = df[value_col] - df[value_col].shift(periods)

        return df

    @staticmethod
    def calculate_z_score(values: pd.Series) -> pd.Series:
        """
        Calculate z-scores (standardized values)

        Args:
            values: Series of values

        Returns:
            Series of z-scores
        """
        return (values - values.mean()) / values.std()

    @staticmethod
    def calculate_percentile_rank(values: pd.Series) -> pd.Series:
        """
        Calculate percentile ranks (0-100)

        Args:
            values: Series of values

        Returns:
            Series of percentile ranks
        """
        return values.rank(pct=True) * 100

    @staticmethod
    def standardize_cross_country(
        data_dict: Dict[str, pd.DataFrame],
        date: pd.Timestamp,
        value_col: str = 'momentum'
    ) -> Dict[str, float]:
        """
        Calculate cross-country percentile ranks for a specific date

        Args:
            data_dict: Dictionary mapping country codes to DataFrames
            date: Date to calculate ranks for
            value_col: Column containing values to rank

        Returns:
            Dictionary mapping country codes to percentile ranks
        """
        # Extract values for all countries at the specified date
        country_values = {}

        for country_code, df in data_dict.items():
            # Find closest date
            df = df.sort_values('date')
            closest_idx = (df['date'] - date).abs().idxmin()
            value = df.loc[closest_idx, value_col]

            if pd.notna(value):
                country_values[country_code] = value

        # Calculate percentile ranks
        if not country_values:
            return {}

        values_series = pd.Series(country_values)
        percentiles = MomentumCalculator.calculate_percentile_rank(values_series)

        return percentiles.to_dict()

    @staticmethod
    def classify_momentum(score: float) -> str:
        """
        Classify momentum score into categories

        Args:
            score: Momentum percentile score (0-100)

        Returns:
            Classification string
        """
        if score >= 80:
            return "Strongly Improving"
        elif score >= 60:
            return "Improving"
        elif score >= 40:
            return "Neutral"
        elif score >= 20:
            return "Deteriorating"
        else:
            return "Strongly Deteriorating"

    @staticmethod
    def calculate_moving_average(
        df: pd.DataFrame,
        window: int = 3,
        value_col: str = 'value'
    ) -> pd.DataFrame:
        """
        Calculate moving average

        Args:
            df: DataFrame with time series data
            window: Window size for moving average
            value_col: Column to calculate MA for

        Returns:
            DataFrame with additional MA column
        """
        df = df.copy()
        df = df.sort_values('date')
        df[f'{value_col}_ma'] = df[value_col].rolling(window=window).mean()

        return df
