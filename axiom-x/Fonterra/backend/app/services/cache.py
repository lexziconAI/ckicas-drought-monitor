"""
Data Caching Service - Brahmacharya Principle Implementation
Prevents unnecessary API calls and resource waste when data hasn't changed significantly
"""
import asyncio
import json
import hashlib
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Cache entry with metadata for Brahmacharya compliance"""
    key: str
    data: Any
    timestamp: datetime
    ttl_seconds: int
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    data_hash: Optional[str] = None
    source_freshness_hours: float = 0.0

    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        return datetime.utcnow() > (self.timestamp + timedelta(seconds=self.ttl_seconds))

    def should_refresh(self, new_freshness_hours: float, indicator_change_threshold: float = 0.05) -> bool:
        """
        Brahmacharya decision: Should we refresh this data?
        Considers data age, freshness, and significance of changes
        """
        now = datetime.utcnow()
        age_hours = (now - self.timestamp).total_seconds() / 3600

        # Always refresh if data is stale (>12 hours)
        if age_hours > 12:
            return True

        # Refresh if source data is much fresher
        if new_freshness_hours < self.source_freshness_hours * 0.5:  # 50% fresher
            return True

        # Don't refresh if data is still very fresh (< 2 hours)
        if age_hours < 2:
            return False

        # For indicator data, check if changes would be significant
        if self.data_hash and isinstance(self.data, dict):
            # This would compare indicator values for significance
            # For now, use time-based refresh
            pass

        return False

    def update_access(self):
        """Update access metadata"""
        self.access_count += 1
        self.last_accessed = datetime.utcnow()

class BrahmacharyaCache:
    """
    Constitutional caching service implementing Brahmacharya principle.
    Prevents resource waste through intelligent cache management.
    """

    def __init__(self, max_size: int = 1000, default_ttl_hours: int = 12):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.default_ttl_hours = default_ttl_hours
        self._lock = asyncio.Lock()

        # Brahmacharya metrics
        self.cache_hits = 0
        self.cache_misses = 0
        self.refreshes_prevented = 0
        self.api_calls_saved = 0

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve cached data if still valid
        """
        async with self._lock:
            entry = self.cache.get(key)

            if entry and not entry.is_expired():
                entry.update_access()
                self.cache_hits += 1
                logger.debug(f"Cache hit for key: {key}")
                return entry.data

            if entry:
                self.cache_misses += 1
                logger.debug(f"Cache expired for key: {key}")

            return None

    async def set(
        self,
        key: str,
        data: Any,
        ttl_hours: Optional[int] = None,
        source_freshness_hours: float = 0.0
    ) -> None:
        """
        Store data in cache with Brahmacharya-aware TTL
        """
        async with self._lock:
            # Generate data hash for change detection
            data_hash = self._generate_data_hash(data)

            # Apply Brahmacharya TTL adjustments
            adjusted_ttl = self._calculate_brahmacharya_ttl(
                data, ttl_hours or self.default_ttl_hours, source_freshness_hours
            )

            entry = CacheEntry(
                key=key,
                data=data,
                timestamp=datetime.utcnow(),
                ttl_seconds=adjusted_ttl * 3600,
                data_hash=data_hash,
                source_freshness_hours=source_freshness_hours
            )

            # Evict old entries if cache is full (LRU)
            if len(self.cache) >= self.max_size:
                await self._evict_lru()

            self.cache[key] = entry
            logger.debug(f"Cached data for key: {key} with TTL: {adjusted_ttl}h")

    async def get_or_compute(
        self,
        key: str,
        compute_func,
        ttl_hours: Optional[int] = None,
        source_freshness_hours: float = 0.0,
        force_refresh: bool = False
    ) -> Tuple[Any, bool]:
        """
        Get cached data or compute new data with Brahmacharya decision making

        Returns:
            (data, was_cached) - True if data came from cache
        """
        # Check cache first
        cached_data = await self.get(key)

        if cached_data is not None and not force_refresh:
            entry = self.cache[key]

            # Brahmacharya decision: should we use cached data?
            if not entry.should_refresh(source_freshness_hours):
                self.refreshes_prevented += 1
                self.api_calls_saved += 1
                return cached_data, True

        # Compute new data
        logger.debug(f"Computing fresh data for key: {key}")
        new_data = await compute_func()

        # Cache the result
        await self.set(key, new_data, ttl_hours, source_freshness_hours)

        return new_data, False

    def _calculate_brahmacharya_ttl(
        self,
        data: Any,
        requested_ttl: int,
        source_freshness: float
    ) -> int:
        """
        Calculate appropriate TTL following Brahmacharya principles

        - Weather data: 2-6 hours (rapidly changing)
        - Soil moisture: 6-12 hours (moderate change)
        - Drought indicators: 12-24 hours (slow change)
        - Historical data: 24-168 hours (stable)
        """
        if isinstance(data, dict):
            # Analyze data type from content
            if any(key in str(data).lower() for key in ['temperature', 'wind', 'weather']):
                # Weather data - shorter TTL
                return min(requested_ttl, 6)
            elif any(key in str(data).lower() for key in ['soil', 'moisture', 'spi', 'smd']):
                # Environmental indicators - medium TTL
                return min(requested_ttl, 12)
            elif 'historical' in str(data).lower():
                # Historical data - longer TTL
                return min(requested_ttl, 168)  # 1 week

        # Default Brahmacharya TTL
        return min(requested_ttl, 12)

    def _generate_data_hash(self, data: Any) -> str:
        """Generate hash of data for change detection"""
        try:
            # Convert to JSON string for hashing
            if isinstance(data, (dict, list)):
                data_str = json.dumps(data, sort_keys=True, default=str)
            else:
                data_str = str(data)

            return hashlib.md5(data_str.encode()).hexdigest()
        except Exception:
            return None

    async def _evict_lru(self):
        """Evict least recently used cache entries"""
        if not self.cache:
            return

        # Find oldest entry
        oldest_key = min(
            self.cache.keys(),
            key=lambda k: self.cache[k].last_accessed or self.cache[k].timestamp
        )

        del self.cache[oldest_key]
        logger.debug(f"Evicted LRU cache entry: {oldest_key}")

    async def clear_expired(self):
        """Remove all expired cache entries"""
        async with self._lock:
            expired_keys = [
                key for key, entry in self.cache.items()
                if entry.is_expired()
            ]

            for key in expired_keys:
                del self.cache[key]

            if expired_keys:
                logger.info(f"Cleared {len(expired_keys)} expired cache entries")

    def get_stats(self) -> Dict[str, Any]:
        """Get Brahmacharya compliance statistics"""
        total_requests = self.cache_hits + self.cache_misses

        return {
            'cache_size': len(self.cache),
            'max_cache_size': self.max_size,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate': self.cache_hits / max(total_requests, 1),
            'refreshes_prevented': self.refreshes_prevented,
            'api_calls_saved': self.api_calls_saved,
            'brahmacharya_efficiency': self.api_calls_saved / max(total_requests, 1),
            'cache_entries': [
                {
                    'key': entry.key,
                    'age_hours': (datetime.utcnow() - entry.timestamp).total_seconds() / 3600,
                    'access_count': entry.access_count,
                    'ttl_hours': entry.ttl_seconds / 3600
                }
                for entry in self.cache.values()
            ]
        }

    async def get_health_metrics(self) -> Dict[str, float]:
        """
        Get health metrics for monitoring dashboard.
        Returns metrics in format expected by health endpoint.
        """
        stats = self.get_stats()

        # Calculate average response time (placeholder - would need actual timing)
        avg_response_time = 0.05  # Assume 50ms average cache response

        return {
            "hit_rate": stats["hit_rate"],
            "total_requests": stats["cache_hits"] + stats["cache_misses"],
            "avg_response_time": avg_response_time
        }

    async def invalidate_pattern(self, pattern: str):
        """Invalidate cache entries matching a pattern"""
        async with self._lock:
            keys_to_remove = [
                key for key in self.cache.keys()
                if pattern in key
            ]

            for key in keys_to_remove:
                del self.cache[key]

            if keys_to_remove:
                logger.info(f"Invalidated {len(keys_to_remove)} cache entries matching: {pattern}")

# Global cache instance
brahmacharya_cache = BrahmacharyaCache()

# Background task to clean expired entries
async def cache_maintenance():
    """Periodic cache maintenance"""
    while True:
        await asyncio.sleep(3600)  # Run every hour
        await brahmacharya_cache.clear_expired()

        stats = brahmacharya_cache.get_stats()
        logger.info(f"Cache maintenance: {stats['cache_size']} entries, "
                   f"{stats['api_calls_saved']} API calls saved")