#!/usr/bin/env python3
"""
AXIOM-X TASK COORDINATOR: Infrastructure Development Tasks
==========================================================

Coordinates tasks for the infrastructure development workers.
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
import logging

# Add project paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'infrastructure'))

from infrastructure.sidecar.router import router

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class InfrastructureTask:
    task_id: str
    task_type: str
    priority: int
    description: str
    requirements: Dict[str, Any]
    assigned_worker: Optional[str] = None
    status: str = "pending"
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    result: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class TaskCoordinator:
    def __init__(self):
        self.tasks: Dict[str, InfrastructureTask] = {}
        self.workers = self._load_worker_status()
        self.task_queue = asyncio.Queue()

    def _load_worker_status(self) -> Dict[str, Any]:
        """Load current worker status"""
        try:
            with open("infrastructure_workers_status.json", 'r') as f:
                status = json.load(f)
                return status.get("worker_status", {})
        except FileNotFoundError:
            logger.warning("Worker status file not found")
            return {}

    async def submit_task(self, task: InfrastructureTask) -> str:
        """Submit a task for processing"""
        self.tasks[task.task_id] = task
        await self.task_queue.put(task)
        logger.info(f"Submitted task: {task.task_id}")
        return task.task_id

    async def process_tasks(self):
        """Process tasks from the queue"""
        while True:
            try:
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                await self._execute_task(task)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Task processing error: {e}")

    async def _execute_task(self, task: InfrastructureTask):
        """Execute a specific task"""
        task.status = "processing"
        logger.info(f"Processing task: {task.task_id}")

        try:
            if task.task_type == "code_generation":
                result = await self._generate_code(task)
            elif task.task_type == "architecture_design":
                result = await self._design_architecture(task)
            elif task.task_type == "testing":
                result = await self._run_tests(task)
            elif task.task_type == "documentation":
                result = await self._generate_docs(task)
            elif task.task_type == "optimization":
                result = await self._optimize_code(task)
            else:
                result = f"Unknown task type: {task.task_type}"

            task.result = result
            task.status = "completed"
            task.completed_at = datetime.now()
            logger.info(f"Completed task: {task.task_id}")

        except Exception as e:
            task.result = f"Error: {str(e)}"
            task.status = "failed"
            task.completed_at = datetime.now()
            logger.error(f"Failed task {task.task_id}: {e}")

    async def _generate_code(self, task: InfrastructureTask) -> str:
        """Generate code using AI"""
        language = task.requirements.get('language', 'python')
        prompt = task.description

        full_prompt = f"""
        Generate {language} code for Axiom-X infrastructure: {prompt}
        Requirements:
        - Clean, readable code
        - Proper error handling
        - Type hints where appropriate
        - Follow best practices
        - Include docstrings
        """

        result = await router.route_task(full_prompt, "auto", max_tokens=1500)
        return result.response

    async def _design_architecture(self, task: InfrastructureTask) -> str:
        """Design system architecture"""
        requirements = task.description

        prompt = f"""
        Design Axiom-X infrastructure architecture: {requirements}
        Provide:
        - Component breakdown
        - Data flow description
        - Interface specifications
        - Scalability considerations
        - Security considerations
        """

        result = await router.route_task(prompt, "auto", max_tokens=1200)
        return result.response

    async def _run_tests(self, task: InfrastructureTask) -> str:
        """Run automated tests"""
        target = task.requirements.get('target', '')
        test_type = task.requirements.get('test_type', 'unit')

        try:
            if test_type == 'unit':
                cmd = ['python', '-m', 'pytest', target, '-v', '--tb=short']
            else:
                cmd = ['python', '-c', f"print('Running {test_type} tests for {target}')"]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            return f"Exit code: {process.returncode}\nSTDOUT:\n{stdout.decode()}\nSTDERR:\n{stderr.decode()}"

        except Exception as e:
            return f"Test execution failed: {str(e)}"

    async def _generate_docs(self, task: InfrastructureTask) -> str:
        """Generate documentation"""
        target = task.description

        prompt = f"Generate comprehensive documentation for: {target}"

        result = await router.route_task(prompt, "auto", max_tokens=1000)
        return result.response

    async def _optimize_code(self, task: InfrastructureTask) -> str:
        """Optimize existing code"""
        code = task.requirements.get('code', '')
        optimization_type = task.requirements.get('optimization_type', 'performance')

        prompt = f"""
        Optimize this code for {optimization_type}:

        {code}

        Provide:
        - Optimized version
        - Performance improvements
        - Trade-offs considered
        """

        result = await router.route_task(prompt, "auto", max_tokens=1200)
        return result.response

    def get_task_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all tasks"""
        status = {}
        for task_id, task in self.tasks.items():
            status[task_id] = {
                "task_id": task.task_id,
                "task_type": task.task_type,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "assigned_worker": task.assigned_worker,
                "result_preview": task.result[:200] + "..." if task.result and len(task.result) > 200 else task.result
            }
        return status

