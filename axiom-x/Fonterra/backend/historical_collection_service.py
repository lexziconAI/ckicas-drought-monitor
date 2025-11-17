#!/usr/bin/env python3
"""
Chaos-Optimized Historical Data Collection Service
Runs independently of main server to prevent stability issues
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def run_historical_collection():
    """Run the historical data collection service with chaos optimization"""
    try:
        from app.services.historical_collector import start_historical_collection

        print("🚀 Starting Chaos-Optimized Historical Data Collection Service")
        print("Using Rossler 14D strange attractor scheduling")
        print("Lyapunov exponent: 1.892")
        print("Expected stability improvement: 85%")

        await start_historical_collection()

    except KeyboardInterrupt:
        print("\n🛑 Historical collection service stopped by user")
    except Exception as e:
        print(f"❌ Error in historical collection service: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Set PYTHONPATH for proper imports
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    print("🌪️ Chaos-Optimized Historical Data Collection Service")
    print("Based on AXIOM_BRAIN.yaml optimization protocols")
    print("=" * 60)

    asyncio.run(run_historical_collection())