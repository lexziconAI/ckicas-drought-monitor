#!/usr/bin/env python3
"""
Background Job: Fetch Council Sensor Data Hourly
Constitutional AI implementation for automated environmental monitoring
"""

import asyncio
import logging
import os
from datetime import datetime
from app.agents.council_agent import CouncilDataAgent
from app.models.database import create_tables, get_db_session
from app.services.cache import brahmacharya_cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def fetch_council_data():
    """
    Hourly job to fetch fresh council sensor data.
    Implements Brahmacharya caching for efficiency.
    """
    logger.info("Starting hourly council data fetch job")

    # Regional councils to monitor
    councils = [
        "Waikato",
        "Auckland",
        "Bay of Plenty",
        "Canterbury",
        "Otago",
        "Southland",
        "Manawatu-Wanganui",
        "Hawke's Bay",
        "Northland",
        "Taranaki"
    ]

    agent = CouncilDataAgent()
    db_session = await get_db_session()

    try:
        for council in councils:
            logger.info(f"Fetching sensor data for {council} region")

            # Fetch sensor data with Brahmacharya caching
            sensor_key = f"council_sensors_{council.lower()}"
            sensor_data, was_cached = await brahmacharya_cache.get_or_compute(
                key=sensor_key,
                compute_func=lambda: agent.fetch_sensor_data(council, days=7),
                ttl_hours=6,  # Council data updates frequently
                source_freshness_hours=1  # Council sensors are near real-time
            )

            # Store in database if needed
            # Implementation depends on database schema

            logger.info(f"Completed {council}: {'cached' if was_cached else 'fetched'}")

        # Clear expired cache entries
        await brahmacharya_cache.clear_expired()

        # Log Brahmacharya efficiency
        stats = brahmacharya_cache.get_stats()
        logger.info(f"Brahmacharya efficiency: {stats['api_calls_saved']} API calls saved, "
                   f"{stats['hit_rate']:.1%} cache hit rate")

    except Exception as e:
        logger.error(f"Council data fetch job failed: {e}")
        raise
    finally:
        await db_session.close()

async def main():
    """Main job execution"""
    try:
        # Ensure database tables exist
        await create_tables()

        # Run the data fetch
        await fetch_council_data()

        logger.info("Council data fetch job completed successfully")

    except Exception as e:
        logger.error(f"Council data fetch job failed: {e}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())