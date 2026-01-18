"""
Country Model
"""
from sqlalchemy import Column, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class Country(Base):
    """
    Country master table
    Stores basic country metadata
    """
    __tablename__ = "countries"

    code = Column(String(3), primary_key=True)  # ISO 3166-1 alpha-3
    name = Column(String(100), nullable=False)
    region = Column(String(50))
    income_group = Column(String(50))

    # Coordinates for map display
    latitude = Column(Float)
    longitude = Column(Float)

    # Metadata
    is_active = Column(Boolean, default=True)  # Include in calculations
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    indicator_values = relationship("IndicatorValue", back_populates="country")
    momentum_scores = relationship("MomentumScore", back_populates="country")
    pillar_scores = relationship("PillarScore", back_populates="country")

    def __repr__(self):
        return f"<Country(code={self.code}, name={self.name})>"
