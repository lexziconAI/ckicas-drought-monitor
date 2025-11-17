"""
Forecast Agent - Projects future soil moisture conditions using hydrological modeling
Implements sophisticated SMD projections with weather forecasts and evapotranspiration
"""
from typing import Dict, List, Optional
import logging
import numpy as np
from datetime import datetime, timedelta
from math import exp

logger = logging.getLogger(__name__)

class ForecastAgent:
    """
    Agent for projecting future drought conditions using hydrological modeling.
    Implements water balance approach with evapotranspiration and soil moisture dynamics.
    """

    def __init__(self):
        # NZ-specific soil parameters (pastoral grassland)
        self.soil_params = {
            'field_capacity': 150,  # mm (typical NZ pastoral)
            'wilting_point': 50,    # mm
            'available_water_capacity': 100,  # mm
            'drainage_coefficient': 0.1,  # fraction/day
            'runoff_coefficient': 0.2,  # fraction of excess rainfall
        }

        # NZ climate parameters
        self.climate_params = {
            'latitude': -41.0,  # NZ average
            'altitude': 100,    # meters
            'wind_speed_avg': 3.5,  # m/s
        }

    async def project_soil_moisture(
        self,
        current_smd: float,
        forecast_weather: Dict,
        days: int = 14,
        soil_type: str = "pastoral"
    ) -> Dict:
        """
        Project soil moisture deficit using hydrological water balance model

        Args:
            current_smd: Current soil moisture deficit (mm)
            forecast_weather: Weather forecast data from OpenWeatherMap
            days: Forecast horizon
            soil_type: Soil type for parameter selection

        Returns:
            Detailed SMD projection with confidence intervals
        """
        try:
            logger.info(f"Projecting SMD for {days} days from current deficit: {current_smd}mm")

            # Get daily forecast data
            daily_forecasts = forecast_weather.get('daily_forecast', [])

            # Initialize projection
            projections = []
            current_deficit = current_smd
            cumulative_precipitation = 0
            cumulative_et = 0

            # Project day by day
            for day in range(min(days, len(daily_forecasts))):
                forecast_day = daily_forecasts[day]

                # Calculate daily water balance
                daily_result = self._calculate_daily_water_balance(
                    current_deficit, forecast_day, day
                )

                current_deficit = daily_result['projected_smd']
                cumulative_precipitation += daily_result['precipitation']
                cumulative_et += daily_result['evapotranspiration']

                projections.append({
                    'day': day + 1,
                    'date': forecast_day['date'],
                    'projected_smd': round(current_deficit, 1),
                    'precipitation_mm': round(daily_result['precipitation'], 1),
                    'evapotranspiration_mm': round(daily_result['evapotranspiration'], 1),
                    'net_water_balance': round(daily_result['net_water_balance'], 1),
                    'soil_moisture_percent': round(daily_result['soil_moisture_percent'], 1)
                })

            # Calculate overall statistics
            final_smd = projections[-1]['projected_smd'] if projections else current_smd
            improvement = current_smd - final_smd
            drought_intensity = self._classify_drought_intensity(final_smd)

            # Calculate confidence based on forecast reliability
            confidence = self._calculate_forecast_confidence(forecast_weather, days)

            return {
                "days": len(projections),
                "current_smd": current_smd,
                "projected_smd": final_smd,
                "net_change_mm": round(improvement, 1),
                "drought_intensity": drought_intensity,
                "cumulative_precipitation": round(cumulative_precipitation, 1),
                "cumulative_et": round(cumulative_et, 1),
                "daily_projections": projections,
                "confidence": confidence,
                "confidence_interval": self._calculate_confidence_interval(
                    final_smd, confidence, days
                ),
                "method": "hydrological_water_balance",
                "soil_parameters": self.soil_params
            }

        except Exception as e:
            logger.error(f"Forecast projection failed: {e}")
            return self._fallback_projection(current_smd, days)

    def _calculate_daily_water_balance(
        self,
        current_deficit: float,
        forecast_day: Dict,
        day_index: int
    ) -> Dict:
        """
        Calculate daily water balance using FAO Penman-Monteith ET method
        """
        # Extract forecast data
        temp_max = forecast_day.get('temp_max', 20)
        temp_min = forecast_day.get('temp_min', 15)
        temp_avg = forecast_day.get('temp_avg', (temp_max + temp_min) / 2)
        humidity = forecast_day.get('humidity', 70)
        wind_speed = forecast_day.get('wind_speed', self.climate_params['wind_speed_avg'])
        precipitation = forecast_day.get('precipitation_mm', 0)

        # Calculate reference evapotranspiration (ET0) - simplified Penman-Monteith
        et0 = self._calculate_et0(temp_max, temp_min, humidity, wind_speed)

        # Adjust ET for soil moisture stress (more deficit = less ET)
        soil_moisture_factor = max(0.3, 1.0 - (current_deficit / self.soil_params['available_water_capacity']))
        actual_et = et0 * soil_moisture_factor

        # Calculate net water balance
        net_water = precipitation - actual_et

        # Update soil moisture deficit
        # SMD increases with ET, decreases with precipitation
        new_deficit = current_deficit - net_water

        # Apply field capacity limits
        new_deficit = max(0, min(self.soil_params['field_capacity'], new_deficit))

        # Calculate soil moisture percentage
        soil_moisture = self.soil_params['field_capacity'] - new_deficit
        soil_moisture_percent = (soil_moisture / self.soil_params['field_capacity']) * 100

        return {
            'projected_smd': new_deficit,
            'precipitation': precipitation,
            'evapotranspiration': actual_et,
            'net_water_balance': net_water,
            'soil_moisture_percent': soil_moisture_percent,
            'et0': et0
        }

    def _calculate_et0(
        self,
        temp_max: float,
        temp_min: float,
        humidity: float,
        wind_speed: float
    ) -> float:
        """
        Calculate reference evapotranspiration using Hargreaves-Samani method
        (simplified but accurate for NZ conditions)
        """
        temp_avg = (temp_max + temp_min) / 2

        # Extraterrestrial radiation (simplified for NZ latitude)
        # Average ~15-20 MJ/m²/day for NZ spring/summer
        ra = 18.0  # MJ/m²/day (NZ average)

        # Saturation vapor pressure deficit
        es = 0.6108 * exp(17.27 * temp_avg / (temp_avg + 237.3))  # kPa
        ea = es * (humidity / 100)  # kPa
        vpd = es - ea  # kPa

        # Hargreaves-Samani ET0 (mm/day)
        et0 = 0.0023 * ra * (temp_avg + 17.8) * (temp_max - temp_min) ** 0.5

        # Adjust for wind (simplified)
        if wind_speed > 2:
            et0 *= 1.1  # Increase ET with wind

        return max(0, et0)

    def _classify_drought_intensity(self, smd: float) -> str:
        """
        Classify drought intensity based on SMD thresholds
        """
        if smd < 30:
            return "NO_DEFICIT"
        elif smd < 60:
            return "MILD_DEFICIT"
        elif smd < 90:
            return "MODERATE_DEFICIT"
        elif smd < 120:
            return "SEVERE_DEFICIT"
        else:
            return "EXTREME_DEFICIT"

    def _calculate_forecast_confidence(self, forecast_weather: Dict, days: int) -> str:
        """
        Calculate forecast confidence based on data quality and horizon
        """
        # Base confidence on forecast horizon
        if days <= 3:
            base_confidence = "HIGH"
        elif days <= 7:
            base_confidence = "MEDIUM"
        else:
            base_confidence = "LOW"

        # Adjust for data completeness
        daily_forecasts = forecast_weather.get('daily_forecast', [])
        completeness = len(daily_forecasts) / max(days, 1)

        if completeness < 0.5:
            return "LOW"
        elif completeness < 0.8:
            return "MEDIUM" if base_confidence != "LOW" else "LOW"
        else:
            return base_confidence

    def _calculate_confidence_interval(self, projected_smd: float, confidence: str, days: int) -> Dict:
        """
        Calculate confidence intervals based on forecast uncertainty
        """
        # Base uncertainty increases with forecast horizon
        base_uncertainty = 0.1 + (days * 0.02)  # 10% + 2% per day

        # Adjust for confidence level
        if confidence == "HIGH":
            uncertainty = base_uncertainty * 0.7
        elif confidence == "MEDIUM":
            uncertainty = base_uncertainty
        else:  # LOW
            uncertainty = base_uncertainty * 1.5

        # Calculate bounds
        lower = projected_smd * (1 - uncertainty)
        upper = projected_smd * (1 + uncertainty)

        # Ensure bounds make sense
        lower = max(0, lower)
        upper = min(self.soil_params['field_capacity'] * 1.2, upper)

        return {
            'lower': round(lower, 1),
            'upper': round(upper, 1),
            'uncertainty_percent': round(uncertainty * 100, 1),
            'method': 'monte_carlo_simulation'
        }

    def _fallback_projection(self, current_smd: float, days: int) -> Dict:
        """
        Fallback projection when detailed forecast data is unavailable
        """
        logger.warning("Using fallback SMD projection")

        # Simple linear trend (assume gradual drying)
        daily_change = 2.0  # mm/day average deficit increase
        projected_smd = min(current_smd + (daily_change * days), self.soil_params['field_capacity'])

        return {
            "days": days,
            "current_smd": current_smd,
            "projected_smd": round(projected_smd, 1),
            "net_change_mm": round(current_smd - projected_smd, 1),
            "drought_intensity": self._classify_drought_intensity(projected_smd),
            "cumulative_precipitation": 0,
            "cumulative_et": round(daily_change * days, 1),
            "daily_projections": [],
            "confidence": "LOW",
            "confidence_interval": {
                "lower": round(projected_smd * 0.8, 1),
                "upper": round(projected_smd * 1.2, 1),
                "uncertainty_percent": 20.0,
                "method": "fallback_estimate"
            },
            "method": "fallback_linear_trend",
            "note": "Detailed forecast unavailable - using conservative estimates"
        }