"""
Agent functionality tests with constitutional compliance.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.agents.orchestrator import DroughtOrchestrator
from app.agents.niwa_agent import NIWADataAgent
from app.agents.calculator_agent import DroughtCalculatorAgent
from app.agents.weather_agent import OpenWeatherAgent
from app.agents.forecast_agent import ForecastAgent
from app.services.cache import BrahmacharyaCache


class TestDroughtOrchestrator:
    """Test the main orchestrator agent with Brahmacharya caching"""

    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator with mocked agents"""
        orchestrator = DroughtOrchestrator()

        # Mock all agents
        orchestrator.agents['niwa'] = AsyncMock()
        orchestrator.agents['councils'] = AsyncMock()
        orchestrator.agents['weather'] = AsyncMock()
        orchestrator.agents['calculator'] = AsyncMock()
        orchestrator.agents['forecast'] = AsyncMock()
        orchestrator.agents['validator'] = AsyncMock()

        # Mock calibrator
        orchestrator.calibrator = MagicMock()
        orchestrator.calibrator.calibrate_confidence.return_value = {
            'confidence': 'HIGH',
            'confidence_factors': {}
        }

        return orchestrator

    @pytest.mark.asyncio
    async def test_parallel_execution(self, orchestrator):
        """Test that agents execute in parallel"""
        # Setup mock returns
        orchestrator.agents['niwa'].fetch_90day_rainfall.return_value = {
            'data': [{'date': '2024-01-01', 'rainfall': 10.0}],
            'sources': []
        }
        orchestrator.agents['niwa'].fetch_90day_temperature.return_value = {
            'data': [{'date': '2024-01-01', 'temperature_max': 25.0}],
            'sources': []
        }
        orchestrator.agents['councils'].fetch_soil_moisture.return_value = {
            'soil_moisture': {'soil_moisture_150mm': 0.35}
        }
        orchestrator.agents['weather'].fetch_current_conditions.return_value = {
            'temperature': 22.0
        }
        orchestrator.agents['weather'].fetch_forecast.return_value = {
            'daily_forecast': [{'date': '2024-01-02', 'precipitation_mm': 5.0}]
        }
        orchestrator.agents['calculator'].calculate_spi.return_value = {'value': -1.2}
        orchestrator.agents['calculator'].calculate_smd.return_value = {
            'current': -75, 'anomaly': -15
        }
        orchestrator.agents['calculator'].calculate_nzdi.return_value = {
            'category': 'MODERATE_DROUGHT'
        }
        orchestrator.agents['calculator'].detect_anomalies.return_value = []
        orchestrator.agents['forecast'].project_soil_moisture.return_value = {
            'projected_smd': -85
        }
        orchestrator.agents['validator'].validate.return_value = {
            'indicators': {'spi_30day': -1.2},
            'sources': []
        }

        result = await orchestrator._compute_full_assessment(
            lat=-37.7, lon=175.2, region="Waikato", days_forecast=14
        )

        # Verify all agents were called
        orchestrator.agents['niwa'].fetch_90day_rainfall.assert_called_once()
        orchestrator.agents['calculator'].calculate_spi.assert_called()

        # Verify result structure
        assert "location" in result
        assert "indicators" in result
        assert "forecast_14day" in result

    @pytest.mark.asyncio
    async def test_brahmacharya_caching(self, orchestrator):
        """Test Brahmacharya caching prevents unnecessary API calls"""
        cache = BrahmacharyaCache()

        # First call should compute
        async def mock_compute():
            return {"test": "data", "sources": []}

        result1, cached1 = await cache.get_or_compute(
            "test_key", mock_compute, ttl_hours=1
        )
        assert cached1 == False  # First call not cached

        # Second call should use cache
        result2, cached2 = await cache.get_or_compute(
            "test_key", mock_compute, ttl_hours=1
        )
        assert cached2 == True  # Second call cached

        # Results should be identical
        assert result1 == result2

    @pytest.mark.asyncio
    async def test_error_handling(self, orchestrator):
        """Test graceful handling of agent failures"""
        # Make agents fail
        orchestrator.agents['niwa'].fetch_90day_rainfall.side_effect = Exception("API Error")
        orchestrator.agents['niwa'].fetch_90day_temperature.side_effect = Exception("API Error")
        orchestrator.agents['councils'].fetch_soil_moisture.return_value = {}
        orchestrator.agents['weather'].fetch_current_conditions.return_value = {}
        orchestrator.agents['weather'].fetch_forecast.return_value = {}
        orchestrator.agents['calculator'].calculate_spi.return_value = {'value': 0}
        orchestrator.agents['calculator'].calculate_smd.return_value = {'current': 0, 'anomaly': 0}
        orchestrator.agents['calculator'].calculate_nzdi.return_value = {'category': 'NORMAL'}
        orchestrator.agents['calculator'].detect_anomalies.return_value = []
        orchestrator.agents['forecast'].project_soil_moisture.return_value = {}
        orchestrator.agents['validator'].validate.return_value = {
            'indicators': {'spi_30day': 0},
            'sources': []
        }

        result = await orchestrator._compute_full_assessment(
            lat=-37.7, lon=175.2, region="Waikato"
        )

        # Should still return a result
        assert "location" in result
        assert "indicators" in result


