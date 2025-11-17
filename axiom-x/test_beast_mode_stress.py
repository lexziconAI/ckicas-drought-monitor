"""
Quick stress test for BeastModeOrchestrator: simulate N tasks and report throughput.
"""
import asyncio
import time
from infrastructure.parallel.beast_mode_orchestrator import orchestrator, Task

async def run_test(n=600):
    tasks = [Task(id=str(i), prompt=f"Test {i}") for i in range(n)]
    start = time.time()
    results = await orchestrator.execute_all(tasks)
    end = time.time()
    succeeded = sum(1 for r in results if r.success)
    print(f"Ran {n} tasks in {end-start:.2f}s - succeeded: {succeeded}/{n}")

if __name__ == '__main__':
    asyncio.run(run_test(600))
