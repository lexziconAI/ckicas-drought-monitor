#!/usr/bin/env python3
"""
AXIOM-X WORKER SPAWNER: Infrastructure Development Army
=======================================================

Spawns specialized workers for infrastructure design and build tasks.
Creates parallel processing units optimized for Axiom-X development.

Capabilities:
- Infrastructure architecture design
- Code generation and optimization
- Testing and validation
- Documentation and deployment
- Parallel execution coordination
"""

import os
import asyncio
import json
import time
import subprocess
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
import logging

# Add project paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'infrastructure'))

from infrastructure.sidecar.router import router

# TURBO MODE CONFIGURATION
TURBO_MODE = True
MAX_INFRASTRUCTURE_WORKERS = 100 if TURBO_MODE else 11
CONCURRENT_TASKS_PER_WORKER = 5 if TURBO_MODE else 1

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('worker_spawner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class WorkerConfig:
    """Configuration for a worker instance"""
    worker_id: str
    worker_type: str
    specialization: str
    concurrency_limit: int
    memory_limit: int
    task_queue_size: int
    heartbeat_interval: int

@dataclass
class WorkerStatus:
    """Status of a worker instance"""
    worker_id: str
    status: str  # active, idle, error, terminated
    tasks_completed: int
    tasks_failed: int
    uptime_seconds: float
    memory_usage: int
    cpu_usage: float
    last_heartbeat: datetime
    current_task: Optional[str] = None

class InfrastructureWorker:
    """Specialized worker for infrastructure development tasks"""

    def __init__(self, config: WorkerConfig):
        self.config = config
        self.status = WorkerStatus(
            worker_id=config.worker_id,
            status="initializing",
            tasks_completed=0,
            tasks_failed=0,
            uptime_seconds=0,
            memory_usage=0,
            cpu_usage=0.0,
            last_heartbeat=datetime.now()
        )
        self.task_queue = asyncio.Queue(maxsize=config.task_queue_size)
        self.executor = ThreadPoolExecutor(max_workers=config.concurrency_limit)
        self.start_time = time.time()
        self.running = False

    async def start(self):
        """Start the worker"""
        self.running = True
        logger.info(f"Starting worker {self.config.worker_id} ({self.config.worker_type})")

        # Start heartbeat
        asyncio.create_task(self._heartbeat_loop())

        # Start task processing
        asyncio.create_task(self._process_tasks())

        self.status.status = "active"

    async def stop(self):
        """Stop the worker"""
        self.running = False
        self.status.status = "terminated"
        self.executor.shutdown(wait=True)
        logger.info(f"Stopped worker {self.config.worker_id}")

    async def submit_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a task to the worker"""
        if self.task_queue.full():
            raise Exception(f"Worker {self.config.worker_id} task queue is full")

        await self.task_queue.put(task)
        return {"status": "submitted", "worker_id": self.config.worker_id}

    async def _process_tasks(self):
        """Process tasks from the queue - FIXED"""
        while self.running:
            task = None
            try:
                # Wait for task with timeout
                task = await asyncio.wait_for(
                    self.task_queue.get(),
                    timeout=1.0
                )

                self.status.current_task = task.get('task_id', 'unknown')
                result = await self._execute_task(task)
                self.status.tasks_completed += 1

            except asyncio.TimeoutError:
                # No task available, continue polling
                continue
            except Exception as e:
                logger.error(f"Worker {self.config.worker_id} task error: {e}")
                self.status.tasks_failed += 1
            finally:
                self.status.current_task = None
                # Only mark done if we actually got a task
                if task is not None:
                    try:
                        self.task_queue.task_done()
                    except ValueError:
                        # Already marked done, ignore
                        pass

    async def _execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task"""
        task_type = task.get('type', 'unknown')

        if task_type == 'code_generation':
            return await self._generate_code(task)
        elif task_type == 'architecture_design':
            return await self._design_architecture(task)
        elif task_type == 'testing':
            return await self._run_tests(task)
        elif task_type == 'documentation':
            return await self._generate_docs(task)
        elif task_type == 'optimization':
            return await self._optimize_code(task)
        else:
            raise Exception(f"Unknown task type: {task_type}")

    async def _generate_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code using AI assistance"""
        prompt = task.get('prompt', '')
        language = task.get('language', 'python')
        complexity = task.get('complexity', 'medium')

        full_prompt = f"""
        Generate {language} code for: {prompt}
        Complexity level: {complexity}
        Requirements:
        - Clean, readable code
        - Proper error handling
        - Documentation
        - Follow best practices
        """

        # Use router to generate code
        result = await router.route_task(full_prompt, "auto", max_tokens=2000)

        return {
            "task_id": task.get('task_id'),
            "result": result.response,
            "language": language,
            "tokens_used": result.tokens
        }

    async def _design_architecture(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Design system architecture"""
        requirements = task.get('requirements', '')
        scope = task.get('scope', 'module')

        prompt = f"""
        Design {scope} architecture for: {requirements}
        Provide:
        - Component breakdown
        - Data flow diagram
        - Interface specifications
        - Scalability considerations
        - Security requirements
        """

        result = await router.route_task(prompt, "auto", max_tokens=1500)

        return {
            "task_id": task.get('task_id'),
            "architecture_design": result.response,
            "scope": scope
        }

    async def _run_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Run automated tests"""
        test_type = task.get('test_type', 'unit')
        target = task.get('target', '')

        # Execute tests using subprocess
        if test_type == 'unit':
            cmd = ['python', '-m', 'pytest', target, '-v']
        elif test_type == 'integration':
            cmd = ['python', '-m', 'pytest', target, '--tb=short']
        else:
            cmd = ['python', '-c', f"print('Running {test_type} tests for {target}')"]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        return {
            "task_id": task.get('task_id'),
            "test_type": test_type,
            "exit_code": process.returncode,
            "stdout": stdout.decode(),
            "stderr": stderr.decode()
        }

    async def _generate_docs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate documentation"""
        target = task.get('target', '')
        doc_type = task.get('doc_type', 'api')

        prompt = f"Generate {doc_type} documentation for: {target}"

        result = await router.route_task(prompt, "auto", max_tokens=1000)

        return {
            "task_id": task.get('task_id'),
            "documentation": result.response,
            "doc_type": doc_type
        }

    async def _optimize_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize existing code"""
        code = task.get('code', '')
        optimization_type = task.get('optimization_type', 'performance')

        prompt = f"""
        Optimize this code for {optimization_type}:

        {code}

        Provide:
        - Optimized version
        - Performance improvements
        - Trade-offs considered
        """

        result = await router.route_task(prompt, "auto", max_tokens=1500)

        return {
            "task_id": task.get('task_id'),
            "optimized_code": result.response,
            "optimization_type": optimization_type
        }

    async def _heartbeat_loop(self):
        """Send periodic heartbeats"""
        while self.running:
            await asyncio.sleep(self.config.heartbeat_interval)
            self.status.last_heartbeat = datetime.now()
            self.status.uptime_seconds = time.time() - self.start_time

            # Update resource usage (simplified)
            self.status.memory_usage = 100 + (self.status.tasks_completed * 10)
            self.status.cpu_usage = 5.0 + (self.status.tasks_completed * 0.1)

class WorkerSpawner:
    """Manages spawning and coordinating multiple workers"""

    def __init__(self):
        self.workers: Dict[str, InfrastructureWorker] = {}
        self.worker_configs = self._load_worker_configs()
        self.coordination_semaphore = asyncio.Semaphore(10)  # Max 10 concurrent coordination tasks

    def _load_worker_configs(self) -> Dict[str, WorkerConfig]:
        """Load worker configurations"""
        return {
            # Code generation workers
            "code_gen_python": WorkerConfig(
                worker_id="code_gen_python",
                worker_type="code_generation",
                specialization="python",
                concurrency_limit=3,
                memory_limit=512,
                task_queue_size=50,
                heartbeat_interval=30
            ),
            "code_gen_javascript": WorkerConfig(
                worker_id="code_gen_javascript",
                worker_type="code_generation",
                specialization="javascript",
                concurrency_limit=3,
                memory_limit=512,
                task_queue_size=50,
                heartbeat_interval=30
            ),
            "code_gen_infrastructure": WorkerConfig(
                worker_id="code_gen_infrastructure",
                worker_type="code_generation",
                specialization="infrastructure",
                concurrency_limit=2,
                memory_limit=1024,
                task_queue_size=30,
                heartbeat_interval=30
            ),

            # Architecture design workers
            "arch_design_system": WorkerConfig(
                worker_id="arch_design_system",
                worker_type="architecture_design",
                specialization="system_architecture",
                concurrency_limit=2,
                memory_limit=1024,
                task_queue_size=20,
                heartbeat_interval=45
            ),
            "arch_design_api": WorkerConfig(
                worker_id="arch_design_api",
                worker_type="architecture_design",
                specialization="api_design",
                concurrency_limit=3,
                memory_limit=512,
                task_queue_size=40,
                heartbeat_interval=30
            ),

            # Testing workers
            "test_unit": WorkerConfig(
                worker_id="test_unit",
                worker_type="testing",
                specialization="unit_tests",
                concurrency_limit=5,
                memory_limit=256,
                task_queue_size=100,
                heartbeat_interval=20
            ),
            "test_integration": WorkerConfig(
                worker_id="test_integration",
                worker_type="testing",
                specialization="integration_tests",
                concurrency_limit=2,
                memory_limit=1024,
                task_queue_size=20,
                heartbeat_interval=60
            ),

            # Documentation workers
            "docs_api": WorkerConfig(
                worker_id="docs_api",
                worker_type="documentation",
                specialization="api_docs",
                concurrency_limit=4,
                memory_limit=256,
                task_queue_size=80,
                heartbeat_interval=25
            ),
            "docs_architecture": WorkerConfig(
                worker_id="docs_architecture",
                worker_type="documentation",
                specialization="architecture_docs",
                concurrency_limit=2,
                memory_limit=512,
                task_queue_size=30,
                heartbeat_interval=40
            ),

            # Optimization workers
            "optimize_performance": WorkerConfig(
                worker_id="optimize_performance",
                worker_type="optimization",
                specialization="performance",
                concurrency_limit=2,
                memory_limit=1024,
                task_queue_size=25,
                heartbeat_interval=50
            ),
            "optimize_security": WorkerConfig(
                worker_id="optimize_security",
                worker_type="optimization",
                specialization="security",
                concurrency_limit=2,
                memory_limit=512,
                task_queue_size=20,
                heartbeat_interval=45
            )
        }

    async def spawn_workers(self, worker_types: List[str] = None) -> Dict[str, str]:
        """Spawn workers of specified types - TURBO MODE"""
        if worker_types is None:
            if not TURBO_MODE:
                # Original 11 workers
                worker_types = list(self.worker_configs.keys())
            else:
                # TURBO: 100 workers across all specialties
                worker_types = []
                # 30 code generators
                for i in range(30):
                    worker_types.append(f"code_gen_{i}")
                # 20 architecture designers
                for i in range(20):
                    worker_types.append(f"arch_design_{i}")
                # 20 testers
                for i in range(20):
                    worker_types.append(f"test_{i}")
                # 15 documentation writers
                for i in range(15):
                    worker_types.append(f"docs_{i}")
                # 15 optimizers
                for i in range(15):
                    worker_types.append(f"optimize_{i}")

        spawned = {}
        for worker_id in worker_types:
            if worker_id in self.worker_configs or TURBO_MODE:
                if TURBO_MODE and worker_id not in self.worker_configs:
                    # Create dynamic config for TURBO mode
                    worker_type = worker_id.split('_')[0] if '_' in worker_id else 'code_gen'
                    config = WorkerConfig(
                        worker_id=worker_id,
                        worker_type=worker_type,
                        specialization=f"{worker_type}_specialist",
                        concurrency_limit=CONCURRENT_TASKS_PER_WORKER,
                        memory_limit=512,
                        task_queue_size=50,
                        heartbeat_interval=30
                    )
                else:
                    config = self.worker_configs[worker_id]

                worker = InfrastructureWorker(config)
                self.workers[worker_id] = worker
                await worker.start()
                spawned[worker_id] = "active"
                logger.info(f"Spawned worker: {worker_id}")

        return spawned

    async def submit_infrastructure_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a task to the most appropriate worker"""
        async with self.coordination_semaphore:
            task_type = task.get('type', 'unknown')

            # Find best worker for task
            best_worker = self._find_best_worker(task_type)
            if not best_worker:
                raise Exception(f"No suitable worker found for task type: {task_type}")

            return await self.workers[best_worker].submit_task(task)

    def _find_best_worker(self, task_type: str) -> Optional[str]:
        """Find the best worker for a task type"""
        candidates = []

        for worker_id, worker in self.workers.items():
            if worker.status.status != "active":
                continue

            # Check if worker can handle this task type
            if worker.config.worker_type == task_type:
                candidates.append((worker_id, worker))

        if not candidates:
            return None

        # Return worker with least tasks in queue
        return min(candidates, key=lambda x: x[1].task_queue.qsize())[0]

    def get_worker_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all workers"""
        status = {}
        for worker_id, worker in self.workers.items():
            status[worker_id] = asdict(worker.status)
        return status

    async def shutdown_all_workers(self):
        """Shutdown all workers"""
        shutdown_tasks = []
        for worker in self.workers.values():
            shutdown_tasks.append(worker.stop())

        await asyncio.gather(*shutdown_tasks, return_exceptions=True)
        logger.info("All workers shut down")

async def main():
    """Main function to spawn infrastructure development workers - TURBO MODE"""
    print("🌀 AXIOM-X WORKER SPAWNER: Infrastructure Development Army")
    print("=" * 70)
    print(f"🚀 TURBO MODE: {'ENABLED' if TURBO_MODE else 'DISABLED'}")
    print(f"🎯 Target Workers: {MAX_INFRASTRUCTURE_WORKERS}")
    print("=" * 70)

    spawner = WorkerSpawner()

    # Spawn all worker types
    print("🚀 Spawning infrastructure development workers...")

    if not TURBO_MODE:
        # Original spawning logic
        core_workers = [
            "code_gen_python",
            "code_gen_infrastructure",
            "arch_design_system",
            "arch_design_api",
            "test_unit",
            "docs_api"
        ]

        spawned = await spawner.spawn_workers(core_workers)

        print(f"✅ Spawned {len(spawned)} core workers:")
        for worker_id, status in spawned.items():
            print(f"   - {worker_id}: {status}")

        # Spawn additional specialized workers
        print("\n🚀 Spawning specialized workers...")
        specialized_workers = [
            "code_gen_javascript",
            "test_integration",
            "docs_architecture",
            "optimize_performance",
            "optimize_security"
        ]

        spawned_specialized = await spawner.spawn_workers(specialized_workers)

        print(f"✅ Spawned {len(spawned_specialized)} specialized workers:")
        for worker_id, status in spawned_specialized.items():
            print(f"   - {worker_id}: {status}")
    else:
        # TURBO MODE: Spawn all 100 workers at once
        spawned = await spawner.spawn_workers()

        print(f"✅ Spawned {len(spawned)} workers in TURBO mode:")
        print(f"   📊 Code Generators: 30")
        print(f"   🏗️  Architecture Designers: 20")
        print(f"   🧪 Testers: 20")
        print(f"   📚 Documentation Writers: 15")
        print(f"   ⚡ Optimizers: 15")

    total_workers = len(spawner.workers)
    print(f"\n🎯 Total active workers: {total_workers}")

    # Save worker status
    status_report = {
        "timestamp": datetime.now().isoformat(),
        "total_workers": total_workers,
        "active_workers": len([w for w in spawner.workers.values() if w.status.status == "active"]),
        "turbo_mode": TURBO_MODE,
        "worker_status": spawner.get_worker_status()
    }

    with open("infrastructure_workers_status.json", 'w') as f:
        json.dump(status_report, f, indent=2, default=str)

    print("💾 Worker status saved to infrastructure_workers_status.json")

    # Submit some example infrastructure tasks
    print("\n🛠️ Submitting example infrastructure tasks...")

    example_tasks = [
        {
            "task_id": "infra_task_001",
            "type": "code_generation",
            "language": "python",
            "complexity": "high",
            "prompt": "Create a scalable API router with rate limiting and error handling for Axiom-X infrastructure"
        },
        {
            "task_id": "infra_task_002",
            "type": "architecture_design",
            "scope": "system",
            "requirements": "Design a distributed worker coordination system for parallel processing of AI tasks"
        },
        {
            "task_id": "infra_task_003",
            "type": "testing",
            "test_type": "unit",
            "target": "infrastructure/sidecar/router.py"
        }
    ]

    for task in example_tasks:
        try:
            result = await spawner.submit_infrastructure_task(task)
            print(f"   ✅ Submitted {task['task_id']}: {result['status']}")
        except Exception as e:
            print(f"   ❌ Failed to submit {task['task_id']}: {e}")

    print("\n⏳ Workers are now active and processing tasks...")
    print("Press Ctrl+C to shutdown workers")

    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(10)
            # Periodic status update
            status = spawner.get_worker_status()
            active_workers = sum(1 for s in status.values() if s['status'] == 'active')
            total_tasks = sum(s['tasks_completed'] for s in status.values())
            print(f"📊 Status: {active_workers} active workers, {total_tasks} tasks completed")

    except KeyboardInterrupt:
        print("\n🛑 Shutting down workers...")
        await spawner.shutdown_all_workers()
        print("✅ All workers shut down gracefully")

if __name__ == "__main__":
    asyncio.run(main())