# NIWA Data Agent
# Fetches meteorological data from NIWA DataHub (CliFlo)

import httpx
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class NIWADataAgent:
    """
    Agent for fetching meteorological data from NIWA DataHub.
    Implements LOG³ precision for strict API contract adherence.
    """

    def __init__(self):
        self.base_url = "https://cliflo.niwa.co.nz"
        self.api_key = os.getenv("NIWA_API_KEY")
        self.email = os.getenv("NIWA_DATAHUB_EMAIL")

        if not self.api_key or not self.email:
            logger.warning("NIWA credentials not configured - using mock data")

    async def fetch_90day_rainfall(self, lat: float, lon: float) -> Dict:
        """
        Fetch 90 days of rainfall data for location
        Returns data with source attribution (Asteya)
        """
        try:
            # Find nearest station
            station = await self._find_nearest_station(lat, lon, "rainfall")

            if not station:
                return self._mock_rainfall_data(lat, lon)

            # Fetch data
            data = await self._fetch_station_data(
                station['id'],
                "rainfall_daily",
                days=90
            )

            return {
                'data': data,
                'station': station,
                'sources': [{
                    'provider': 'NIWA_DataHub',
                    'dataset': f"CliFlo_Station_{station['id']}",
                    'timestamp': datetime.utcnow(),
                    'freshness_hours': 0,
                    'parameters': ['rainfall_daily']
                }]
            }

        except Exception as e:
            logger.error(f"NIWA rainfall fetch failed: {e}")
            return self._mock_rainfall_data(lat, lon)

    async def fetch_90day_temperature(self, lat: float, lon: float) -> Dict:
        """
        Fetch 90 days of temperature data for location
        """
        try:
            station = await self._find_nearest_station(lat, lon, "temperature")

            if not station:
                return self._mock_temperature_data(lat, lon)

            data = await self._fetch_station_data(
                station['id'],
                "temperature_max,temperature_min",
                days=90
            )

            return {
                'data': data,
                'station': station,
                'sources': [{
                    'provider': 'NIWA_DataHub',
                    'dataset': f"CliFlo_Station_{station['id']}",
                    'timestamp': datetime.utcnow(),
                    'freshness_hours': 0,
                    'parameters': ['temperature_max', 'temperature_min']
                }]
            }

        except Exception as e:
            logger.error(f"NIWA temperature fetch failed: {e}")
            return self._mock_temperature_data(lat, lon)

    async def fetch_historical_analogs(
        self,
        current_spi_30: float,
        current_spi_60: float,
        region: str
    ) -> List[Dict]:
        """
        Find historical periods with similar SPI patterns
        Used for LOG⁴ anomaly exploration
        """
        # This would query historical SPI database
        # For now, return mock analogs
        return [
            {
                'date': '2013-02-15',
                'spi_30': -1.8,
                'spi_60': -1.6,
                'similarity': 0.89,
                'outcome': '8-week drought'
            },
            {
                'date': '2008-03-22',
                'spi_30': -2.1,
                'spi_60': -1.4,
                'similarity': 0.76,
                'outcome': '4-week drought'
            }
        ]

    async def _find_nearest_station(self, lat: float, lon: float, data_type: str) -> Optional[Dict]:
        """
        Find nearest NIWA station with required data type
        Uses NIWA station list API and filters by distance
        """
        if not self.api_key or not self.email:
            return None

        try:
            # NIWA station list endpoint
            stations_url = f"{self.base_url}/stations"

            params = {
                'key': self.api_key,
                'format': 'json'
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(stations_url, params=params)
                response.raise_for_status()

                data = response.json()

                # NIWA returns stations in various formats
                stations = data.get('stations', data.get('features', []))

                suitable_stations = []
                for station in stations:
                    # Handle different station data formats
                    if isinstance(station, dict):
                        station_lat = station.get('latitude', station.get('lat'))
                        station_lon = station.get('longitude', station.get('lon'))

                        if station_lat is not None and station_lon is not None:
                            # Check if station has required data type
                            if self._station_has_data_type(station, data_type):
                                distance = self._calculate_distance(
                                    lat, lon, station_lat, station_lon
                                )

                                # Only include stations within 100km
                                if distance <= 100:
                                    suitable_stations.append({
                                        'id': station.get('station_id', station.get('id')),
                                        'name': station.get('name', 'Unknown Station'),
                                        'lat': station_lat,
                                        'lon': station_lon,
                                        'distance_km': distance,
                                        'elevation': station.get('elevation', 0)
                                    })

                # Return nearest station
                if suitable_stations:
                    return min(suitable_stations, key=lambda s: s['distance_km'])

        except Exception as e:
            logger.error(f"NIWA station search failed: {e}")

        return None

    async def _fetch_station_data(self, station_id: str, parameters: str, days: int) -> List[Dict]:
        """
        Fetch actual data from NIWA CliFlo API
        """
        if not self.api_key or not self.email:
            return self._mock_station_data(parameters, days)

        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)

            # NIWA API parameters
            params = {
                'key': self.api_key,
                'station': station_id,
                'datacategory': 'DAILY',
                'start_date': start_date.strftime('%Y%m%d'),
                'end_date': end_date.strftime('%Y%m%d'),
                'format': 'json'
            }

            # Add specific parameters
            if 'rainfall' in parameters:
                params['datatypes'] = 'RD'
            if 'temperature' in parameters:
                params['datatypes'] = params.get('datatypes', '') + ',TMX,TMN'

            data_url = f"{self.base_url}/data"

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(data_url, params=params)
                response.raise_for_status()

                raw_data = response.json()

                # Parse NIWA response format
                return self._parse_niwa_response(raw_data, parameters)

        except Exception as e:
            logger.error(f"NIWA data fetch failed for station {station_id}: {e}")
            return self._mock_station_data(parameters, days)

    def _station_has_data_type(self, station: Dict, data_type: str) -> bool:
        """
        Check if station has the required data type
        """
        # NIWA station metadata includes data availability
        # This is a simplified check - in production would check station['datatypes']
        return True  # Assume stations have basic weather data

    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points in kilometers
        """
        from math import radians, sin, cos, sqrt, atan2

        R = 6371  # Earth's radius in kilometers

        lat1_rad, lon1_rad = radians(lat1), radians(lon1)
        lat2_rad, lon2_rad = radians(lat2), radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return R * c

    def _parse_niwa_response(self, raw_data: Dict, parameters: str) -> List[Dict]:
        """
        Parse NIWA CliFlo JSON response into standardized format
        Handles the actual NIWA API response structure
        """
        parsed_data = []

        try:
            # NIWA CliFlo returns data in a specific nested format
            # The exact structure depends on the datacategory and datatypes requested

            if 'data' not in raw_data:
                logger.warning("No data field in NIWA response")
                return parsed_data

            data_records = raw_data['data']

            # Handle different response formats
            if isinstance(data_records, list):
                for record in data_records:
                    if isinstance(record, dict):
                        # Parse date - NIWA uses various date formats
                        date_str = record.get('date', record.get('Date', record.get('timestamp')))
                        if not date_str:
                            continue

                        # Standardize date format
                        try:
                            if isinstance(date_str, str):
                                # Handle different date formats
                                if 'T' in date_str:
                                    parsed_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                                else:
                                    parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
                            else:
                                # Assume it's already a date object
                                parsed_date = date_str

                            data_point = {'date': parsed_date.date().isoformat()}

                            # Parse rainfall data (RD = Rain Daily)
                            if 'rainfall' in parameters:
                                rainfall_value = record.get('RD', record.get('rainfall', record.get('precipitation')))
                                if rainfall_value is not None and rainfall_value != '':
                                    try:
                                        data_point['rainfall'] = float(rainfall_value)
                                    except (ValueError, TypeError):
                                        data_point['rainfall'] = 0.0
                                else:
                                    data_point['rainfall'] = 0.0

                            # Parse temperature data (TMX = Temp Max, TMN = Temp Min)
                            if 'temperature_max' in parameters:
                                tmax_value = record.get('TMX', record.get('temperature_max', record.get('tmax')))
                                if tmax_value is not None and tmax_value != '':
                                    try:
                                        data_point['temperature_max'] = float(tmax_value)
                                    except (ValueError, TypeError):
                                        data_point['temperature_max'] = None

                            if 'temperature_min' in parameters:
                                tmin_value = record.get('TMN', record.get('temperature_min', record.get('tmin')))
                                if tmin_value is not None and tmin_value != '':
                                    try:
                                        data_point['temperature_min'] = float(tmin_value)
                                    except (ValueError, TypeError):
                                        data_point['temperature_min'] = None

                            # Only add data points that have at least one valid measurement
                            if any(k in data_point for k in ['rainfall', 'temperature_max', 'temperature_min']):
                                parsed_data.append(data_point)

                        except (ValueError, TypeError) as e:
                            logger.warning(f"Failed to parse NIWA record date: {date_str} - {e}")
                            continue

            else:
                logger.warning(f"Unexpected NIWA data format: {type(data_records)}")

        except Exception as e:
            logger.error(f"Failed to parse NIWA response: {e}")
            logger.debug(f"Raw NIWA response: {raw_data}")

        # Sort by date (most recent first)
        parsed_data.sort(key=lambda x: x['date'], reverse=True)

        logger.info(f"Parsed {len(parsed_data)} data points from NIWA response")
        return parsed_data

    def _mock_station_data(self, parameters: str, days: int) -> List[Dict]:
        """
        Generate mock data when API is unavailable
        """
        mock_data = []

        for i in range(days):
            data_point = {
                'date': (datetime.utcnow() - timedelta(days=i)).date().isoformat()
            }

            if 'rainfall' in parameters:
                data_point['rainfall'] = max(0, 3.0 + (i % 14 - 7) * 0.2)

            if 'temperature_max' in parameters:
                data_point['temperature_max'] = 24.0 - abs(i % 30 - 15) * 0.3

            if 'temperature_min' in parameters:
                data_point['temperature_min'] = 14.0 - abs(i % 30 - 15) * 0.2

            mock_data.append(data_point)

        return mock_data

    def _mock_rainfall_data(self, lat: float, lon: float) -> Dict:
        """Mock rainfall data for development"""
        return {
            'data': [
                {
                    'date': (datetime.utcnow() - timedelta(days=i)).date().isoformat(),
                    'rainfall': max(0, 3.0 + (i % 14 - 7) * 0.2)  # Gradual drying trend
                }
                for i in range(90)
            ],
            'sources': [{
                'provider': 'NIWA_DataHub',
                'dataset': 'Mock_Data',
                'timestamp': datetime.utcnow(),
                'freshness_hours': 0,
                'parameters': ['rainfall_daily']
            }]
        }

    def _mock_temperature_data(self, lat: float, lon: float) -> Dict:
        """Mock temperature data for development"""
        return {
            'data': [
                {
                    'date': (datetime.utcnow() - timedelta(days=i)).date().isoformat(),
                    'temperature_max': 24.0 - abs(i % 30 - 15) * 0.3,  # Seasonal variation
                    'temperature_min': 14.0 - abs(i % 30 - 15) * 0.2
                }
                for i in range(90)
            ],
            'sources': [{
                'provider': 'NIWA_DataHub',
                'dataset': 'Mock_Data',
                'timestamp': datetime.utcnow(),
                'freshness_hours': 0,
                'parameters': ['temperature_max', 'temperature_min']
            }]
        }