"""
OpenWeather Agent - Fetches weather forecast data from OpenWeatherMap API
Implements real API integration for current conditions and multi-day forecasts
"""
import httpx
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class OpenWeatherAgent:
    """
    Agent for fetching weather data from OpenWeatherMap API.
    Provides current conditions and multi-day forecasts for drought modeling.
    """

    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geocoding_url = "https://api.openweathermap.org/geo/1.0"

        if not self.api_key:
            logger.warning("OPENWEATHER_API_KEY not set - using mock data")

    async def fetch_current_conditions(self, lat: float, lon: float) -> Dict:
        """
        Fetch current weather conditions from OpenWeatherMap

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Current weather data with temperature, humidity, wind, etc.
        """
        try:
            if not self.api_key:
                return self._mock_current_conditions(lat, lon)

            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'  # Celsius, m/s, etc.
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()

                data = response.json()

                return {
                    "provider": "OpenWeatherMap",
                    "dataset": "Current_Conditions",
                    "temperature": data['main']['temp'],
                    "humidity": data['main']['humidity'],
                    "wind_speed": data['wind']['speed'],
                    "wind_direction": data['wind'].get('deg', 0),
                    "pressure": data['main']['pressure'],
                    "visibility": data.get('visibility', 10000),
                    "cloud_cover": data['clouds']['all'],
                    "weather_description": data['weather'][0]['description'],
                    "timestamp": datetime.fromtimestamp(data['dt']).isoformat() + 'Z',
                    "freshness_hours": 0.0,  # Current data
                    "coordinates": {
                        "lat": data['coord']['lat'],
                        "lon": data['coord']['lon']
                    }
                }

        except Exception as e:
            logger.error(f"Failed to fetch current weather: {e}")
            return self._mock_current_conditions(lat, lon)

    async def fetch_forecast(self, lat: float, lon: float, days: int = 14) -> Dict:
        """
        Fetch multi-day weather forecast from OpenWeatherMap

        Args:
            lat: Latitude
            lon: Longitude
            days: Number of forecast days (max 16 for free tier)

        Returns:
            Daily forecast data with temperature, precipitation probability, etc.
        """
        try:
            if not self.api_key:
                return self._mock_forecast(lat, lon, days)

            # Use 5-day/3-hour forecast API (free tier)
            url = f"{self.base_url}/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()

                data = response.json()

                # Process 3-hourly data into daily aggregates
                daily_forecast = self._aggregate_daily_forecast(data['list'], days)

                return {
                    "provider": "OpenWeatherMap",
                    "dataset": "5Day_3Hourly_Forecast",
                    "forecast_days": min(days, 5),  # Free tier limit
                    "daily_forecast": daily_forecast,
                    "timestamp": datetime.fromtimestamp(data['list'][0]['dt']).isoformat() + 'Z',
                    "freshness_hours": 0.0,
                    "coordinates": {
                        "lat": data['city']['coord']['lat'],
                        "lon": data['city']['coord']['lon']
                    }
                }

        except Exception as e:
            logger.error(f"Failed to fetch forecast: {e}")
            return self._mock_forecast(lat, lon, days)

    def _aggregate_daily_forecast(self, forecast_list: List[Dict], days: int) -> List[Dict]:
        """
        Aggregate 3-hourly forecast data into daily summaries
        """
        daily_data = {}
        now = datetime.utcnow()

        for item in forecast_list:
            dt = datetime.fromtimestamp(item['dt'])
            date_key = dt.date()

            # Only process future days
            if dt <= now:
                continue

            # Limit to requested days
            if (dt.date() - now.date()).days >= days:
                continue

            if date_key not in daily_data:
                daily_data[date_key] = {
                    'date': date_key.isoformat(),
                    'temp_max': item['main']['temp_max'],
                    'temp_min': item['main']['temp_min'],
                    'temp_avg': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed'],
                    'rain_probability': 0.0,
                    'precipitation_mm': 0.0,
                    'weather_descriptions': [],
                    'count': 1
                }
            else:
                day = daily_data[date_key]
                day['temp_max'] = max(day['temp_max'], item['main']['temp_max'])
                day['temp_min'] = min(day['temp_min'], item['main']['temp_min'])
                day['temp_avg'] = (day['temp_avg'] * day['count'] + item['main']['temp']) / (day['count'] + 1)
                day['humidity'] = (day['humidity'] * day['count'] + item['main']['humidity']) / (day['count'] + 1)
                day['wind_speed'] = (day['wind_speed'] * day['count'] + item['wind']['speed']) / (day['count'] + 1)
                day['count'] += 1

            # Add precipitation if available
            if 'rain' in item and '3h' in item['rain']:
                daily_data[date_key]['precipitation_mm'] += item['rain']['3h']
                daily_data[date_key]['rain_probability'] = min(1.0, daily_data[date_key]['rain_probability'] + 0.2)

            # Collect weather descriptions
            if item['weather'][0]['description'] not in daily_data[date_key]['weather_descriptions']:
                daily_data[date_key]['weather_descriptions'].append(item['weather'][0]['description'])

        # Convert to list and sort by date
        result = []
        for date_key in sorted(daily_data.keys()):
            day = daily_data[date_key]
            day['weather_main'] = day['weather_descriptions'][0] if day['weather_descriptions'] else 'clear'
            del day['count']
            result.append(day)

        return result

    def _mock_current_conditions(self, lat: float, lon: float) -> Dict:
        """
        Return mock current weather data when API is unavailable
        """
        logger.info(f"Using mock current weather data for {lat}, {lon}")

        return {
            "provider": "OpenWeatherMap_Mock",
            "dataset": "Current_Conditions",
            "temperature": 18.5,
            "humidity": 72,
            "wind_speed": 8.5,
            "wind_direction": 225,
            "pressure": 1013,
            "visibility": 15000,
            "cloud_cover": 45,
            "weather_description": "partly cloudy",
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "freshness_hours": 0.0,
            "coordinates": {"lat": lat, "lon": lon}
        }

    def _mock_forecast(self, lat: float, lon: float, days: int) -> Dict:
        """
        Return mock forecast data when API is unavailable
        """
        logger.info(f"Using mock forecast data for {lat}, {lon}")

        daily_forecast = []
        base_date = datetime.utcnow().date()

        for i in range(min(days, 5)):
            date = base_date + timedelta(days=i+1)
            daily_forecast.append({
                'date': date.isoformat(),
                'temp_max': 22 + i % 3,
                'temp_min': 12 + i % 2,
                'temp_avg': 17 + i % 2,
                'humidity': 65 + i * 2,
                'wind_speed': 10 + i % 5,
                'rain_probability': 0.2 + (i % 3) * 0.1,
                'precipitation_mm': (i % 2) * 5.0,
                'weather_main': ['rain', 'cloudy', 'sunny'][i % 3],
                'weather_descriptions': [['light rain'], ['overcast clouds'], ['clear sky']][i % 3]
            })

        return {
            "provider": "OpenWeatherMap_Mock",
            "dataset": "5Day_Forecast_Mock",
            "forecast_days": len(daily_forecast),
            "daily_forecast": daily_forecast,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "freshness_hours": 0.0,
            "coordinates": {"lat": lat, "lon": lon}
        }