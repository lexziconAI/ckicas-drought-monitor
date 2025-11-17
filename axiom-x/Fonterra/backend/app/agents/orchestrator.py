# Drought Assessment Orchestrator
# Constitutional multi-agent coordinator for drought intelligence

from typing import Dict, List, Tuple
import asyncio
import logging
from datetime import datetime, timedelta

from app.constitutional.yamas import YamaValidator
from app.constitutional.confidence import ConfidenceCalibrator
from app.agents.niwa_agent import NIWADataAgent
from app.agents.council_agent import RegionalCouncilAgent
from app.agents.weather_agent import OpenWeatherAgent
from app.agents.calculator_agent import DroughtCalculatorAgent
from app.agents.forecast_agent import ForecastAgent
from app.services.cache import brahmacharya_cache

logger = logging.getLogger(__name__)

class DroughtOrchestrator:
    """
    Constitutional coordinator for multi-agent drought assessment.

    Reasoning Allocation:
    - LOG³ (60%): Precise data fetching (strict API contract adherence)
    - LOG⁴ (30%): Anomaly exploration (detect unusual patterns)
    - Bellman (10%): Sequential forecast optimization (day 1→2→3...→14)
    """

    def __init__(self):
        self.agents = {
            'niwa': NIWADataAgent(),
            'councils': RegionalCouncilAgent(),
            'weather': OpenWeatherAgent(),
            'calculator': DroughtCalculatorAgent(),
            'forecast': ForecastAgent(),
            'validator': YamaValidator()
        }
        self.calibrator = ConfidenceCalibrator()

    async def assess_drought_risk(
        self,
        lat: float,
        lon: float,
        region: str,
        days_forecast: int = 14,
        force_refresh: bool = False
    ) -> Dict:
        """
        PARALLEL EXECUTION STRATEGY with BRAHMACHARYA caching:
        1. Check cache first (prevent unnecessary API calls)
        2. Fetch historical data (NIWA + Councils) in parallel if needed
        3. Fetch forecast data (OWM) while historical processes
        4. Calculate indicators (SPI, SMD) from historical
        5. Run forecast projections
        6. Validate constitutional compliance
        7. Cache result and return with confidence calibration
        """

        # Generate cache key
        cache_key = f"drought_risk_{lat:.4f}_{lon:.4f}_{region}_{days_forecast}"

        # Brahmacharya: Check cache before expensive computations
        async def compute_assessment():
            return await self._compute_full_assessment(lat, lon, region, days_forecast)

        assessment, was_cached = await brahmacharya_cache.get_or_compute(
            key=cache_key,
            compute_func=compute_assessment,
            ttl_hours=12,  # Brahmacharya: 12-hour cache for drought data
            source_freshness_hours=6,  # Assume 6-hour source freshness
            force_refresh=force_refresh
        )

        # Add caching metadata
        assessment['caching'] = {
            'was_cached': was_cached,
            'cache_key': cache_key,
            'computed_at': datetime.utcnow().isoformat(),
            'brahmacharya_compliant': True
        }

        if was_cached:
            logger.info(f"Brahmacharya: Used cached assessment for {region} (prevented API calls)")
        else:
            logger.info(f"Computed fresh assessment for {region}")

        return assessment

    async def _compute_full_assessment(
        self,
        lat: float,
        lon: float,
        region: str,
        days_forecast: int = 14
    ) -> Dict:
        """
        Compute complete drought assessment (expensive operation)
        Called only when caching determines fresh data is needed
        """

        # PHASE 1: PARALLEL DATA FETCH (LOG³ precision)
        historical_tasks = [
            self.agents['niwa'].fetch_90day_rainfall(lat, lon),
            self.agents['niwa'].fetch_90day_temperature(lat, lon),
            self.agents['councils'].fetch_soil_moisture(lat, lon, region),  # Updated to use lat/lon
            self.agents['weather'].fetch_current_conditions(lat, lon)
        ]

        forecast_task = self.agents['weather'].fetch_forecast(lat, lon, days_forecast)

        # Execute in parallel
        historical_results, forecast_result = await asyncio.gather(
            asyncio.gather(*historical_tasks),
            forecast_task
        )

        rainfall_90d, temp_90d, soil_sensors, current_wx = historical_results

        # PHASE 2: CALCULATE INDICATORS (LOG³ precision)
        calc_tasks = [
            self.agents['calculator'].calculate_spi(rainfall_90d, period=30),
            self.agents['calculator'].calculate_spi(rainfall_90d, period=60),
            self.agents['calculator'].calculate_smd(rainfall_90d, temp_90d, soil_sensors),
            self.agents['calculator'].calculate_nzdi(rainfall_90d, temp_90d, soil_sensors)
        ]

        spi_30, spi_60, smd_data, nzdi = await asyncio.gather(*calc_tasks)

        # PHASE 3: FORECAST PROJECTION (Bellman sequential optimization)
        forecast_smd = await self.agents['forecast'].project_soil_moisture(
            current_smd=smd_data['current'],
            forecast_weather=forecast_result,
            days=days_forecast
        )

        # PHASE 4: ANOMALY DETECTION (LOG⁴ exploration)
        anomalies = await self.agents['calculator'].detect_anomalies({
            'spi_30': spi_30,
            'spi_60': spi_60,
            'smd': smd_data,
            'historical_analogs': await self.agents['niwa'].fetch_historical_analogs(
                spi_30['value'] if 'value' in spi_30 else 0,
                spi_60['value'] if 'value' in spi_60 else 0,
                region
            )
        })

        # PHASE 5: CONSTITUTIONAL VALIDATION (Ahimsa, Satya, Asteya)
        risk_assessment = {
            'location': {'lat': lat, 'lon': lon, 'region': region},
            'indicators': {
                'spi_30day': spi_30.get('value', 0),
                'spi_60day': spi_60.get('value', 0),
                'smd_current': smd_data.get('current', 0),
                'smd_anomaly': smd_data.get('anomaly', 0),
                'nzdi_category': nzdi.get('category', 'NORMAL')
            },
            'forecast_14day': forecast_smd,
            'anomalies': anomalies,
            'sources': self._aggregate_sources([
                rainfall_90d, temp_90d, soil_sensors, current_wx, forecast_result
            ])
        }

        # Apply constitutional validation
        validated = await self.agents['validator'].validate(risk_assessment)

        # PHASE 6: CONFIDENCE CALIBRATION (Satya principle)
        final_assessment = self.calibrator.calibrate_confidence(
            validated,
            data_freshness=self._calculate_freshness(validated['sources']),
            indicator_convergence=self._check_convergence(validated['indicators']),
            forecast_horizon=days_forecast
        )

        return final_assessment

    def _check_convergence(self, indicators: Dict) -> float:
        """
        Ahimsa enforcement: Calculate indicator convergence score
        Returns 0.0-1.0, where 1.0 = all indicators agree on drought severity
        """
        drought_votes = 0
        total_indicators = 0

        if indicators['spi_30day'] < -1.5:
            drought_votes += 1
        total_indicators += 1

        if indicators['spi_60day'] < -1.5:
            drought_votes += 1
        total_indicators += 1

        if indicators['smd_current'] < -110 and indicators['smd_anomaly'] < -30:
            drought_votes += 1
        total_indicators += 1

        if indicators['nzdi_category'] in ['DROUGHT', 'SEVERE_DROUGHT']:
            drought_votes += 1
        total_indicators += 1

        return drought_votes / total_indicators

    def _calculate_freshness(self, sources: List[Dict]) -> float:
        """
        Calculate average data freshness in hours
        """
        if not sources:
            return 999  # Very stale if no sources

        freshness_values = []
        for source in sources:
            freshness = source.get('freshness_hours', 999)
            freshness_values.append(freshness)

        return sum(freshness_values) / len(freshness_values)

    def _aggregate_sources(self, data_results: List) -> List[Dict]:
        """
        Aggregate all data sources with timestamps and freshness
        (Asteya principle - proper attribution)
        """
        sources = []
        now = datetime.utcnow()

        for result in data_results:
            if isinstance(result, dict) and 'sources' in result:
                sources.extend(result['sources'])
            elif isinstance(result, dict) and 'provider' in result:
                # Single source result
                timestamp = result.get('timestamp', now)
                freshness = (now - timestamp).total_seconds() / 3600
                sources.append({
                    'provider': result['provider'],
                    'dataset': result.get('dataset'),
                    'timestamp': timestamp.isoformat(),
                    'freshness_hours': round(freshness, 1),
                    'parameters': result.get('parameters', [])
                })

        return sources