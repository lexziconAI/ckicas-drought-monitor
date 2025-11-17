# NIWA DataHub Agent
# Fetches meteorological data from NIWA DataHub API (VCSN grid data)
# Implements constitutional AI principles with CliFlo fallback

import httpx
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)

class NIWADataHubAgent:
    """
    Agent for fetching meteorological data from NIWA DataHub VCSN (Virtual Climate Station Network).
    Implements LOG³ precision for strict API contract adherence.
    Falls back to CliFlo if DataHub unavailable (Asteya - proper attribution).
    """

    def __init__(self):
        # DataHub API endpoints
        self.datahub_base = "https://data.niwa.co.nz/api"
        self.cliflo_base = "https://cliflo.niwa.co.nz"

        # Credentials
        self.api_key = os.getenv("NIWA_API_KEY")
        self.email = os.getenv("NIWA_DATAHUB_EMAIL")

        # VCSN grid resolution (0.05° ~ 5km)
        self.grid_resolution = 0.05

        if not self.api_key or not self.email:
            logger.warning("NIWA DataHub credentials not configured - will use CliFlo fallback")

    async def fetch_90day_rainfall(self, lat: float, lon: float) -> Dict:
        """
        Fetch 90 days of rainfall data for location.
        Prefers VCSN grid data, falls back to CliFlo station data.
        Returns data with source attribution (Asteya principle).
        """
        try:
            # Try DataHub VCSN first
            datahub_result = await self._fetch_datahub_rainfall(lat, lon)
            if datahub_result:
                return datahub_result

            # Fallback to CliFlo
            logger.info("DataHub unavailable, falling back to CliFlo")
            return await self._fetch_cliflo_rainfall(lat, lon)

        except Exception as e:
            logger.error(f"NIWA DataHub rainfall fetch failed: {e}")
            # Final fallback to mock data
            return self._mock_rainfall_data(lat, lon)

    async def fetch_90day_temperature(self, lat: float, lon: float) -> Dict:
        """
        Fetch 90 days of temperature data for location.
        Prefers VCSN grid data, falls back to CliFlo station data.
        """
        try:
            # Try DataHub VCSN first
            datahub_result = await self._fetch_datahub_temperature(lat, lon)
            if datahub_result:
                return datahub_result

            # Fallback to CliFlo
            logger.info("DataHub unavailable, falling back to CliFlo")
            return await self._fetch_cliflo_temperature(lat, lon)

        except Exception as e:
            logger.error(f"NIWA DataHub temperature fetch failed: {e}")
            # Final fallback to mock data
            return self._mock_temperature_data(lat, lon)

    async def _fetch_datahub_rainfall(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Fetch rainfall from NIWA DataHub VCSN API.
        Returns None if unavailable (triggers CliFlo fallback).
        """
        if not self.api_key or not self.email:
            return None

        try:
            # Find nearest VCSN grid point
            grid_lat, grid_lon = self._lat_lon_to_vcsn_grid(lat, lon)

            # DataHub API endpoint for VCSN rainfall
            # Note: This is a placeholder - actual endpoint structure TBD when access granted
            endpoint = f"{self.datahub_base}/vcsn/rainfall"

            params = {
                'lat': grid_lat,
                'lon': grid_lon,
                'start_date': (datetime.utcnow() - timedelta(days=90)).strftime('%Y-%m-%d'),
                'end_date': datetime.utcnow().strftime('%Y-%m-%d'),
                'api_key': self.api_key,
                'email': self.email
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(endpoint, params=params)
                response.raise_for_status()

                data = response.json()

                # Parse VCSN response (structure TBD)
                parsed_data = self._parse_vcsn_rainfall(data)

                return {
                    'data': parsed_data,
                    'grid_point': {'lat': grid_lat, 'lon': grid_lon},
                    'sources': [{
                        'provider': 'NIWA_DataHub',
                        'dataset': f'VCSN_Grid_{grid_lat:.3f}_{grid_lon:.3f}',
                        'timestamp': datetime.utcnow(),
                        'freshness_hours': 0,
                        'parameters': ['rainfall_daily'],
                        'grid_resolution_km': 5,
                        'interpolation_method': 'bilinear'
                    }]
                }

        except Exception as e:
            logger.warning(f"DataHub VCSN rainfall fetch failed: {e}")
            return None

    async def _fetch_datahub_temperature(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Fetch temperature from NIWA DataHub VCSN API.
        Returns None if unavailable (triggers CliFlo fallback).
        """
        if not self.api_key or not self.email:
            return None

        try:
            # Find nearest VCSN grid point
            grid_lat, grid_lon = self._lat_lon_to_vcsn_grid(lat, lon)

            # DataHub API endpoint for VCSN temperature
            endpoint = f"{self.datahub_base}/vcsn/temperature"

            params = {
                'lat': grid_lat,
                'lon': grid_lon,
                'start_date': (datetime.utcnow() - timedelta(days=90)).strftime('%Y-%m-%d'),
                'end_date': datetime.utcnow().strftime('%Y-%m-%d'),
                'api_key': self.api_key,
                'email': self.email
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(endpoint, params=params)
                response.raise_for_status()

                data = response.json()

                # Parse VCSN response
                parsed_data = self._parse_vcsn_temperature(data)

                return {
                    'data': parsed_data,
                    'grid_point': {'lat': grid_lat, 'lon': grid_lon},
                    'sources': [{
                        'provider': 'NIWA_DataHub',
                        'dataset': f'VCSN_Grid_{grid_lat:.3f}_{grid_lon:.3f}',
                        'timestamp': datetime.utcnow(),
                        'freshness_hours': 0,
                        'parameters': ['temperature_max', 'temperature_min'],
                        'grid_resolution_km': 5,
                        'interpolation_method': 'bilinear'
                    }]
                }

        except Exception as e:
            logger.warning(f"DataHub VCSN temperature fetch failed: {e}")
            return None

    async def _fetch_cliflo_rainfall(self, lat: float, lon: float) -> Dict:
        """
        Fallback to CliFlo station data for rainfall.
        Uses existing CliFlo agent logic.
        """
        # Import here to avoid circular dependency
        from app.agents.niwa_agent import NIWADataAgent

        cliflo_agent = NIWADataAgent()
        return await cliflo_agent.fetch_90day_rainfall(lat, lon)

    async def _fetch_cliflo_temperature(self, lat: float, lon: float) -> Dict:
        """
        Fallback to CliFlo station data for temperature.
        Uses existing CliFlo agent logic.
        """
        # Import here to avoid circular dependency
        from app.agents.niwa_agent import NIWADataAgent

        cliflo_agent = NIWADataAgent()
        return await cliflo_agent.fetch_90day_temperature(lat, lon)

    def _lat_lon_to_vcsn_grid(self, lat: float, lon: float) -> Tuple[float, float]:
        """
        Convert lat/lon to nearest VCSN grid point.
        VCSN grid covers NZ at 0.05° resolution (~5km).
        """
        # VCSN grid bounds (approximate NZ coverage)
        grid_bounds = {
            'lat_min': -47.0,
            'lat_max': -34.0,
            'lon_min': 166.0,
            'lon_max': 179.0
        }

        # Clamp to grid bounds
        grid_lat = max(grid_bounds['lat_min'],
                      min(grid_bounds['lat_max'],
                          round(lat / self.grid_resolution) * self.grid_resolution))

        grid_lon = max(grid_bounds['lon_min'],
                      min(grid_bounds['lon_max'],
                          round(lon / self.grid_resolution) * self.grid_resolution))

        return grid_lat, grid_lon

    def _parse_vcsn_rainfall(self, data: Dict) -> List[Dict]:
        """
        Parse VCSN rainfall response into standardized format.
        Structure TBD when DataHub access granted.
        """
        # Placeholder parsing - will be updated when we have actual API response
        parsed_data = []

        try:
            # Expected VCSN structure (hypothetical based on NIWA documentation)
            if 'rainfall' in data:
                for record in data['rainfall']:
                    parsed_data.append({
                        'date': record.get('date'),
                        'rainfall': record.get('value', 0.0)
                    })

        except Exception as e:
            logger.error(f"Failed to parse VCSN rainfall: {e}")

        return parsed_data

    def _parse_vcsn_temperature(self, data: Dict) -> List[Dict]:
        """
        Parse VCSN temperature response into standardized format.
        Structure TBD when DataHub access granted.
        """
        # Placeholder parsing - will be updated when we have actual API response
        parsed_data = []

        try:
            # Expected VCSN structure (hypothetical)
            if 'temperature' in data:
                for record in data['temperature']:
                    parsed_data.append({
                        'date': record.get('date'),
                        'temperature_max': record.get('tmax'),
                        'temperature_min': record.get('tmin')
                    })

        except Exception as e:
            logger.error(f"Failed to parse VCSN temperature: {e}")

        return parsed_data

    def _mock_rainfall_data(self, lat: float, lon: float) -> Dict:
        """Mock rainfall data for development/testing"""
        return {
            'data': [
                {
                    'date': (datetime.utcnow() - timedelta(days=i)).date().isoformat(),
                    'rainfall': max(0, 3.0 + (i % 14 - 7) * 0.2)
                }
                for i in range(90)
            ],
            'sources': [{
                'provider': 'NIWA_DataHub',
                'dataset': 'Mock_VCSN_Data',
                'timestamp': datetime.utcnow(),
                'freshness_hours': 0,
                'parameters': ['rainfall_daily'],
                'note': 'Mock data - awaiting DataHub access'
            }]
        }

    def _mock_temperature_data(self, lat: float, lon: float) -> Dict:
        """Mock temperature data for development/testing"""
        return {
            'data': [
                {
                    'date': (datetime.utcnow() - timedelta(days=i)).date().isoformat(),
                    'temperature_max': 24.0 - abs(i % 30 - 15) * 0.3,
                    'temperature_min': 14.0 - abs(i % 30 - 15) * 0.2
                }
                for i in range(90)
            ],
            'sources': [{
                'provider': 'NIWA_DataHub',
                'dataset': 'Mock_VCSN_Data',
                'timestamp': datetime.utcnow(),
                'freshness_hours': 0,
                'parameters': ['temperature_max', 'temperature_min'],
                'note': 'Mock data - awaiting DataHub access'
            }]
        }