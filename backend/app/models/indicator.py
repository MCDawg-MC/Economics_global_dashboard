"""
Indicator Models
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class Indicator(Base):
    """
    Indicator metadata table
    Defines all economic indicators used in CMI
    """
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)

    # Pillar classification
    pillar = Column(String(50), nullable=False)  # e.g., "external_sector", "inflation"
    weight_in_pillar = Column(Float, nullable=False)  # 0.0 to 1.0

    # Data source
    source = Column(String(50))  # IMF, World Bank, OECD, etc.
    source_series_id = Column(String(100))  # External API series ID

    # Calculation method
    calculation_method = Column(String(50))  # e.g., "yoy_acceleration", "pct_change_6m"

    # Metadata
    unit = Column(String(50))  # %, index, USD, etc.
    frequency = Column(String(20))  # monthly, quarterly, annual
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    values = relationship("IndicatorValue", back_populates="indicator")

    def __repr__(self):
        return f"<Indicator(code={self.code}, name={self.name})>"


class IndicatorValue(Base):
    """
    Indicator time series data
    Stores raw and calculated values for each indicator
    """
    __tablename__ = "indicator_values"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    country_code = Column(String(3), ForeignKey("countries.code"), nullable=False)
    indicator_id = Column(Integer, ForeignKey("indicators.id"), nullable=False)

    # Time period
    date = Column(DateTime, nullable=False)

    # Values
    raw_value = Column(Float)  # Original value from data source
    calculated_value = Column(Float)  # Momentum value (acceleration, change, etc.)
    percentile_rank = Column(Float)  # Cross-country percentile (0-100)
    z_score = Column(Float)  # Standardized z-score

    # Metadata
    is_estimate = Column(Boolean, default=False)  # Flag for estimated/provisional data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    country = relationship("Country", back_populates="indicator_values")
    indicator = relationship("Indicator", back_populates="values")

    def __repr__(self):
        return f"<IndicatorValue(country={self.country_code}, indicator={self.indicator_id}, date={self.date})>"
