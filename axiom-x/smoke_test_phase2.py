#!/usr/bin/env python3
import asyncio
from phase2_swarm_coordinator import Phase2SwarmCoordinator

async def smoke():
    print('🧪 Starting Phase2 smoke test (short)')
    coordinator = Phase2SwarmCoordinator()
    await coordinator.initialize_swarm()
    print('✅ initialize_swarm complete')
    await coordinator.assign_tasks()
    print('✅ assign_tasks complete')
    # Run execute_tasks which now uses PHASE2_BATCH_SIZE (default 600)
    await coordinator.execute_tasks()
    print('🧪 Smoke test complete')

if __name__ == '__main__':
    asyncio.run(smoke())