class TestNIWAAgent:
    """Test NIWA data fetching agent"""

    @pytest.fixture
    def agent(self):
        """Create NIWA agent"""
        return NIWADataAgent()

    @pytest.mark.asyncio
    async def test_data_fetching(self, agent):
        """Test fetching data from NIWA"""
        # Mock the HTTP client
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "data": [
                    {"date": "2024-11-01", "RD": "10.5", "TMX": "25.2", "TMN": "15.1"},
                    {"date": "2024-11-02", "RD": "0.0", "TMX": "28.1", "TMN": "16.2"}
                ]
            }
            mock_response.raise_for_status.return_value = None
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            result = await agent._fetch_station_data("test_station", "rainfall,temperature", 30)

            assert len(result) > 0
            assert "date" in result[0]
            assert "rainfall" in result[0] or "temperature_max" in result[0]

    def test_data_validation(self, agent):
        """Test data quality validation"""
        # Valid data
        valid_data = {
            "data": [
                {"date": "2024-01-01", "rainfall": 10.0},
                {"date": "2024-01-02", "rainfall": 15.0}
            ],
            "sources": []
        }
        # NIWA agent doesn't have validate_data method, so we'll test parsing
        parsed = agent._parse_niwa_response({"data": valid_data["data"]}, "rainfall")
        assert len(parsed) == 2
        assert parsed[0]["rainfall"] == 10.0


class TestCalculatorAgent:
    """Test drought indicator calculations"""

    @pytest.fixture
    def agent(self):
        """Create calculator agent"""
        return DroughtCalculatorAgent()

    def test_spi_calculation(self, agent):
        """Test SPI calculation"""
        rainfall_data = {
            'data': [
                {'date': f'2024-01-{i:02d}', 'rainfall': 10 + (i % 5)} for i in range(1, 31)
            ]
        }

        spi_result = agent.calculate_spi(rainfall_data, period=30)

        assert isinstance(spi_result, dict)
        assert "value" in spi_result
        assert "period" in spi_result
        assert isinstance(spi_result["value"], (int, float))

    def test_smd_calculation(self, agent):
        """Test SMD calculation"""
        rainfall_data = {
            'data': [{'date': f'2024-01-{i:02d}', 'rainfall': 5.0} for i in range(1, 31)]
        }
        temperature_data = {
            'data': [{'date': f'2024-01-{i:02d}', 'temperature_max': 25.0, 'temperature_min': 15.0} for i in range(1, 31)]
        }

        smd_result = agent.calculate_smd(rainfall_data, temperature_data)

        assert isinstance(smd_result, dict)
        assert "current" in smd_result
        assert "anomaly" in smd_result
        assert isinstance(smd_result["current"], (int, float))

    def test_nzdi_calculation(self, agent):
        """Test NZDI calculation"""
        rainfall_data = {
            'data': [{'date': f'2024-01-{i:02d}', 'rainfall': 2.0} for i in range(1, 31)]
        }
        temperature_data = {
            'data': [{'date': f'2024-01-{i:02d}', 'temperature_max': 25.0, 'temperature_min': 15.0} for i in range(1, 31)]
        }

        nzdi_result = agent.calculate_nzdi(rainfall_data, temperature_data)

        assert isinstance(nzdi_result, dict)
        assert "value" in nzdi_result
        assert "category" in nzdi_result
        assert nzdi_result["category"] in [
            "NORMAL", "DRY", "VERY_DRY", "EXTREMELY_DRY",
            "DROUGHT", "SEVERE_DROUGHT"
        ]


class TestWeatherAgent:
    """Test OpenWeatherMap agent"""

    @pytest.fixture
    def agent(self):
        """Create weather agent"""
        return OpenWeatherAgent()

    @pytest.mark.asyncio
    async def test_forecast_aggregation(self, agent):
        """Test daily forecast aggregation"""
        mock_forecast_data = {
            "list": [
                {
                    "dt": 1638360000,  # 2024-11-01 12:00
                    "main": {"temp_max": 25.0, "temp_min": 15.0, "humidity": 70},
                    "wind": {"speed": 10.0},
                    "weather": [{"description": "clear sky"}],
                    "rain": {"3h": 0}
                },
                {
                    "dt": 1638370800,  # 2024-11-01 15:00
                    "main": {"temp_max": 26.0, "temp_min": 16.0, "humidity": 65},
                    "wind": {"speed": 12.0},
                    "weather": [{"description": "few clouds"}],
                    "rain": {"3h": 0}
                }
            ],
            "city": {"coord": {"lat": -37.7, "lon": 175.2}}
        }

        daily_forecast = agent._aggregate_daily_forecast(mock_forecast_data["list"], 5)

        assert len(daily_forecast) > 0
        assert "date" in daily_forecast[0]
        assert "temp_max" in daily_forecast[0]
        assert "precipitation_mm" in daily_forecast[0]


class TestForecastAgent:
    """Test forecast agent"""

    @pytest.fixture
    def agent(self):
        """Create forecast agent"""
        return ForecastAgent()

    @pytest.mark.asyncio
    async def test_soil_moisture_projection(self, agent):
        """Test soil moisture projection"""
        forecast_weather = {
            'daily_forecast': [
                {'date': '2024-01-02', 'precipitation_mm': 5.0, 'temp_max': 25.0, 'temp_min': 15.0, 'humidity': 70, 'wind_speed': 10.0},
                {'date': '2024-01-03', 'precipitation_mm': 0.0, 'temp_max': 28.0, 'temp_min': 18.0, 'humidity': 60, 'wind_speed': 8.0}
            ]
        }

        result = await agent.project_soil_moisture(
            current_smd=-50.0,
            forecast_weather=forecast_weather,
            days=2
        )

        assert isinstance(result, dict)
        assert "projected_smd" in result
        assert "confidence" in result
        assert "daily_projections" in result
        assert len(result["daily_projections"]) == 2