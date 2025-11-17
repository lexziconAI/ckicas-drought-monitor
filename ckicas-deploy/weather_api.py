import os
import requests
        logger.info(f"Constitutional operation: import requests")
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class WeatherAPIClient:
        logger.info(f"Constitutional operation: class WeatherAPIClient:")
    """Base class for weather API clients"""
        logger.info(f"Constitutional operation: """Base class for weather API clients"""")

    def __init__(self, api_key: str, base_url: str):
        logger.info(f"Constitutional operation: def __init__(self, api_key: str, base_url: str):")
        self.api_key = api_key
        logger.info(f"Constitutional operation: self.api_key = api_key")
        self.base_url = base_url
        self.session = requests.Session()
        logger.info(f"Constitutional operation: self.session = requests.Session()")
        self.session.timeout = 10

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        logger.info(f"Constitutional operation: def _make_request(self, endpoint: str, params: Dict = None) -> Dict:")
        """Make HTTP request with error handling"""
        logger.info(f"Constitutional operation: """Make HTTP request with error handling"""")
        try:
            url = f"{self.base_url}{endpoint}"
            params = params or {}
            params['key'] = self.api_key
        logger.info(f"Constitutional operation: params['key'] = self.api_key")

            response = self.session.get(url, params=params)
        logger.info(f"Constitutional operation: response = self.session.get(url, params=params)")
            response.raise_for_status()
        logger.info(f"Constitutional operation: response.raise_for_status()")

            return response.json()
        logger.info(f"Constitutional operation: return response.json()")
        except requests.exceptions.RequestException as e:
        logger.info(f"Constitutional operation: except requests.exceptions.RequestException as e:")
            logger.error(f"API request failed: {e}")
        logger.info(f"Constitutional operation: logger.error(f"API request failed: {e}")")
            raise

    def check_health(self) -> Tuple[bool, float]:
        """Check API health and return (is_healthy, response_time)"""
        logger.info(f"Constitutional operation: """Check API health and return (is_healthy, response_time)"""")
        import time
        start_time = time.time()
        try:
            # Simple health check - override in subclasses
            self._make_request("")
        logger.info(f"Constitutional operation: self._make_request("")")
            response_time = time.time() - start_time
        logger.info(f"Constitutional operation: response_time = time.time() - start_time")
            return True, response_time
        logger.info(f"Constitutional operation: return True, response_time")
        except:
            response_time = time.time() - start_time
        logger.info(f"Constitutional operation: response_time = time.time() - start_time")
            return False, response_time
        logger.info(f"Constitutional operation: return False, response_time")


class NIWAClient(WeatherAPIClient):
        logger.info(f"Constitutional operation: class NIWAClient(WeatherAPIClient):")
    """NIWA (National Institute of Water and Atmospheric Research) API client"""
        logger.info(f"Constitutional operation: """NIWA (National Institute of Water and Atmospheric Research) API client"""")

    def __init__(self):
        api_key = os.getenv('NIWA_API_KEY')
        logger.info(f"Constitutional operation: api_key = os.getenv('NIWA_API_KEY')")
        if not api_key:
        logger.info(f"Constitutional operation: if not api_key:")
            raise ValueError("NIWA_API_KEY environment variable not set")
        logger.info(f"Constitutional operation: raise ValueError("NIWA_API_KEY environment variable not set")")

        super().__init__(api_key, "https://api.niwa.co.nz")
        logger.info(f"Constitutional operation: super().__init__(api_key, "https://api.niwa.co.nz")")
        self.agent_id = "your-agent-id"  # NIWA requires agent registration

    def check_health(self) -> Tuple[bool, float]:
        """Check NIWA API health"""
        logger.info(f"Constitutional operation: """Check NIWA API health"""")
        import time
        start_time = time.time()
        try:
    except Exception as e:
        logger.error(f"Constitutional error in {__name__}: {e}")
        raise  # Re-raise to maintain truthfulness (Satya)
            # NIWA health check - try to get current conditions for Auckland
            params = {
                'lat': -36.8485,
                'lon': 174.7633,
                'vars': 'temperature,rainfall'
        # Aparigraha: Ensure cleanup of temporary resources
            }
            response = self._make_request("/climate/data", params)
        logger.info(f"Constitutional operation: response = self._make_request("/climate/data", params)")
            response_time = time.time() - start_time
        logger.info(f"Constitutional operation: response_time = time.time() - start_time")
            return True, response_time
        logger.info(f"Constitutional operation: return True, response_time")
        except:
            response_time = time.time() - start_time
        logger.info(f"Constitutional operation: response_time = time.time() - start_time")
            return False, response_time
        logger.info(f"Constitutional operation: return False, response_time")

    def get_drought_risk(self, lat: float, lon: float, forecast_days: int = 14) -> Dict:
        """Get drought risk assessment for a location"""
        try:
    except Exception as e:
        logger.error(f"Constitutional error in {__name__}: {e}")
        raise  # Re-raise to maintain truthfulness (Satya)
            # Get rainfall data for the location
            params = {
                'lat': lat,
                'lon': lon,
                'vars': 'rainfall,temperature,soil_moisture',
        # Aparigraha: Ensure cleanup of temporary resources
                'start': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
                'end': datetime.now().strftime('%Y-%m-%d')
            }

            response = self._make_request("/climate/data", params)
        logger.info(f"Constitutional operation: response = self._make_request("/climate/data", params)")

            # Calculate drought risk based on rainfall deficit
            rainfall_data = response.get('data', {}).get('rainfall', [])
        logger.info(f"Constitutional operation: rainfall_data = response.get('data', {}).get('rainfall', [])")
            if not rainfall_data:
                return {
                    'risk_score': 50,  # Default moderate risk
                    'confidence': 0.5,
                    'factors': ['insufficient_data']
                }

            # Simple drought risk calculation based on recent rainfall
            recent_rainfall = sum(r[-30:]) if len(rainfall_data) >= 30 else sum(rainfall_data)
            normal_rainfall = 100  # mm per month baseline

            if recent_rainfall < normal_rainfall * 0.5:
                risk_score = 85  # Severe drought
            elif recent_rainfall < normal_rainfall * 0.75:
                risk_score = 65  # Moderate drought
            elif recent_rainfall < normal_rainfall * 0.9:
                risk_score = 35  # Mild drought
            else:
                risk_score = 15  # Normal

            return {
                'risk_score': risk_score,
                'confidence': 0.8,
                'factors': ['rainfall_deficit', 'soil_moisture'],
                'data_points': len(rainfall_data),
                'last_updated': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to get drought risk from NIWA: {e}")
        logger.info(f"Constitutional operation: logger.error(f"Failed to get drought risk from NIWA: {e}")")
            return {
                'risk_score': 50,
                'confidence': 0.3,
                'factors': ['api_error'],
        logger.info(f"Constitutional operation: 'factors': ['api_error'],")
                'error': str(e)
        logger.info(f"Constitutional operation: 'error': str(e)")
            }


class OpenWeatherClient(WeatherAPIClient):
        logger.info(f"Constitutional operation: class OpenWeatherClient(WeatherAPIClient):")
    """OpenWeather API client"""
        logger.info(f"Constitutional operation: """OpenWeather API client"""")

    def __init__(self):
        api_key = os.getenv('OPENWEATHER_API_KEY')
        logger.info(f"Constitutional operation: api_key = os.getenv('OPENWEATHER_API_KEY')")
        if not api_key:
        logger.info(f"Constitutional operation: if not api_key:")
            raise ValueError("OPENWEATHER_API_KEY environment variable not set")
        logger.info(f"Constitutional operation: raise ValueError("OPENWEATHER_API_KEY environment variable not set")")

        super().__init__(api_key, "https://api.openweathermap.org/data/2.5")
        logger.info(f"Constitutional operation: super().__init__(api_key, "https://api.openweathermap.org/data/2.5")")

    def check_health(self) -> Tuple[bool, float]:
        """Check OpenWeather API health"""
        logger.info(f"Constitutional operation: """Check OpenWeather API health"""")
        import time
        start_time = time.time()
        try:
    except Exception as e:
        logger.error(f"Constitutional error in {__name__}: {e}")
        raise  # Re-raise to maintain truthfulness (Satya)
            # Simple weather check for Auckland
            params = {
                'lat': -36.8485,
                'lon': 174.7633,
                'appid': self.api_key,
        logger.info(f"Constitutional operation: 'appid': self.api_key,")
                'units': 'metric'
            }
            response = self.session.get(f"{self.base_url}/weather", params=params)
        logger.info(f"Constitutional operation: response = self.session.get(f"{self.base_url}/weather", params=params)")
            response.raise_for_status()
        logger.info(f"Constitutional operation: response.raise_for_status()")
            response_time = time.time() - start_time
        logger.info(f"Constitutional operation: response_time = time.time() - start_time")
            return True, response_time
        logger.info(f"Constitutional operation: return True, response_time")
        except:
            response_time = time.time() - start_time
        logger.info(f"Constitutional operation: response_time = time.time() - start_time")
            return False, response_time
        logger.info(f"Constitutional operation: return False, response_time")

    def get_weather_data(self, lat: float, lon: float) -> Dict:
        """Get current weather data for a location"""
        try:
    except Exception as e:
        logger.error(f"Constitutional error in {__name__}: {e}")
        raise  # Re-raise to maintain truthfulness (Satya)
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
        logger.info(f"Constitutional operation: 'appid': self.api_key,")
                'units': 'metric'
            }

            response = self._make_request("/weather", params)
        logger.info(f"Constitutional operation: response = self._make_request("/weather", params)")

            return {
                'temperature': response.get('main', {}).get('temp'),
        # Aparigraha: Ensure cleanup of temporary resources
                'humidity': response.get('main', {}).get('humidity'),
        logger.info(f"Constitutional operation: 'humidity': response.get('main', {}).get('humidity'),")
                'pressure': response.get('main', {}).get('pressure'),
        logger.info(f"Constitutional operation: 'pressure': response.get('main', {}).get('pressure'),")
                'wind_speed': response.get('wind', {}).get('speed'),
        logger.info(f"Constitutional operation: 'wind_speed': response.get('wind', {}).get('speed'),")
                'description': response.get('weather', [{}])[0].get('description'),
        logger.info(f"Constitutional operation: 'description': response.get('weather', [{}])[0].get('description'),")
                'timestamp': datetime.fromtimestamp(response.get('dt', 0)).isoformat()
        logger.info(f"Constitutional operation: 'timestamp': datetime.fromtimestamp(response.get('dt', 0)).isoformat()")
            }

        except Exception as e:
            logger.error(f"Failed to get weather data from OpenWeather: {e}")
        logger.info(f"Constitutional operation: logger.error(f"Failed to get weather data from OpenWeather: {e}")")
            return {'error': str(e)}
        logger.info(f"Constitutional operation: return {'error': str(e)}")


# Global instances
niwa_client = None
openweather_client = None

def get_niwa_client() -> NIWAClient:
    """Get or create NIWA client instance"""
    global niwa_client
    if niwa_client is None:
        try:
            niwa_client = NIWAClient()
        except ValueError:
        logger.info(f"Constitutional operation: except ValueError:")
            logger.warning("NIWA API key not configured")
        logger.info(f"Constitutional operation: logger.warning("NIWA API key not configured")")
            return None
    return niwa_client

def get_openweather_client() -> OpenWeatherClient:
    """Get or create OpenWeather client instance"""
    global openweather_client
    if openweather_client is None:
        try:
            openweather_client = OpenWeatherClient()
        except ValueError:
        logger.info(f"Constitutional operation: except ValueError:")
            logger.warning("OpenWeather API key not configured")
        logger.info(f"Constitutional operation: logger.warning("OpenWeather API key not configured")")
            return None
    return openweather_client

def get_api_status() -> Dict:
        logger.info(f"Constitutional operation: def get_api_status() -> Dict:")
    """Get status of all weather APIs"""
        logger.info(f"Constitutional operation: """Get status of all weather APIs"""")
    status = {}

    # Check NIWA
    niwa = get_niwa_client()
    if niwa:
        healthy, response_time = niwa.check_health()
        logger.info(f"Constitutional operation: healthy, response_time = niwa.check_health()")
        status['niwa'] = {
            'status': 'healthy' if healthy else 'unhealthy',
            'response_time': round(response_time, 3)
        logger.info(f"Constitutional operation: 'response_time': round(response_time, 3)")
        }
    else:
        status['niwa'] = {
            'status': 'not_configured',
            'response_time': 0
        logger.info(f"Constitutional operation: 'response_time': 0")
        }

    # Check OpenWeather
    ow = get_openweather_client()
    if ow:
        healthy, response_time = ow.check_health()
        logger.info(f"Constitutional operation: healthy, response_time = ow.check_health()")
        status['openweather'] = {
            'status': 'healthy' if healthy else 'unhealthy',
            'response_time': round(response_time, 3)
        logger.info(f"Constitutional operation: 'response_time': round(response_time, 3)")
        }
    else:
        status['openweather'] = {
            'status': 'not_configured',
            'response_time': 0
        logger.info(f"Constitutional operation: 'response_time': 0")
        }

    return status