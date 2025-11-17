"""
Patch helper to inject Beast Mode orchestrator into Phase 2
"""
import asyncio
from infrastructure.parallel.beast_mode_orchestrator import orchestrator, Task


async def execute_scouts_parallel(scouts_data):
    tasks = []
    for scout in scouts_data:
        tasks.append(Task(id=scout.get('id', 'unknown'), prompt=scout.get('prompt', ''), max_tokens=4000))
    results = await orchestrator.execute_all(tasks)
    scout_results = []
    for r in results:
        scout_results.append({'id': r.task_id, 'provider': r.provider, 'response': r.response, 'success': r.success, 'latency': r.latency})
    return scout_results


def patch_phase2():
    try:
        import phase2_constitutional_swarm as p2
        # Replace the internal scout execution with parallel variant if present
        p2._single_agent_scout = None  # Defensive: avoid old single-agent path
        p2.execute_scouts_parallel = execute_scouts_parallel
        print("✅ Phase2 patched: execute_scouts_parallel available as p2.execute_scouts_parallel")
    except Exception as e:
        print(f"⚠️ Could not patch phase2: {e}")


if __name__ == '__main__':
    patch_phase2()
