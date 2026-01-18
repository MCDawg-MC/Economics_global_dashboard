"""
Country Pydantic Schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class CountryBase(BaseModel):
    """Base country schema"""
    code: str
    name: str
    region: Optional[str] = None
    income_group: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Country(CountryBase):
    """Country schema for API responses"""
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CountryDetail(Country):
    """Detailed country information with latest momentum score"""
    latest_momentum_score: Optional[float] = None
    latest_classification: Optional[str] = None
    global_rank: Optional[int] = None

    class Config:
        from_attributes = True


class CountryCreate(CountryBase):
    """Schema for creating a new country"""
    is_active: bool = True


class CountryUpdate(BaseModel):
    """Schema for updating country information"""
    name: Optional[str] = None
    region: Optional[str] = None
    income_group: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = None
