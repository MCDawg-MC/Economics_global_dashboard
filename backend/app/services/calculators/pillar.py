"""
Pillar Score Calculator
Aggregates individual indicators into pillar scores
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime


class PillarCalculator:
    """
    Calculates aggregate pillar scores from individual indicator scores
    """

    # Pillar definitions with weights
    PILLAR_WEIGHTS = {
        'external_sector': 0.25,
        'inflation': 0.20,
        'real_activity': 0.20,
        'monetary_financial': 0.20,
        'structural': 0.15
    }

    # Indicator weights within each pillar
    INDICATOR_WEIGHTS = {
        'external_sector': {
            'fx_momentum': 0.40,
            'fx_reserves_change': 0.30,
            'export_growth_momentum': 0.30
        },
        'inflation': {
            'cpi_acceleration': 0.70,
            'core_cpi_acceleration': 0.30
        },
        'real_activity': {
            'industrial_production_acceleration': 0.60,
            'pmi': 0.40
        },
        'monetary_financial': {
            'policy_rate_change': 0.40,
            'balance_sheet_growth': 0.30,
            'credit_growth': 0.30
        },
        'structural': {
            'education_index': 0.40,
            'industry_composition': 0.40,
            'diversification': 0.20
        }
    }

    @staticmethod
    def calculate_pillar_score(
        indicator_scores: Dict[str, float],
        pillar_name: str
    ) -> Optional[float]:
        """
        Calculate weighted average score for a pillar

        Args:
            indicator_scores: Dictionary mapping indicator codes to percentile scores
            pillar_name: Name of the pillar

        Returns:
            Pillar score (0-100) or None if insufficient data
        """
        if pillar_name not in PillarCalculator.INDICATOR_WEIGHTS:
            raise ValueError(f"Unknown pillar: {pillar_name}")

        weights = PillarCalculator.INDICATOR_WEIGHTS[pillar_name]

        # Calculate weighted average
        weighted_sum = 0
        weight_total = 0

        for indicator_code, weight in weights.items():
            if indicator_code in indicator_scores:
                score = indicator_scores[indicator_code]
                if pd.notna(score):
                    weighted_sum += score * weight
                    weight_total += weight

        # Return None if we have less than 50% of indicators
        if weight_total < 0.5:
            return None

        # Normalize to account for missing indicators
        return weighted_sum / weight_total if weight_total > 0 else None

    @staticmethod
    def calculate_all_pillars(
        indicator_scores: Dict[str, float]
    ) -> Dict[str, Optional[float]]:
        """
        Calculate scores for all pillars

        Args:
            indicator_scores: Dictionary mapping indicator codes to percentile scores

        Returns:
            Dictionary mapping pillar names to scores
        """
        pillar_scores = {}

        for pillar_name in PillarCalculator.PILLAR_WEIGHTS.keys():
            score = PillarCalculator.calculate_pillar_score(
                indicator_scores,
                pillar_name
            )
            pillar_scores[pillar_name] = score

        return pillar_scores

    @staticmethod
    def calculate_momentum_score(
        pillar_scores: Dict[str, float],
        exclude_structural: bool = True
    ) -> Optional[float]:
        """
        Calculate final momentum score from pillar scores

        Args:
            pillar_scores: Dictionary mapping pillar names to scores
            exclude_structural: If True, exclude structural pillar from momentum score

        Returns:
            Final momentum score (0-100) or None if insufficient data
        """
        weighted_sum = 0
        weight_total = 0

        for pillar_name, weight in PillarCalculator.PILLAR_WEIGHTS.items():
            # Skip structural pillar if requested
            if exclude_structural and pillar_name == 'structural':
                continue

            if pillar_name in pillar_scores:
                score = pillar_scores[pillar_name]
                if pd.notna(score):
                    weighted_sum += score * weight
                    weight_total += weight

        # Normalize weights
        if weight_total == 0:
            return None

        # Normalize to 0-100 scale
        if exclude_structural:
            # Renormalize without structural pillar
            momentum_weight_total = sum(
                w for p, w in PillarCalculator.PILLAR_WEIGHTS.items()
                if p != 'structural'
            )
            return (weighted_sum / weight_total) * (momentum_weight_total / weight_total)
        else:
            return weighted_sum / weight_total

    @staticmethod
    def calculate_combined_score(
        momentum_score: float,
        structural_score: float,
        structural_weight: float = 0.3
    ) -> float:
        """
        Calculate combined score (momentum × structural adjustment)

        Args:
            momentum_score: Momentum score (0-100)
            structural_score: Structural score (0-100)
            structural_weight: Weight for structural component (0-1)

        Returns:
            Combined score (0-100)
        """
        # Convert scores to 0-1 scale
        mom_norm = momentum_score / 100
        struct_norm = structural_score / 100

        # Weighted combination
        combined = (
            mom_norm * (1 - structural_weight) +
            (mom_norm * struct_norm) * structural_weight
        )

        # Convert back to 0-100 scale
        return combined * 100
