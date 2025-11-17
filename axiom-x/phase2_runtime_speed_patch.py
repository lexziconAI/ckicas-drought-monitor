"""
Runtime speed patch to increase BeastModeOrchestrator provider semaphores
Run while Phase 2 is active to immediately increase concurrency.
"""
import asyncio
import json
import os
from importlib import reload

from infrastructure.parallel import beast_mode_orchestrator as bmo

# Desired per-provider limits
PATCH = {
    'anthropic': 150,
    'openai': 150,
    'google': 100,
    'groq': 200,
    'cohere': 100,
    'fireworks': 100,
}

print("Phase2 runtime speed patch starting...")

# Update orchestrator max_workers
try:
    o = bmo.orchestrator
    o.max_workers = max(PATCH.values())
    print(f"Set orchestrator.max_workers = {o.max_workers}")

    # Replace semaphores per provider
    for p, limit in PATCH.items():
        if p in o.providers:
            old = o.providers[p].get('semaphore')
            o.providers[p]['semaphore'] = asyncio.Semaphore(limit)
            print(f"Updated provider {p} semaphore: {limit}")
        else:
            o.providers[p] = {'semaphore': asyncio.Semaphore(limit), 'speed': 1.0}
            print(f"Added provider {p} with semaphore {limit}")

    # Optionally increase groq/fireworks multiplier
    if 'groq' in o.providers:
        o.providers['groq']['semaphore'] = asyncio.Semaphore(PATCH.get('groq', 100))
    if 'fireworks' in o.providers:
        o.providers['fireworks']['semaphore'] = asyncio.Semaphore(PATCH.get('fireworks', 100))

    print("✅ Runtime semaphores patched. New provider limits:")
    for p, cfg in o.providers.items():
        sem = cfg.get('semaphore')
        # best-effort introspection
        lim = getattr(sem, '_value', 'unknown')
        print(f"  - {p}: {lim}")

except Exception as e:
    print("⚠️ Failed to patch orchestrator at runtime:", e)
    raise

print("Phase2 runtime speed patch complete.")
