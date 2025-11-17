# Pydantic Schemas for NZ Drought Early Warning API
# Constitutional AI implementation with enforced validation

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Literal
from datetime import datetime
from enum import Enum

class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class NZDICategory(str, Enum):
    NORMAL = "NORMAL"
    DRY = "DRY"
    VERY_DRY = "VERY_DRY"
    EXTREMELY_DRY = "EXTREMELY_DRY"
    DROUGHT = "DROUGHT"
    SEVERE_DROUGHT = "SEVERE_DROUGHT"

class DataSource(BaseModel):
    provider: str = Field(..., description="Data provider (e.g., NIWA_DataHub, Waikato_RC)")
    dataset: Optional[str] = Field(None, description="Specific dataset ID")
    timestamp: datetime = Field(..., description="When data was collected")
    freshness_hours: float = Field(..., description="Hours since data collection")
    parameters: List[str] = Field(..., description="Parameters included (e.g., ['rainfall', 'temperature'])")

class DroughtIndicators(BaseModel):
    spi_30day: float = Field(..., ge=-4.0, le=4.0, description="30-day Standardized Precipitation Index")
    spi_60day: float = Field(..., ge=-4.0, le=4.0, description="60-day Standardized Precipitation Index")
    smd_current: float = Field(..., description="Current Soil Moisture Deficit (mm)")
    smd_anomaly: float = Field(..., description="SMD departure from normal (mm)")
    nzdi_category: NZDICategory = Field(..., description="New Zealand Drought Index category")

class ForecastProjection(BaseModel):
    days: int = Field(..., ge=1, le=35, description="Forecast horizon in days")
    rain_probability: float = Field(..., ge=0.0, le=1.0, description="Probability of significant rain (>10mm)")
    projected_smd: float = Field(..., description="Projected Soil Moisture Deficit (mm)")
    confidence: ConfidenceLevel
    confidence_interval: Dict[str, float] = Field(
        ...,
        description="Uncertainty range",
        example={"lower": -145, "upper": -125}
    )

class ThresholdDistance(BaseModel):
    parameter: str
    current_value: float
    threshold_value: float
    distance: float
    distance_percent: float
    example_scenario: str

class DroughtRiskResponse(BaseModel):
    location: Dict[str, float] = Field(..., example={"lat": -37.7, "lon": 175.2, "region": "Waikato"})
    risk_score: int = Field(..., ge=0, le=100, description="Composite drought risk (0=no risk, 100=severe)")
    confidence: ConfidenceLevel
    confidence_reason: Optional[str] = Field(None, description="Explanation for confidence level")
    indicators: DroughtIndicators
    forecast_14day: ForecastProjection
    anomalies: Optional[List[str]] = Field(None, description="Notable anomalies detected")
    threshold_distances: Dict[str, List[ThresholdDistance]] = Field(
        ...,
        description="How close to critical thresholds (Ahimsa transparency)"
    )
    sources: List[DataSource] = Field(..., min_items=1, description="All data sources (Asteya compliance)")
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class RegionSummary(BaseModel):
    region_name: str
    avg_risk_score: float
    max_risk_score: float
    drought_area_percent: float = Field(..., description="% of region in drought conditions")
    affected_population_estimate: Optional[int] = None
    top_affected_locations: List[Dict[str, float]]

class HistoricalAnalog(BaseModel):
    date: datetime
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="How similar to current conditions")
    spi_30_comparison: float
    spi_60_comparison: float
    outcome: str = Field(..., description="What happened after this similar period")
    lessons_learned: str

# Request models
class DroughtRiskRequest(BaseModel):
    lat: float = Field(..., ge=-47.0, le=-34.0, description="Latitude (NZ bounds)")
    lon: float = Field(..., ge=166.0, le=179.0, description="Longitude (NZ bounds)")
    region: Optional[str] = Field(None, description="NZ region name (auto-detected if not provided)")
    forecast_days: int = Field(14, ge=1, le=35, description="Forecast horizon")

class HistoricalAnalogsRequest(BaseModel):
    lat: float
    lon: float
    current_spi_30: float
    current_spi_60: float
    limit: int = Field(5, ge=1, le=20)