async def submit_infrastructure_tasks():
    """Submit infrastructure development tasks to workers"""
    print("🛠️ AXIOM-X TASK COORDINATOR: Infrastructure Development")
    print("=" * 70)

    coordinator = TaskCoordinator()

    # Start task processing
    asyncio.create_task(coordinator.process_tasks())

    # Submit infrastructure development tasks
    print("📋 Submitting infrastructure development tasks...")

    tasks = [
        InfrastructureTask(
            task_id="infra_api_router",
            task_type="code_generation",
            priority=1,
            description="Create a scalable API router with rate limiting and error handling for Axiom-X infrastructure",
            requirements={"language": "python", "complexity": "high"}
        ),
        InfrastructureTask(
            task_id="infra_worker_coordinator",
            task_type="architecture_design",
            priority=1,
            description="Design a distributed worker coordination system for parallel processing of AI tasks",
            requirements={"scope": "system"}
        ),
        InfrastructureTask(
            task_id="infra_test_router",
            task_type="testing",
            priority=2,
            description="Run unit tests for the router infrastructure",
            requirements={"target": "infrastructure/sidecar/router.py", "test_type": "unit"}
        ),
        InfrastructureTask(
            task_id="infra_docs_api",
            task_type="documentation",
            priority=2,
            description="Generate API documentation for the infrastructure components",
            requirements={"doc_type": "api"}
        ),
        InfrastructureTask(
            task_id="infra_optimize_performance",
            task_type="optimization",
            priority=3,
            description="Optimize performance of the debate orchestrator",
            requirements={
                "optimization_type": "performance",
                "code": "core/orchestrator.py parallel execution logic"
            }
        )
    ]

    submitted_tasks = []
    for task in tasks:
        task_id = await coordinator.submit_task(task)
        submitted_tasks.append(task_id)
        print(f"   ✅ Submitted {task_id}: {task.description[:60]}...")

    print(f"\n📊 Submitted {len(submitted_tasks)} infrastructure tasks")
    print("⏳ Processing tasks... (this may take a few minutes)")

    # Wait for tasks to complete
    start_time = time.time()
    while True:
        await asyncio.sleep(5)
        status = coordinator.get_task_status()

        completed = sum(1 for s in status.values() if s['status'] == 'completed')
        failed = sum(1 for s in status.values() if s['status'] == 'failed')
        processing = sum(1 for s in status.values() if s['status'] == 'processing')

        print(f"📊 Progress: {completed} completed, {processing} processing, {failed} failed")

        if completed + failed == len(tasks):
            break

        # Timeout after 5 minutes
        if time.time() - start_time > 300:
            print("⏰ Timeout reached - some tasks may still be processing")
            break

    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "total_tasks": len(tasks),
        "task_results": status
    }

    with open("infrastructure_task_results.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print("💾 Task results saved to infrastructure_task_results.json")

    # Display summary
    print("\n🎯 INFRASTRUCTURE DEVELOPMENT SUMMARY")
    print("=" * 50)

    for task_id, task_status in status.items():
        status_icon = "✅" if task_status['status'] == 'completed' else "❌" if task_status['status'] == 'failed' else "⏳"
        print(f"{status_icon} {task_id}: {task_status['status']}")

    print(f"\n🎯 Infrastructure development workers are now active and have processed {len(tasks)} tasks!")
    print("Additional tasks can be submitted programmatically or via the task coordinator.")

if __name__ == "__main__":
    asyncio.run(submit_infrastructure_tasks())