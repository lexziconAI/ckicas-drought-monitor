import asyncio
from infrastructure.parallel.beast_mode_orchestrator import orchestrator, Task


async def benchmark(n=1000):
    tasks = [Task(id=f"{i}", prompt=f"Return exactly: TASK_{i}_COMPLETE", max_tokens=50) for i in range(n)]
    print(f"🔥 BEAST MODE BENCHMARK: {n} parallel tasks (SIMULATE={orchestrator.simulate})")
    start = time = None
    start = __import__('time').time()
    results = await orchestrator.execute_all(tasks)
    end = __import__('time').time()
    success = sum(1 for r in results if r.success)
    print(f"\n✅ Verification: {success}/{len(tasks)} successful")
    print(f"Elapsed: {end - start:.2f}s")


if __name__ == '__main__':
    # Use 1000 as requested; reduce if running is too heavy
    asyncio.run(benchmark(1000))
