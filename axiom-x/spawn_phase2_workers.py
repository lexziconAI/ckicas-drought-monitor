#!/usr/bin/env python3
"""
AXIOM-X PHASE 2 WORKER SPAWNER
=============================
Spawns Phase 2 specialized workers for the Constitutional Swarm architecture:
- Scout agents (270)
- Extractor agents (27)
- Validator agents (1350)

This is a lightweight in-memory spawner (workers are objects, not OS processes).
"""

import asyncio
import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WorkerConfig:
    worker_id: str
    worker_type: str
    specialization: str
    concurrency_limit: int

@dataclass
class WorkerStatus:
    worker_id: str
    status: str
    tasks_completed: int
    uptime_seconds: float

class Phase2Worker:
    def __init__(self, config: WorkerConfig):
        self.config = config
        self.status = WorkerStatus(
            worker_id=config.worker_id,
            status="initializing",
            tasks_completed=0,
            uptime_seconds=0.0
        )
        self.start_time = time.time()
        self.running = False

    async def start(self):
        self.running = True
        self.status.status = "active"
        self.start_time = time.time()
        logger.info(f"Started Phase2 worker {self.config.worker_id}")

    def update_status(self):
        self.status.uptime_seconds = time.time() - self.start_time

class Phase2Spawner:
    def __init__(self):
        self.workers: Dict[str, Phase2Worker] = {}

    def _generate_configs(self):
        configs: Dict[str, WorkerConfig] = {}

        # Scouts: 270 (10 per amendment)
        for i in range(1, 271):
            worker_id = f"scout_{i:03d}"
            configs[worker_id] = WorkerConfig(worker_id, "scout", "source_discovery", 2)

        # Extractors: 27 (1 per amendment)
        for i in range(1, 28):
            worker_id = f"extractor_{i:02d}"
            configs[worker_id] = WorkerConfig(worker_id, "extractor", "canonical_extraction", 1)

        # Validators: 1350 (50 per amendment)
        for i in range(1, 1351):
            worker_id = f"validator_{i:04d}"
            configs[worker_id] = WorkerConfig(worker_id, "validator", "validation_hashing", 1)

        return configs

    async def spawn_all(self):
        configs = self._generate_configs()

        # Spawn in controlled batches to avoid huge synchronous work
        batch_size = 200
        keys = list(configs.keys())
        total = len(keys)
        logger.info(f"Spawning {total} Phase2 workers in batches of {batch_size}...")

        for i in range(0, total, batch_size):
            batch = keys[i:i+batch_size]
            tasks = []
            for wid in batch:
                cfg = configs[wid]
                w = Phase2Worker(cfg)
                self.workers[wid] = w
                tasks.append(w.start())

            # Start batch concurrently
            await asyncio.gather(*tasks)
            # Small pause between batches to reduce instantaneous load
            await asyncio.sleep(0.05)
            logger.info(f"Spawned batch {i//batch_size + 1}: {len(batch)} workers")

        logger.info(f"All Phase2 workers spawned: {len(self.workers)}")
        return self.workers

    def get_status_report(self) -> Dict[str, Any]:
        for w in self.workers.values():
            w.update_status()

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_workers": len(self.workers),
            "active_workers": len([w for w in self.workers.values() if w.status.status == 'active']),
            "worker_status": {wid: asdict(w.status) for wid, w in self.workers.items()}
        }
        return report

async def main():
    spawner = Phase2Spawner()
    await spawner.spawn_all()

    report = spawner.get_status_report()
    with open('infrastructure_workers_phase2.json', 'w') as f:
        json.dump(report, f, indent=2)

    print(f"✅ Phase 2 workers spawned: {report['total_workers']}")
    print("💾 Status written to infrastructure_workers_phase2.json")

if __name__ == '__main__':
    asyncio.run(main())
