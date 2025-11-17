import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class WeatherAPIClient:
    """Base class for weather API clients"""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()

    def check_health(self) -> Tuple[bool, float]:
        """Check API health and response time"""
        try:
            start_time = datetime.utcnow()
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            response_time = (datetime.utcnow() - start_time).total_seconds()
            return response.status_code == 200, response_time
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False, 0.0

class NIWAClient(WeatherAPIClient):
    """NIWA CliFlo API client"""

    def __init__(self, api_key: str):
        super().__init__(api_key, "https://cliflo.niwa.co.nz")
        self.api_key = api_key

    def get_drought_risk(self, lat: float, lon: float, forecast_days: int = 14) -> Dict:
        """Get drought risk assessment"""
        try:
            # Mock implementation for testing
            return {
                'risk_score': 35,
                'confidence': 0.8,
                'factors': ['rainfall_deficit', 'soil_moisture_low'],
                'forecast_days': forecast_days,
                'location': {'lat': lat, 'lon': lon},
                'data_source': 'NIWA_CliFlo'
            }
        except Exception as e:
            logger.error(f"NIWA API error: {e}")
            return {
                'risk_score': 50,
                'confidence': 0.2,
                'factors': ['api_error'],
                'error': str(e)
            }

class OpenWeatherClient(WeatherAPIClient):
    """OpenWeather API client"""

    def __init__(self, api_key: str):
        super().__init__(api_key, "https://api.openweathermap.org/data/2.5")
        self.api_key = api_key

    def get_weather_data(self, lat: float, lon: float) -> Dict:
        """Get current weather data"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OpenWeather API error: {e}")
            return {'error': str(e)}

# Global client instances
_niwa_client = None
_openweather_client = None

def get_niwa_client() -> Optional[NIWAClient]:
    """Get NIWA client instance"""
    global _niwa_client
    api_key = os.getenv('NIWA_API_KEY')
    if api_key and not _niwa_client:
        _niwa_client = NIWAClient(api_key)
    return _niwa_client

def get_openweather_client() -> Optional[OpenWeatherClient]:
    """Get OpenWeather client instance"""
    global _openweather_client
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if api_key and not _openweather_client:
        _openweather_client = OpenWeatherClient(api_key)
    return _openweather_client

def get_api_status() -> Dict:
    """Get status of all weather APIs"""
    status = {}

    # Check NIWA
    niwa = get_niwa_client()
    if niwa:
        healthy, response_time = niwa.check_health()
        status['niwa'] = {
            'status': 'healthy' if healthy else 'unhealthy',
            'response_time': round(response_time, 3)
        }
    else:
        status['niwa'] = {
            'status': 'not_configured',
            'response_time': 0
        }

    # Check OpenWeather
    ow = get_openweather_client()
    if ow:
        healthy, response_time = ow.check_health()
        status['openweather'] = {
            'status': 'healthy' if healthy else 'unhealthy',
            'response_time': round(response_time, 3)
        }
    else:
        status['openweather'] = {
            'status': 'not_configured',
            'response_time': 0
        }

    return status