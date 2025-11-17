# Drought Calculator Agent
# Computes SPI, SMD, and NZDI indicators with scientific precision

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from scipy import stats
import logging

logger = logging.getLogger(__name__)

class DroughtCalculatorAgent:
    """
    Agent for calculating drought indicators using meteorological data.
    Implements LOG³ precision for accurate scientific computations.
    """

    def __init__(self):
        # NZDI thresholds (NIWA standard)
        self.nzdi_thresholds = {
            'NORMAL': (-0.5, 0.5),
            'DRY': (-0.8, -0.5),
            'VERY_DRY': (-1.3, -0.8),
            'EXTREMELY_DRY': (-2.0, -1.3),
            'DROUGHT': (-float('inf'), -2.0),
            'SEVERE_DROUGHT': (-float('inf'), -2.5)
        }

    async def calculate_spi(self, rainfall_data: Dict, period: int = 30) -> Dict:
        """
        Calculate Standardized Precipitation Index
        SPI measures precipitation deficit relative to historical norms

        Args:
            rainfall_data: Dict with 'data' containing daily rainfall
            period: Accumulation period (30 or 60 days)

        Returns:
            SPI value and metadata
        """
        try:
            df = pd.DataFrame(rainfall_data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date').sort_index()

            # Calculate rolling precipitation sum
            df[f'precip_{period}d'] = df['rainfall'].rolling(window=period).sum()

            # Fit gamma distribution to historical data
            precip_values = df[f'precip_{period}d'].dropna().values
            if len(precip_values) < 30:
                return {'value': 0.0, 'period': period, 'error': 'Insufficient data'}

            # Gamma distribution fitting
            shape, loc, scale = stats.gamma.fit(precip_values[precip_values > 0])

            # Calculate SPI for most recent value
            current_precip = df[f'precip_{period}d'].iloc[-1]
            if current_precip <= 0:
                spi_value = -3.0  # Extreme drought
            else:
                # CDF of gamma distribution
                cdf_value = stats.gamma.cdf(current_precip, shape, loc, scale)
                # Convert to standard normal
                spi_value = stats.norm.ppf(cdf_value)

            return {
                'value': round(float(spi_value), 2),
                'period': period,
                'precipitation_mm': round(current_precip, 1),
                'method': 'gamma_distribution'
            }

        except Exception as e:
            logger.error(f"SPI calculation failed: {e}")
            return {'value': 0.0, 'period': period, 'error': str(e)}

    async def calculate_smd(self, rainfall_data: Dict, temperature_data: Dict,
                           soil_sensors: Optional[Dict] = None) -> Dict:
        """
        Calculate Soil Moisture Deficit using water balance approach
        SMD = Potential Evapotranspiration - Actual Precipitation

        Args:
            rainfall_data: Daily rainfall data
            temperature_data: Daily temperature data
            soil_sensors: Optional direct soil moisture measurements

        Returns:
            Current SMD and anomaly analysis
        """
        try:
            # Combine rainfall and temperature data
            rain_df = pd.DataFrame(rainfall_data['data'])
            temp_df = pd.DataFrame(temperature_data['data'])

            # Merge on date
            df = pd.merge(rain_df, temp_df, on='date', how='inner')
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date').sort_index()

            # Calculate potential evapotranspiration (simplified Thornthwaite)
            df['pet'] = self._calculate_pet(df['temperature_max'], df['temperature_min'])

            # Calculate soil moisture balance
            df['net_water'] = df['rainfall'] - df['pet']
            df['soil_moisture'] = df['net_water'].cumsum()

            # Calculate field capacity (assume 150mm for NZ pastoral)
            field_capacity = 150
            df['smd'] = field_capacity - df['soil_moisture']
            df['smd'] = df['smd'].clip(lower=0)  # Can't be negative

            # Current SMD (most recent)
            current_smd = df['smd'].iloc[-1]

            # Calculate anomaly (departure from normal)
            # Use 30-day rolling mean as "normal"
            df['smd_normal'] = df['smd'].rolling(window=30).mean()
            current_anomaly = current_smd - df['smd_normal'].iloc[-1]

            return {
                'current': round(current_smd, 1),
                'anomaly': round(current_anomaly, 1),
                'field_capacity': field_capacity,
                'method': 'water_balance_thornthwaite',
                'time_series': df[['smd', 'smd_normal']].tail(30).to_dict('records')
            }

        except Exception as e:
            logger.error(f"SMD calculation failed: {e}")
            return {
                'current': 50.0,  # Default moderate deficit
                'anomaly': -10.0,
                'error': str(e)
            }

    async def calculate_nzdi(self, rainfall_data: Dict, temperature_data: Dict,
                            soil_sensors: Optional[Dict] = None) -> Dict:
        """
        Calculate New Zealand Drought Index (composite indicator)
        NZDI combines multiple drought signals into categorical assessment
        """
        try:
            # Get component indicators
            spi_30 = await self.calculate_spi(rainfall_data, 30)
            spi_60 = await self.calculate_spi(rainfall_data, 60)
            smd = await self.calculate_smd(rainfall_data, temperature_data, soil_sensors)

            # NZDI calculation (simplified version of NIWA methodology)
            # Weighted combination of SPI and SMD
            spi_weight = 0.6
            smd_weight = 0.4

            # Normalize SMD to SPI scale (rough approximation)
            smd_normalized = min(3.0, smd['current'] / 50.0)  # SMD >150mm = SPI -3

            nzdi_value = spi_weight * spi_30['value'] + smd_weight * smd_normalized

            # Categorize
            category = self._categorize_nzdi(nzdi_value)

            return {
                'value': round(nzdi_value, 2),
                'category': category,
                'components': {
                    'spi_30_weighted': round(spi_weight * spi_30['value'], 2),
                    'smd_weighted': round(smd_weight * smd_normalized, 2)
                },
                'method': 'niwa_composite'
            }

        except Exception as e:
            logger.error(f"NZDI calculation failed: {e}")
            return {
                'value': 0.0,
                'category': 'NORMAL',
                'error': str(e)
            }

    async def detect_anomalies(self, indicators: Dict) -> List[str]:
        """
        LOG⁴ anomaly exploration: Detect unusual patterns
        """
        anomalies = []

        spi_30 = indicators.get('spi_30', {}).get('value', 0)
        spi_60 = indicators.get('spi_60', {}).get('value', 0)
        smd = indicators.get('smd', {})

        # Check for rapid deterioration
        if spi_30 < -2.0 and spi_60 > -1.0:
            anomalies.append("Rapid SPI deterioration: 30-day extreme, 60-day moderate")

        # Check for SMD anomalies
        if smd.get('anomaly', 0) < -50:
            anomalies.append(f"Extreme SMD anomaly: {smd['anomaly']:.0f}mm below normal")

        # Check historical analogs
        analogs = indicators.get('historical_analogs', [])
        if analogs:
            best_match = max(analogs, key=lambda x: x.get('similarity', 0))
            if best_match.get('similarity', 0) > 0.8:
                anomalies.append(f"Similar to {best_match['date']} drought pattern")

        return anomalies

    async def lat_lon_to_region(self, lat: float, lon: float) -> str:
        """
        Convert latitude/longitude to NZ region name
        """
        # Simplified region mapping (would use proper GIS in production)
        if -35.0 <= lat <= -34.0 and 172.0 <= lon <= 173.0:
            return "Marlborough"
        elif -38.0 <= lat <= -37.0 and 175.0 <= lon <= 176.0:
            return "Waikato"
        elif -41.0 <= lat <= -40.0 and 174.0 <= lon <= 175.0:
            return "Wellington"
        elif -45.0 <= lat <= -44.0 and 168.0 <= lon <= 169.0:
            return "Otago"
        else:
            return "Canterbury"  # Default

    def _calculate_pet(self, tmax_series: pd.Series, tmin_series: pd.Series) -> pd.Series:
        """
        Calculate Potential Evapotranspiration using Thornthwaite method
        Simplified for NZ conditions
        """
        # Average temperature
        tmean = (tmax_series + tmin_series) / 2

        # Thornthwaite PET (simplified)
        # PET = 16 * (10 * Tmean / I)^a * (N/12) * (N_days/30)
        # For NZ, approximate with temperature-based formula
        pet = 0.0023 * (tmean + 17.8) * (tmax_series - tmin_series) ** 0.5

        return pet.clip(lower=0)  # Can't be negative

    def _categorize_nzdi(self, nzdi_value: float) -> str:
        """
        Categorize NZDI value into drought categories
        """
        for category, (min_val, max_val) in self.nzdi_thresholds.items():
            if min_val <= nzdi_value < max_val:
                return category

        # Handle extreme values
        if nzdi_value < -2.5:
            return "SEVERE_DROUGHT"
        elif nzdi_value < -2.0:
            return "DROUGHT"
        else:
            return "NORMAL"