# Confidence Calibration System
# Implements Satya principle with time-based confidence degradation

from typing import Dict, List, Any
from datetime import datetime, timedelta
import statistics
import logging

logger = logging.getLogger(__name__)

class ConfidenceCalibrator:
    """
    Calibrates confidence levels based on Satya principle.

    Confidence Scale (MANDATORY):
    - HIGH: 0-7 days (observed data + verified forecasts)
    - MEDIUM: 8-21 days (model forecasts, ±20% variance)
    - LOW: 22+ days (directional trends only, ±40% variance)
    """

    def __init__(self):
        self.confidence_thresholds = {
            'HIGH': {'max_days': 7, 'min_convergence': 0.75, 'max_variance': 0.10},
            'MEDIUM': {'max_days': 21, 'min_convergence': 0.50, 'max_variance': 0.20},
            'LOW': {'max_days': float('inf'), 'min_convergence': 0.0, 'max_variance': 0.40}
        }

    def calibrate_confidence(
        self,
        assessment: Dict,
        data_freshness: float,
        indicator_convergence: float,
        forecast_horizon: int
    ) -> Dict:
        """
        Calibrate overall confidence based on multiple factors

        Args:
            assessment: The drought assessment dict
            data_freshness: Average hours since data collection (lower = better)
            indicator_convergence: 0-1 score of indicator agreement
            forecast_horizon: Days into future being forecast

        Returns:
            Assessment with calibrated confidence
        """
        # Start with time-based confidence
        time_confidence = self._calculate_time_confidence(forecast_horizon)

        # Adjust for data freshness
        freshness_penalty = self._calculate_freshness_penalty(data_freshness)

        # Adjust for indicator convergence
        convergence_bonus = self._calculate_convergence_bonus(indicator_convergence)

        # Calculate final confidence
        final_confidence = self._combine_confidence_factors(
            time_confidence, freshness_penalty, convergence_bonus
        )

        # Update assessment
        assessment['confidence'] = final_confidence
        assessment['confidence_factors'] = {
            'time_based': time_confidence,
            'freshness_penalty': freshness_penalty,
            'convergence_bonus': convergence_bonus,
            'data_freshness_hours': data_freshness,
            'indicator_convergence': indicator_convergence,
            'forecast_horizon_days': forecast_horizon
        }

        # Add confidence reason
        assessment['confidence_reason'] = self._generate_confidence_reason(
            final_confidence, forecast_horizon, data_freshness, indicator_convergence
        )

        return assessment

    def _calculate_time_confidence(self, forecast_days: int) -> str:
        """
        Calculate confidence based purely on forecast horizon (Satya principle)
        """
        if forecast_days <= 7:
            return 'HIGH'
        elif forecast_days <= 21:
            return 'MEDIUM'
        else:
            return 'LOW'

    def _calculate_freshness_penalty(self, avg_freshness_hours: float) -> float:
        """
        Calculate confidence penalty based on data freshness
        Returns multiplier (0.5 = 50% confidence reduction)
        """
        if avg_freshness_hours <= 6:  # Very fresh data
            return 1.0
        elif avg_freshness_hours <= 12:  # Fresh data
            return 0.95
        elif avg_freshness_hours <= 24:  # Day-old data
            return 0.85
        elif avg_freshness_hours <= 48:  # Two-day-old data
            return 0.70
        else:  # Stale data
            return 0.50

    def _calculate_convergence_bonus(self, convergence: float) -> float:
        """
        Calculate confidence bonus based on indicator convergence
        Returns multiplier (1.2 = 20% confidence increase)
        """
        if convergence >= 0.9:  # Near perfect agreement
            return 1.2
        elif convergence >= 0.75:  # Strong agreement
            return 1.1
        elif convergence >= 0.5:  # Moderate agreement
            return 1.0
        elif convergence >= 0.25:  # Weak agreement
            return 0.9
        else:  # Poor agreement
            return 0.8

    def _combine_confidence_factors(
        self,
        time_confidence: str,
        freshness_penalty: float,
        convergence_bonus: float
    ) -> str:
        """
        Combine all factors to determine final confidence level
        """
        # Start with time-based confidence as base
        confidence_levels = ['LOW', 'MEDIUM', 'HIGH']
        base_index = confidence_levels.index(time_confidence)

        # Apply freshness penalty and convergence bonus
        combined_multiplier = freshness_penalty * convergence_bonus

        # Adjust confidence level based on combined factors
        if combined_multiplier >= 1.15:  # Strong positive factors
            final_index = min(base_index + 1, 2)  # Can upgrade one level
        elif combined_multiplier >= 0.9:  # Neutral to slightly positive
            final_index = base_index
        elif combined_multiplier >= 0.7:  # Moderate penalty
            final_index = max(base_index - 1, 0)  # Can downgrade one level
        else:  # Strong penalty
            final_index = 0  # Force LOW confidence

        return confidence_levels[final_index]

    def _generate_confidence_reason(
        self,
        final_confidence: str,
        forecast_days: int,
        data_freshness: float,
        convergence: float
    ) -> str:
        """
        Generate human-readable explanation for confidence level
        """
        reasons = []

        # Time-based reason
        if forecast_days <= 7:
            reasons.append("forecast horizon ≤7 days")
        elif forecast_days <= 21:
            reasons.append("forecast horizon 8-21 days")
        else:
            reasons.append("forecast horizon >21 days")

        # Data freshness
        if data_freshness <= 6:
            reasons.append("very fresh data (<6h old)")
        elif data_freshness <= 12:
            reasons.append("fresh data (<12h old)")
        elif data_freshness <= 24:
            reasons.append("day-old data")
        else:
            reasons.append("stale data (investigate freshness)")

        # Convergence
        if convergence >= 0.75:
            reasons.append(f"strong indicator convergence ({convergence*100:.0f}%)")
        elif convergence >= 0.5:
            reasons.append(f"moderate indicator convergence ({convergence*100:.0f}%)")
        else:
            reasons.append(f"weak indicator convergence ({convergence*100:.0f}%)")

        reason_text = ", ".join(reasons)
        return f"Confidence calibrated to {final_confidence} based on: {reason_text}."

    # Public test method for unit testing
    def calibrate_confidence(self, forecast_days: int, data_timestamp: datetime) -> str:
        """
        Simple confidence calibration based on forecast horizon and data age.
        Used for unit testing.
        """
        # Calculate data age in hours
        data_age_hours = (datetime.now() - data_timestamp).total_seconds() / 3600

        # Time-based confidence limits
        if forecast_days <= 7 and data_age_hours <= 12:
            return "HIGH"
        elif forecast_days <= 21 and data_age_hours <= 48:
            return "MEDIUM"
        else:
            return "LOW"