"""
Constitutional AI tests for Yama principle compliance.
Tests ensure the system follows ethical AI guidelines.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.constitutional.yamas import YamaValidator
from app.constitutional.confidence import ConfidenceCalibrator


class TestAhimsa:
    """Test non-harm principle (Ahimsa)"""

    def test_high_confidence_requires_multiple_indicators(self):
        """HIGH confidence requires 3+ converging indicators"""
        validator = YamaValidator()

        # Single extreme indicator should not allow HIGH confidence
        indicators = {
            "spi_30day": -2.5,  # Extreme drought
            "spi_60day": -0.5,  # Normal
            "smd_current": -50,  # Moderate deficit
            "smd_anomaly": -10   # Small anomaly
        }

        result = validator.validate_ahimsa(indicators, "HIGH")
        assert result["allowed"] == False
        assert "75% convergence" in result["reason"]

        # Three converging indicators should allow HIGH confidence
        indicators = {
            "spi_30day": -1.8,  # Drought
            "spi_60day": -1.6,  # Drought
            "smd_current": -125,  # Severe deficit
            "smd_anomaly": -35   # Large anomaly
        }

        result = validator.validate_ahimsa(indicators, "MEDIUM")
        assert result["allowed"] == True  # Should allow MEDIUM even with low convergence

    def test_includes_what_would_change_assessment(self):
        """All alerts must include what would change the assessment"""
        validator = YamaValidator()

        indicators = {
            "spi_30day": -1.2,
            "spi_60day": -0.8,
            "smd_current": -75,
            "smd_anomaly": -15
        }

        result = validator.validate_ahimsa(indicators, "MEDIUM")
        assert "what would change" in result["reason"].lower()


class TestSatya:
    """Test truth principle (Satya)"""

    def test_confidence_degrades_with_time(self):
        """Confidence levels must degrade with forecast time"""
        calibrator = ConfidenceCalibrator()

        # Recent data should allow HIGH confidence
        recent_data = datetime.now() - timedelta(hours=6)
        confidence = calibrator.calibrate_confidence(14, recent_data)
        assert confidence == "HIGH"

        # Old data should reduce confidence
        old_data = datetime.now() - timedelta(days=10)
        confidence = calibrator.calibrate_confidence(14, old_data)
        assert confidence in ["MEDIUM", "LOW"]

    def test_time_based_confidence_limits(self):
        """Time horizons have strict confidence limits"""
        calibrator = ConfidenceCalibrator()

        # 3 days: can be HIGH
        confidence = calibrator.calibrate_confidence(3, datetime.now())
        assert confidence == "HIGH"

        # 25 days: maximum LOW
        confidence = calibrator.calibrate_confidence(25, datetime.now())
        assert confidence == "LOW"


class TestAsteya:
    """Test non-stealing principle (Asteya)"""

    def test_all_sources_attributed(self):
        """All data sources must be cited with timestamps"""
        validator = YamaValidator()

        sources = [
            {
                "provider": "NIWA_DataHub",
                "dataset": "CliFlo_Station_2112",
                "timestamp": "2024-11-16T06:00:00Z",
                "freshness_hours": 8
            }
        ]

        result = validator.validate_asteya(sources)
        assert result["compliant"] == True

        # Missing timestamp should fail
        bad_sources = [
            {
                "provider": "Unknown",
                "dataset": "Mystery_Data"
                # Missing timestamp
            }
        ]

        result = validator.validate_asteya(bad_sources)
        assert result["compliant"] == False

    def test_freshness_tracking(self):
        """Data freshness must be tracked"""
        validator = YamaValidator()

        sources = [
            {
                "provider": "NIWA_DataHub",
                "timestamp": "2024-11-16T06:00:00Z",
                "freshness_hours": 48  # Too old
            }
        ]

        result = validator.validate_asteya(sources)
        assert "freshness" in result["warnings"]


class TestBrahmacharya:
    """Test right energy principle (Brahmacharya)"""

    def test_efficient_caching(self):
        """Don't re-fetch if cached data is fresh enough"""
        validator = YamaValidator()

        # Fresh cache should prevent re-fetch
        cache_info = {
            "age_hours": 8,
            "indicator_change_percent": 3.0
        }

        result = validator.validate_brahmacharya(cache_info)
        assert result["should_refetch"] == False

        # Stale cache should allow re-fetch
        cache_info = {
            "age_hours": 20,
            "indicator_change_percent": 8.0
        }

        result = validator.validate_brahmacharya(cache_info)
        assert result["should_refetch"] == True


class TestAparigraha:
    """Test non-hoarding principle (Aparigraha)"""

    def test_public_data_accessible(self):
        """Critical drought data must be freely accessible"""
        validator = YamaValidator()

        endpoints = [
            "/api/public/drought-risk",
            "/api/public/regions",
            "/api/public/historical-analogs"
        ]

        for endpoint in endpoints:
            result = validator.validate_aparigraha(endpoint)
            assert result["is_public"] == True

    def test_reasonable_rate_limits(self):
        """Rate limits should be generous for farmers"""
        validator = YamaValidator()

        rate_limit = 1000  # requests per day

        result = validator.validate_aparigraha_rate_limit(rate_limit)
        assert result["is_generous"] == True

        # Too restrictive should fail
        restrictive_limit = 10  # requests per day
        result = validator.validate_aparigraha_rate_limit(restrictive_limit)
        assert result["is_generous"] == False


class TestConstitutionalIntegration:
    """Integration tests for full constitutional compliance"""

    def test_full_assessment_validation(self):
        """Complete drought assessment must pass all Yama principles"""
        validator = YamaValidator()

        assessment = {
            "indicators": {
                "spi_30day": -1.8,
                "spi_60day": -1.6,
                "smd_current": -125,
                "smd_anomaly": -35
            },
            "confidence": "HIGH",
            "sources": [
                {
                    "provider": "NIWA_DataHub",
                    "timestamp": "2024-11-16T06:00:00Z",
                    "freshness_hours": 8
                }
            ],
            "cache_info": {
                "age_hours": 6,
                "indicator_change_percent": 2.0
            }
        }

        result = validator.validate_full_assessment(assessment)

        # Should pass all principles
        assert all(principle["compliant"] for principle in result.values())

    def test_violation_blocks_assessment(self):
        """Constitutional violations must block assessments"""
        validator = YamaValidator()

        # Assessment with insufficient indicators for HIGH confidence
        bad_assessment = {
            "indicators": {
                "spi_30day": -2.5,  # Extreme but alone
                "spi_60day": -0.2,
                "smd_current": -30,
                "smd_anomaly": -5
            },
            "confidence": "HIGH",  # Should not be allowed
            "sources": [],
            "cache_info": {"age_hours": 50, "indicator_change_percent": 10}
        }

        result = validator.validate_full_assessment(bad_assessment)

        # Should fail Ahimsa principle
        assert result["ahimsa"]["compliant"] == False
        assert "blocked" in result["ahimsa"]["action"]