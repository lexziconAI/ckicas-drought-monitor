# Database Models for NZ Drought Early Warning System
# Constitutional AI implementation with proper data attribution (Asteya)

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship
from sqlalchemy import String, Float, DateTime, Integer, ForeignKey, Index, func
from datetime import datetime
from typing import Optional, List
import os

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/drought.db")

# Async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Async session
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    """Base class for all database models"""
    pass

class TimeseriesMetric(Base):
    """
    Time-series storage for all drought indicators
    Optimized for: fast range queries, source attribution (Asteya)
    """
    __tablename__ = 'timeseries_metrics'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    location_lat: Mapped[float] = mapped_column(Float, nullable=False)
    location_lon: Mapped[float] = mapped_column(Float, nullable=False)
    region: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    metric_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)  # 'spi_30', 'smd', 'rainfall', etc.
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # 'mm', 'degrees', None for indices

    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey('data_sources.id'), nullable=False)  # Asteya: always cite source

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    source: Mapped["DataSource"] = relationship("DataSource", back_populates="metrics")

    # Composite index for common query pattern
    __table_args__ = (
        Index('idx_location_metric_time', 'location_lat', 'location_lon', 'metric_type', 'timestamp'),
    )

class DataSource(Base):
    """
    Source attribution table (Asteya principle)
    Every metric must reference a data source
    """
    __tablename__ = 'data_sources'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # 'NIWA_DataHub', 'Waikato_RC', 'OpenWeatherMap'
    dataset: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Specific dataset/station ID
    api_endpoint: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_fetched: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fetch_frequency_hours: Mapped[int] = mapped_column(Integer, default=24)  # How often to refresh (Brahmacharya)
    api_key_required: Mapped[str] = mapped_column(String(10), default='no')  # 'yes' or 'no' for Aparigraha compliance

    # Relationships
    metrics: Mapped[List["TimeseriesMetric"]] = relationship("TimeseriesMetric", back_populates="source")

class DroughtAlert(Base):
    """
    Alert history for tracking when drought conditions triggered
    Constitutional compliance: only HIGH confidence alerts are stored
    """
    __tablename__ = 'drought_alerts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    region: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    alert_level: Mapped[str] = mapped_column(String(20), nullable=False)  # 'WATCH', 'WARNING', 'CRITICAL'
    confidence: Mapped[str] = mapped_column(String(10), nullable=False)  # 'HIGH' only (Ahimsa principle)

    # Risk assessment at time of alert
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)  # 0-100
    spi_30: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    spi_60: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    smd_current: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    smd_anomaly: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    nzdi_category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Forecast context
    forecast_days: Mapped[int] = mapped_column(Integer, default=14)
    projected_smd_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    projected_smd_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Constitutional compliance tracking
    convergence_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 0.0-1.0 (Ahimsa)
    sources_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Asteya compliance
    yama_compliant: Mapped[str] = mapped_column(String(3), default='YES')  # 'YES' or 'NO'

    triggered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # User notification tracking (future feature)
    notifications_sent: Mapped[int] = mapped_column(Integer, default=0)
    farmer_acknowledgments: Mapped[int] = mapped_column(Integer, default=0)

class CacheEntry(Base):
    """
    Brahmacharya principle: Cache layer to prevent wasteful API calls
    """
    __tablename__ = 'cache_entries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cache_key: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    data: Mapped[str] = mapped_column(String, nullable=False)  # JSON serialized data
    data_hash: Mapped[str] = mapped_column(String(64), nullable=False)  # SHA256 for change detection

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    last_accessed: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    access_count: Mapped[int] = mapped_column(Integer, default=0)

    # Brahmacharya metrics
    api_calls_saved: Mapped[int] = mapped_column(Integer, default=0)
    data_freshness_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        return datetime.utcnow() > self.expires_at

    def should_refresh(self, change_threshold: float = 0.05) -> bool:
        """
        Brahmacharya: Determine if data should be refreshed
        Returns True if age > 12h OR change > 5%
        """
        age_hours = (datetime.utcnow() - self.created_at).total_seconds() / 3600
        return age_hours > 12  # Simplified: just check age for now

class SystemHealth(Base):
    """
    System health monitoring for constitutional compliance
    """
    __tablename__ = 'system_health'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    component: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # 'niwa_agent', 'api', 'database'
    metric: Mapped[str] = mapped_column(String(50), nullable=False)  # 'response_time', 'error_rate', 'cache_hit_rate'
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # 'ms', 'percent', 'count'

    # Constitutional compliance indicators
    yama_principle: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # 'ahimsa', 'satya', 'asteya', 'brahmacharya', 'aparigraha'
    compliance_status: Mapped[str] = mapped_column(String(10), default='compliant')  # 'compliant', 'warning', 'violation'

    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index('idx_component_metric_time', 'component', 'metric', 'recorded_at'),
    )
    farmer_acknowledgments: Mapped[int] = mapped_column(Integer, default=0)

async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    """Dependency for getting database session"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()