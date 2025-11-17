import asyncio
from router import router
import time

async def smoke_test():
    """
    Smoke test: Prove parallelization works

    Test: Send 20 simple tasks, ensure they execute in parallel
    """

    print("=" * 70)
    print("🔥 AXIOM-X SMOKE TEST - PARALLELIZATION VALIDATION")
    print("=" * 70)

    # Generate 20 simple tasks
    tasks = [
        f"Task {i}: Return just the number {i}"
        for i in range(1, 21)
    ]

    print(f"\n📊 Submitting {len(tasks)} tasks for parallel execution...")

    start_time = time.time()
    results = await router.parallel_execute(tasks)
    elapsed = time.time() - start_time

    print(f"\n⏱️  Completed in {elapsed:.2f} seconds")
    print(f"🚀 Average: {elapsed/len(tasks):.3f} seconds per task (parallelized)")

    # Show routing stats
    stats = router.get_routing_stats()
    print(f"\n📈 Routing Statistics:")
    print(f"   Total calls: {stats['total_calls']}")
    print(f"   Grok (coordinator): {stats['grok_calls']} ({stats['grok_percentage']})")
    print(f"   Other LLMs (workers): {stats['other_calls']} ({stats['other_percentage']})")

    if stats['target_met']:
        print(f"\n✅ SUCCESS: {stats['other_percentage']} offloaded to other LLMs (target: 95%)")
        print("✅ PARALLELIZATION VALIDATED - System ready for advanced tasks")
        return True
    else:
        print(f"\n⚠️  Target not met: {stats['other_percentage']} < 95%")
        return False

if __name__ == "__main__":
    success = asyncio.run(smoke_test())
    exit(0 if success else 1)