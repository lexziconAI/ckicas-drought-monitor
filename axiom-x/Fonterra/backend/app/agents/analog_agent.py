# Historical Drought Analog Agent
# Finds historical periods similar to current conditions

from typing import List, Dict, Tuple
import logging
from datetime import datetime, timedelta
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from app.constitutional.yamas import YamaValidator

logger = logging.getLogger(__name__)


class HistoricalAnalogAgent:
    """
    Agent for finding historical drought analogs.
    Constitutional AI: Satya (truth) - provides factual historical context
    """

    def __init__(self, validator: YamaValidator):
        self.validator = validator
        self.historical_data = {}  # Would be loaded from database/cache

    async def find_analogs(
        self,
        current_indicators: Dict,
        region: str,
        lookback_years: int = 50,
        max_analogs: int = 5
    ) -> List[Dict]:
        """
        Find historical periods with similar drought conditions.

        Args:
            current_indicators: Current SPI, SMD values
            region: Geographic region
            lookback_years: How far back to search
            max_analogs: Maximum number of analogs to return

        Returns:
            List of analog periods with similarity scores
        """
        try:
            # Load historical data for region
            historical_series = await self._load_historical_data(region, lookback_years)

            if not historical_series:
                logger.warning(f"No historical data available for region {region}")
                return []

            # Calculate similarities
            analogs = []
            current_vector = self._indicators_to_vector(current_indicators)

            for period_data in historical_series:
                period_vector = self._indicators_to_vector(period_data["indicators"])
                similarity = self._calculate_similarity(current_vector, period_vector)

                if similarity > 0.7:  # Similarity threshold
                    analog = {
                        "date": period_data["date"],
                        "similarity_score": round(similarity, 3),
                        "indicators": period_data["indicators"],
                        "outcome": period_data.get("outcome", "unknown"),
                        "duration_days": period_data.get("duration_days", 0)
                    }
                    analogs.append(analog)

            # Sort by similarity and return top matches
            analogs.sort(key=lambda x: x["similarity_score"], reverse=True)
            return analogs[:max_analogs]

        except Exception as e:
            logger.error(f"Error finding historical analogs: {e}")
            return []

    async def _load_historical_data(self, region: str, years: int) -> List[Dict]:
        """
        Load historical drought data for the region.
        In production, this would query a database.
        """
        # Mock data for now - would be replaced with actual database queries
        base_date = datetime.now() - timedelta(days=years*365)

        mock_data = []
        for i in range(100):  # Generate 100 historical periods
            date = base_date + timedelta(days=i*30)  # Monthly intervals
            # Generate somewhat realistic drought indicators
            spi_30 = np.random.normal(-0.5, 1.5)  # Slightly dry bias
            spi_60 = np.random.normal(-0.3, 1.3)
            smd = np.random.normal(-80, 50) if spi_30 < -1 else np.random.normal(-20, 30)

            mock_data.append({
                "date": date.isoformat(),
                "indicators": {
                    "spi_30day": round(spi_30, 2),
                    "spi_60day": round(spi_60, 2),
                    "smd_current": round(smd, 1),
                    "smd_anomaly": round(smd * 0.8, 1)
                },
                "outcome": "recovered" if np.random.random() > 0.3 else "worsened",
                "duration_days": np.random.randint(30, 180)
            })

        return mock_data

    def _indicators_to_vector(self, indicators: Dict) -> np.ndarray:
        """Convert indicators dict to feature vector for similarity calculation"""
        # Normalize indicators to similar scales
        features = [
            indicators.get("spi_30day", 0) / 3,  # SPI ranges ~ -3 to +3
            indicators.get("spi_60day", 0) / 3,
            indicators.get("smd_current", 0) / 200,  # SMD ranges ~ -200 to +50
            indicators.get("smd_anomaly", 0) / 100
        ]
        return np.array(features).reshape(1, -1)

    def _calculate_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two indicator vectors"""
        return cosine_similarity(vec1, vec2)[0][0]

    def validate_analog(self, analog: Dict) -> bool:
        """
        Validate that an analog meets constitutional standards.
        """
        # Ensure analog has required fields
        required_fields = ["date", "similarity_score", "indicators"]
        if not all(field in analog for field in required_fields):
            return False

        # Ensure similarity is reasonable
        if not (0 <= analog["similarity_score"] <= 1):
            return False

        # Validate indicators
        indicators = analog["indicators"]
        if not all(isinstance(indicators.get(k), (int, float)) for k in ["spi_30day", "spi_60day", "smd_current"]):
            return False

        return True