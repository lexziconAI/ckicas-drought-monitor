# Constitutional Yama Principles Validator
# Enforces Ahimsa, Satya, Asteya, Brahmacharya, Aparigraha in drought assessments

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class YamaValidator:
    """
    Enforces the 5 Yama constitutional principles in drought assessments.

    Yama Principles (MANDATORY):
    1. AHIMSA: Never issue HIGH confidence drought alerts without 3+ converging indicators
    2. SATYA: Mark all confidence levels explicitly with time-based degradation
    3. ASTEYA: Cite every data source with timestamp and freshness
    4. BRAHMACHARYA: Don't re-fetch if cached data <12h old AND indicators changed <5%
    5. APARIGRAHA: All drought-critical data freely accessible via public API
    """

    def __init__(self):
        self.violations: List[Dict] = []

    async def validate(self, assessment: Dict) -> Dict:
        """
        Apply all 5 Yama principles in sequence.
        Returns assessment with modifications if violations detected.
        """
        assessment = self._enforce_ahimsa(assessment)
        assessment = self._enforce_satya(assessment)
        assessment = self._enforce_asteya(assessment)
        # Brahmacharya enforced at cache layer (not here)
        # Aparigraha enforced at API auth layer (not here)

        if self.violations:
            assessment['constitutional_violations'] = self.violations
            logger.warning(f"Constitutional violations detected: {len(self.violations)}")

        return assessment

    def _enforce_ahimsa(self, assessment: Dict) -> Dict:
        """
        AHIMSA: Never allow HIGH confidence without 3+ converging indicators

        Rule: Single extreme indicator (e.g., SPI -2.5 alone) = MEDIUM confidence maximum
        HIGH confidence requires: (SPI_30 < -1.5 AND SMD < -110 AND SMA < -30) OR (SPI_60 < -1.5 AND SMD < -110)
        """
        indicators = assessment.get('indicators', {})
        current_confidence = assessment.get('confidence', 'LOW')

        # Calculate convergence score (0.0 to 1.0)
        convergence = self._calculate_convergence(indicators)

        # Ahimsa enforcement
        if convergence < 0.75:  # Less than 3/4 indicators agree
            if current_confidence == 'HIGH':
                self.violations.append({
                    'yama': 'ahimsa',
                    'rule': 'HIGH confidence requires 75%+ indicator convergence',
                    'action': 'downgraded to MEDIUM',
                    'convergence_score': convergence
                })
                assessment['confidence'] = 'MEDIUM'
                assessment['confidence_reason'] = (
                    f"Only {convergence*100:.0f}% of indicators converge. "
                    f"HIGH confidence requires ≥75% convergence to avoid false alarms (Ahimsa)."
                )

        # Add transparency about what would change this assessment
        assessment['threshold_distances'] = {
            'to_high_confidence': self._calculate_threshold_distance(indicators, 'HIGH'),
            'to_drought_declaration': self._calculate_threshold_distance(indicators, 'DROUGHT')
        }

        return assessment

    def _enforce_satya(self, assessment: Dict) -> Dict:
        """
        SATYA: Ensure confidence level properly calibrated by time horizon

        Confidence Scale:
        - HIGH: 0-7 days (observed data + verified forecasts)
        - MEDIUM: 8-21 days (model forecasts, ±20% variance)
        - LOW: 22+ days (directional trends only, ±40% variance)
        """
        forecast_days = assessment.get('forecast_14day', {}).get('days', 0)
        current_confidence = assessment.get('confidence', 'LOW')

        # Time-based confidence degradation
        if forecast_days > 21:
            if current_confidence in ['HIGH', 'MEDIUM']:
                self.violations.append({
                    'yama': 'satya',
                    'rule': 'Confidence must be LOW for forecasts >21 days',
                    'action': 'downgraded to LOW',
                    'forecast_days': forecast_days
                })
                assessment['confidence'] = 'LOW'
        elif forecast_days > 7:
            if current_confidence == 'HIGH':
                assessment['confidence'] = 'MEDIUM'

        # Add confidence intervals to all forecasts (Satya transparency)
        if 'forecast_14day' in assessment:
            assessment['forecast_14day']['confidence_interval'] = (
                self._calculate_confidence_interval(
                    assessment['forecast_14day'],
                    assessment['confidence']
                )
            )

        return assessment

    def _enforce_asteya(self, assessment: Dict) -> Dict:
        """
        ASTEYA: Ensure all data sources properly attributed

        Every metric must reference a data source with timestamp and freshness
        """
        if 'sources' not in assessment or len(assessment['sources']) == 0:
            raise ValueError(
                "Asteya violation: No data sources provided. "
                "All assessments must cite sources."
            )

        # Verify each source has required fields
        required_fields = ['provider', 'timestamp', 'freshness_hours']
        for source in assessment['sources']:
            missing = [f for f in required_fields if f not in source]
            if missing:
                raise ValueError(
                    f"Asteya violation: Source {source.get('provider')} "
                    f"missing required fields: {missing}"
                )

            # Verify freshness (should be reasonable for production data)
            freshness = source.get('freshness_hours', 999)
            if freshness > 48:  # More than 2 days old
                logger.warning(f"Stale data source: {source['provider']} is {freshness}h old")

        return assessment

    def _calculate_convergence(self, indicators: Dict) -> float:
        """
        Calculate indicator convergence score for Ahimsa enforcement
        Returns 0.0-1.0, where 1.0 = all indicators agree on drought severity
        """
        drought_votes = 0
        total_indicators = 0

        # SPI 30-day (key drought indicator)
        if indicators.get('spi_30day', 0) < -1.5:
            drought_votes += 1
        total_indicators += 1

        # SPI 60-day (longer-term trend)
        if indicators.get('spi_60day', 0) < -1.5:
            drought_votes += 1
        total_indicators += 1

        # SMD current (soil moisture deficit)
        if indicators.get('smd_current', 0) < -110 and indicators.get('smd_anomaly', 0) < -30:
            drought_votes += 1
        total_indicators += 1

        # NZDI category (composite drought index)
        if indicators.get('nzdi_category') in ['DROUGHT', 'SEVERE_DROUGHT']:
            drought_votes += 1
        total_indicators += 1

        return drought_votes / max(total_indicators, 1)

    def _calculate_threshold_distance(self, indicators: Dict, target: str) -> List[Dict]:
        """
        Calculate how close indicators are to critical thresholds
        Provides transparency for "what would change this assessment"
        """
        distances = []

        if target == 'HIGH':
            # Distance to HIGH confidence (3+ converging indicators)
            spi_30_dist = max(0, -1.5 - indicators.get('spi_30day', 0))
            if spi_30_dist > 0:
                distances.append({
                    'parameter': 'spi_30day',
                    'current_value': indicators.get('spi_30day', 0),
                    'threshold_value': -1.5,
                    'distance': spi_30_dist,
                    'description': f"SPI 30-day needs to drop {spi_30_dist:.1f} more points"
                })

        elif target == 'DROUGHT':
            # Distance to drought declaration
            smd_dist = max(0, -110 - indicators.get('smd_current', 0))
            if smd_dist > 0:
                distances.append({
                    'parameter': 'smd_current',
                    'current_value': indicators.get('smd_current', 0),
                    'threshold_value': -110,
                    'distance': smd_dist,
                    'description': f"Soil moisture deficit needs {smd_dist:.0f}mm more depletion"
                })

        return distances

    def _calculate_confidence_interval(self, forecast: Dict, confidence: str) -> Dict:
        """
        Calculate confidence intervals based on Satya time-based degradation
        """
        base_value = forecast.get('projected_smd', 0)

        if confidence == 'HIGH':
            variance = 0.10  # ±10% for HIGH confidence (0-7 days)
        elif confidence == 'MEDIUM':
            variance = 0.20  # ±20% for MEDIUM confidence (8-21 days)
        else:  # LOW
            variance = 0.40  # ±40% for LOW confidence (22+ days)

        return {
            'lower': base_value * (1 - variance),
            'upper': base_value * (1 + variance),
            'variance_percent': variance * 100,
            'confidence_level': confidence
        }

    # Public test methods for unit testing
    def validate_ahimsa(self, indicators: Dict, requested_confidence: str) -> Dict:
        """Public method for testing Ahimsa principle"""
        assessment = {'indicators': indicators, 'confidence': requested_confidence}
        result = self._enforce_ahimsa(assessment)
        return {
            'allowed': result['confidence'] == requested_confidence,
            'reason': result.get('confidence_reason', 'No reason provided')
        }

    def validate_asteya(self, sources: List[Dict]) -> Dict:
        """Public method for testing Asteya principle"""
        assessment = {'sources': sources}
        result = self._enforce_asteya(assessment)
        return {
            'compliant': len(result.get('constitutional_violations', [])) == 0,
            'warnings': [v.get('warning', '') for v in result.get('constitutional_violations', []) if 'warning' in v]
        }

    def validate_brahmacharya(self, cache_info: Dict) -> Dict:
        """Public method for testing Brahmacharya principle"""
        # Brahmacharya is enforced at the caching layer
        age_hours = cache_info.get('age_hours', 0)
        change_percent = cache_info.get('indicator_change_percent', 0)

        should_refetch = age_hours > 12 or change_percent > 5

        return {
            'should_refetch': should_refetch,
            'reason': f"Data age: {age_hours}h, change: {change_percent}%"
        }

    def validate_aparigraha(self, endpoint: str) -> Dict:
        """Public method for testing Aparigraha principle"""
        public_endpoints = [
            '/api/public/drought-risk',
            '/api/public/regions',
            '/api/public/historical-analogs'
        ]

        is_public = endpoint in public_endpoints
        return {
            'is_public': is_public,
            'reason': 'Endpoint is publicly accessible' if is_public else 'Endpoint requires authentication'
        }

    def validate_aparigraha_rate_limit(self, rate_limit: int) -> Dict:
        """Public method for testing Aparigraha rate limits"""
        # Farmers should have generous access (1000+ requests/day)
        is_generous = rate_limit >= 1000
        return {
            'is_generous': is_generous,
            'reason': f'Rate limit of {rate_limit} requests/day is {"generous" if is_generous else "restrictive"}'
        }

    def validate_full_assessment(self, assessment: Dict) -> Dict:
        """Public method for testing full constitutional compliance"""
        import asyncio
        result = asyncio.run(self.validate(assessment))

        violations = result.get('constitutional_violations', [])
        principles_status = {}

        # Check each principle
        for violation in violations:
            principle = violation.get('principle', 'unknown')
            principles_status[principle] = {'compliant': False, 'reason': violation.get('message', '')}

        # If no violations for a principle, mark as compliant
        all_principles = ['ahimsa', 'satya', 'asteya', 'brahmacharya', 'aparigraha']
        for principle in all_principles:
            if principle not in principles_status:
                principles_status[principle] = {'compliant': True, 'reason': 'No violations detected'}

        return principles_status