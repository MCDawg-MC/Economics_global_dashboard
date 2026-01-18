"""
Momentum Score Models
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class PillarScore(Base):
    """
    Individual pillar scores for each country
    Stores calculated scores for each of the 5 pillars
    """
    __tablename__ = "pillar_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign key
    country_code = Column(String(3), ForeignKey("countries.code"), nullable=False)

    # Time period
    date = Column(DateTime, nullable=False)

    # Pillar identification
    pillar_name = Column(String(50), nullable=False)  # e.g., "external_sector"

    # Scores
    raw_score = Column(Float)  # Weighted average of indicators
    percentile_rank = Column(Float)  # Cross-country percentile (0-100)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    country = relationship("Country", back_populates="pillar_scores")

    def __repr__(self):
        return f"<PillarScore(country={self.country_code}, pillar={self.pillar_name}, date={self.date})>"


class MomentumScore(Base):
    """
    Final aggregated momentum scores for each country
    Combines all pillar scores into final CMI score
    """
    __tablename__ = "momentum_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign key
    country_code = Column(String(3), ForeignKey("countries.code"), nullable=False)

    # Time period
    date = Column(DateTime, nullable=False)

    # Final scores
    momentum_score = Column(Float, nullable=False)  # Weighted average of pillars (0-100)
    structural_score = Column(Float)  # Separate structural/capacity score (0-100)
    combined_score = Column(Float)  # momentum × structural adjustment

    # Classification
    classification = Column(String(50))  # "Strongly Improving", "Improving", etc.

    # Rank
    global_rank = Column(Integer)  # 1-based ranking

    # Change metrics
    score_change_1m = Column(Float)  # Change from 1 month ago
    score_change_3m = Column(Float)  # Change from 3 months ago
    score_change_6m = Column(Float)  # Change from 6 months ago

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    country = relationship("Country", back_populates="momentum_scores")

    def __repr__(self):
        return f"<MomentumScore(country={self.country_code}, score={self.momentum_score}, date={self.date})>"
