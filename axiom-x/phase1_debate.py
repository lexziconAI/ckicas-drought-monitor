#!/usr/bin/env python3
"""
Phase 1 Debate Runner for Axiom-X Self-Optimization
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.orchestrator import Phase1Orchestrator, run_phase1_debate

async def main():
    parser = argparse.ArgumentParser(description='Run Phase 1 Debate')
    parser.add_argument('--mission-file', required=True, help='Path to mission file')
    parser.add_argument('--output', required=True, help='Output JSON file')
    parser.add_argument('--force-close-after', type=int, help='Force close after N rounds')
    parser.add_argument('--max-rounds', type=int, default=20, help='Maximum rounds')

    args = parser.parse_args()

    # Read mission file
    with open(args.mission_file, 'r', encoding='utf-8') as f:
        mission_content = f.read()

    print(f"Starting Phase 1 Debate with mission from {args.mission_file}")
    print("Mission preview:")
    print(mission_content[:500] + "..." if len(mission_content) > 500 else mission_content)

    # Initialize orchestrator
    orchestrator = Phase1Orchestrator()

    # Run the debate (this will use the mission content somehow - orchestrator needs to be modified if needed)
    # For now, just run it and capture output
    try:
        result = await run_phase1_debate(mission_file=args.mission_file)

        # Save result
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"Phase 1 complete. Output saved to {args.output}")

    except Exception as e:
        print(f"Error running Phase 1: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())