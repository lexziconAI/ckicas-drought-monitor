#!/usr/bin/env python3
"""
Background Job: Fetch NIWA Data Daily
Constitutional AI implementation for automated data collection
"""

import asyncio
import logging
import os
from datetime import datetime
from app.agents.niwa_datahub_agent import NIWADataHubAgent
from app.models.database import create_tables, get_db_session
from app.services.cache import brahmacharya_cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def fetch_niwa_data():
    """
    Daily job to fetch fresh NIWA data for key locations.
    Implements Brahmacharya caching to avoid unnecessary API calls.
    """
    logger.info("Starting daily NIWA data fetch job")

    # Key locations to monitor (major farming regions)
    locations = [
        {"name": "Auckland", "lat": -36.8485, "lon": 174.7633},
        {"name": "Hamilton", "lat": -37.7833, "lon": 175.2833},
        {"name": "Wellington", "lat": -41.2865, "lon": 174.7762},
        {"name": "Christchurch", "lat": -43.5321, "lon": 172.6362},
        {"name": "Dunedin", "lat": -45.8788, "lon": 170.5028},
        {"name": "Invercargill", "lat": -46.4132, "lon": 168.3538},
        {"name": "Whangarei", "lat": -35.7251, "lon": 174.3237},
        {"name": "New Plymouth", "lat": -39.0556, "lon": 174.0752},
        {"name": "Napier", "lat": -39.4928, "lon": 176.9120},
        {"name": "Queenstown", "lat": -45.0312, "lon": 168.6626}
    ]

    agent = NIWADataHubAgent()
    db_session = await get_db_session()

    try:
        for location in locations:
            logger.info(f"Fetching NIWA data for {location['name']}")

            # Fetch rainfall data with Brahmacharya caching
            rainfall_key = f"niwa_rainfall_{location['name'].lower()}"
            rainfall_data, was_cached = await brahmacharya_cache.get_or_compute(
                key=rainfall_key,
                compute_func=lambda: agent.fetch_90day_rainfall(location['lat'], location['lon']),
                ttl_hours=24,  # Daily refresh
                source_freshness_hours=12  # NIWA data freshness
            )

            # Fetch temperature data
            temp_key = f"niwa_temperature_{location['name'].lower()}"
            temp_data, was_cached_temp = await brahmacharya_cache.get_or_compute(
                key=temp_key,
                compute_func=lambda: agent.fetch_90day_temperature(location['lat'], location['lon']),
                ttl_hours=24,
                source_freshness_hours=12
            )

            # Store in database if needed (for historical analysis)
            # Implementation depends on database schema

            logger.info(f"Completed {location['name']}: rainfall={'cached' if was_cached else 'fetched'}, "
                       f"temperature={'cached' if was_cached_temp else 'fetched'}")

        # Clear expired cache entries
        await brahmacharya_cache.clear_expired()

        # Log Brahmacharya efficiency
        stats = brahmacharya_cache.get_stats()
        logger.info(f"Brahmacharya efficiency: {stats['api_calls_saved']} API calls saved, "
                   f"{stats['hit_rate']:.1%} cache hit rate")

    except Exception as e:
        logger.error(f"NIWA data fetch job failed: {e}")
        raise
    finally:
        await db_session.close()

async def main():
    """Main job execution"""
    try:
        # Ensure database tables exist
        await create_tables()

        # Run the data fetch
        await fetch_niwa_data()

        logger.info("NIWA data fetch job completed successfully")

    except Exception as e:
        logger.error(f"NIWA data fetch job failed: {e}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())