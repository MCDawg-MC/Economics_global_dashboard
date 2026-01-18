"""
Indicator Pydantic Schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class IndicatorBase(BaseModel):
    """Base indicator schema"""
    code: str
    name: str
    description: Optional[str] = None
    pillar: str
    weight_in_pillar: float
    source: Optional[str] = None
    source_series_id: Optional[str] = None
    calculation_method: Optional[str] = None
    unit: Optional[str] = None
    frequency: Optional[str] = None


class Indicator(IndicatorBase):
    """Indicator schema for API responses"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IndicatorCreate(IndicatorBase):
    """Schema for creating a new indicator"""
    pass


class IndicatorValueBase(BaseModel):
    """Base indicator value schema"""
    country_code: str
    indicator_id: int
    date: datetime
    raw_value: Optional[float] = None
    calculated_value: Optional[float] = None
    percentile_rank: Optional[float] = None
    z_score: Optional[float] = None
    is_estimate: bool = False


class IndicatorValue(IndicatorValueBase):
    """Indicator value schema for API responses"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IndicatorValueCreate(IndicatorValueBase):
    """Schema for creating a new indicator value"""
    pass
