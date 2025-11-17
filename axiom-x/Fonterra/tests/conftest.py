"""
Pytest configuration and shared fixtures.
"""
import pytest
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from unittest.mock import AsyncMock
from app.agents.orchestrator import DroughtOrchestrator


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_orchestrator():
    """Create a mocked orchestrator for testing"""
    orchestrator = DroughtOrchestrator()

    # Mock all agents
    orchestrator.niwa_agent = AsyncMock()
    orchestrator.calculator_agent = AsyncMock()
    orchestrator.regional_council_agent = AsyncMock()
    orchestrator.openweather_agent = AsyncMock()
    orchestrator.forecast_agent = AsyncMock()

    # Set up default return values
    orchestrator.niwa_agent.fetch_data.return_value = {
        "rainfall": [10, 15, 5, 20],
        "temperature": [22, 25, 20, 24]
    }
    orchestrator.calculator_agent.calculate_indicators.return_value = {
        "spi_30day": -1.2,
        "spi_60day": -0.8,
        "smd_current": -75,
        "smd_anomaly": -15,
        "nzdi_category": "DRY"
    }
    orchestrator.regional_council_agent.fetch_data.return_value = {
        "soil_moisture": 0.35
    }
    orchestrator.openweather_agent.fetch_forecast.return_value = {
        "rain_probability": 0.25,
        "temperature_forecast": [24, 26, 22, 25]
    }
    orchestrator.forecast_agent.generate_forecast.return_value = {
        "projected_smd": -85,
        "confidence": "MEDIUM",
        "confidence_interval": {"lower": -95, "upper": -75}
    }

    return orchestrator


@pytest.fixture
def sample_location():
    """Sample location data for testing"""
    return {
        "lat": -37.7870,  # Hamilton, NZ
        "lon": 175.2793,
        "region": "Waikato"
    }


@pytest.fixture
def sample_indicators():
    """Sample drought indicators for testing"""
    return {
        "spi_30day": -1.5,
        "spi_60day": -1.2,
        "smd_current": -110,
        "smd_anomaly": -30,
        "nzdi_category": "DROUGHT"
    }


@pytest.fixture
def sample_sources():
    """Sample data sources for testing"""
    return [
        {
            "provider": "NIWA_DataHub",
            "dataset": "CliFlo_Station_2112",
            "timestamp": "2024-11-16T06:00:00Z",
            "freshness_hours": 8,
            "parameters": ["rainfall_daily", "temperature_max"]
        },
        {
            "provider": "Waikato_Regional_Council",
            "dataset": "Soil_Moisture_Sensors",
            "timestamp": "2024-11-16T05:30:00Z",
            "freshness_hours": 9,
            "parameters": ["soil_moisture_150mm"]
        }
    ]