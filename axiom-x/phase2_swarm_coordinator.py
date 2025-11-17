#!/usr/bin/env python3
"""
AXIOM-X PHASE 2: FRACTAL SWARM EXECUTION COORDINATOR
====================================================

Coordinates the Phase 2 fractal swarm using the spawned Phase 2 workers.
Implements gossip-based communication, hybrid optimization, and iterative refinement.

Capabilities:
- Task assignment to scouts (discovery), extractors (mining), validators (verification)
- Gossip protocol for swarm communication
- Hybrid RL + genetic algorithm optimization
- Canonical file identification and receipt mining
- YAML brain structure updates
"""

import os
import asyncio
import json
import time
import random
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import numpy as np
import sys

# Add paths
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "infrastructure"))
sys.path.append(str(Path(__file__).parent / "infrastructure" / "sidecar"))

from infrastructure.sidecar.router import router, TaskResult

# TURBO MODE CONFIGURATION - MAX PARALLELIZATION
TURBO_MODE = True
BATCH_SIZE = 200  # 70% of total capacity for Phase 2 (reduced from 400 for stability)
MAX_CONCURRENT = 400
INFRASTRUCTURE_RESERVED = 100  # 30% reserved for infrastructure workers
TOTAL_SYSTEM_CAPACITY = 500  # 24 cores can handle this

@dataclass
class SwarmAgent:
    """Represents a swarm agent with role and state"""
    worker_id: str
    role: str  # scout|extractor|validator
    status: str  # active|busy|idle
    tasks_completed: int
    knowledge_base: Dict[str, Any]
    last_communication: float
    fitness_score: float

@dataclass
class SwarmTask:
    """Task for swarm execution"""
    task_id: str
    type: str  # discovery|extraction|validation
    priority: int
    data: Dict[str, Any]
    assigned_to: Optional[str]
    status: str  # pending|in_progress|completed
    created_at: float

class GossipProtocol:
    """Gossip-based communication for swarm coordination"""

    def __init__(self, fanout: int = 3):
        self.fanout = fanout
        self.messages = {}  # message_id -> content

    def gossip_message(self, message: Dict[str, Any], sender: str, agents: List[SwarmAgent]) -> List[str]:
        """Send message via gossip to fanout agents"""
        message_id = hashlib.md5(json.dumps(message, sort_keys=True).encode()).hexdigest()
        if message_id in self.messages:
            return []  # Already gossiped

        self.messages[message_id] = message
        recipients = []

        # Select fanout random agents (excluding sender)
        available = [a for a in agents if a.worker_id != sender and a.status == 'active']
        if len(available) <= self.fanout:
            recipients = [a.worker_id for a in available]
        else:
            recipients = [a.worker_id for a in random.sample(available, self.fanout)]

        return recipients

class HybridOptimizer:
    """Hybrid RL + Genetic Algorithm optimizer"""

    def __init__(self):
        self.population = []
        self.generation = 0
        self.best_fitness = 0.0

    def initialize_population(self, size: int = 50):
        """Initialize population with random strategies"""
        for i in range(size):
            strategy = {
                'exploration_rate': random.uniform(0.1, 0.9),
                'mutation_rate': random.uniform(0.01, 0.1),
                'communication_freq': random.uniform(10, 100),
                'task_prioritization': random.choice(['priority', 'fifo', 'random'])
            }
            self.population.append(strategy)

    def evaluate_fitness(self, strategy: Dict[str, Any], metrics: Dict[str, float]) -> float:
        """Evaluate strategy fitness based on swarm metrics"""
        fitness = 0.0

        # Reward high task completion rate
        fitness += metrics.get('completion_rate', 0) * 0.4

        # Reward low communication overhead
        fitness += (1.0 - min(metrics.get('communication_overhead', 0), 1.0)) * 0.3

        # Reward diversity in task types
        fitness += metrics.get('task_diversity', 0) * 0.2

        # Reward convergence speed
        fitness += metrics.get('convergence_speed', 0) * 0.1

        return fitness

    def evolve_population(self, metrics: Dict[str, float]):
        """Evolve population using genetic operators"""
        # Evaluate current population
        fitness_scores = [self.evaluate_fitness(s, metrics) for s in self.population]

        # Select top performers
        sorted_indices = np.argsort(fitness_scores)[::-1]
        elite = [self.population[i] for i in sorted_indices[:10]]

        # Generate offspring via crossover and mutation
        offspring = []
        for _ in range(len(self.population) - len(elite)):
            parent1, parent2 = random.sample(elite, 2)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            offspring.append(child)

        self.population = elite + offspring
        self.generation += 1
        self.best_fitness = max(fitness_scores)

    def crossover(self, parent1: Dict, parent2: Dict) -> Dict:
        """Crossover two strategies"""
        child = {}
        for key in parent1.keys():
            child[key] = parent1[key] if random.random() < 0.5 else parent2[key]
        return child

    def mutate(self, strategy: Dict) -> Dict:
        """Mutate a strategy"""
        mutated = strategy.copy()
        if random.random() < 0.1:  # 10% mutation rate
            key = random.choice(list(mutated.keys()))
            if key == 'exploration_rate':
                mutated[key] = random.uniform(0.1, 0.9)
            elif key == 'mutation_rate':
                mutated[key] = random.uniform(0.01, 0.1)
            elif key == 'communication_freq':
                mutated[key] = random.uniform(10, 100)
            elif key == 'task_prioritization':
                mutated[key] = random.choice(['priority', 'fifo', 'random'])
        return mutated

class Phase2SwarmCoordinator:
    """Main coordinator for Phase 2 fractal swarm execution"""

    def __init__(self, workers_file: str = "infrastructure_workers_phase2_expanded.json"):
        self.workers_file = Path(workers_file)
        self.output_dir = Path("self-optimization/phase2")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Provider rate limiting semaphores (increased limits for higher throughput)
        self.provider_semaphores = {
            'anthropic': asyncio.Semaphore(200),
            'openai': asyncio.Semaphore(200),
            'google': asyncio.Semaphore(150),
            'groq': asyncio.Semaphore(250),
            'cohere': asyncio.Semaphore(150),
            'fireworks': asyncio.Semaphore(150)
        }
        self.workers_file = Path(workers_file)
        self.output_dir = Path("self-optimization/phase2")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load Phase 2 workers
        with open(self.workers_file, 'r') as f:
            data = json.load(f)

        self.agents = []
        for worker_id, status in data['worker_status'].items():
            role = worker_id.split('_')[0]  # scout, extractor, validator
            agent = SwarmAgent(
                worker_id=worker_id,
                role=role,
                status='active',
                tasks_completed=status['tasks_completed'],
                knowledge_base={},
                last_communication=time.time(),
                fitness_score=0.0
            )
            self.agents.append(agent)

        # Swarm components
        self.gossip = GossipProtocol()
        self.optimizer = HybridOptimizer()
        self.optimizer.initialize_population()

        # Task management
        self.tasks = []
        self.task_counter = 0

        # Metrics
        self.metrics = {
            'completion_rate': 0.0,
            'communication_overhead': 0.0,
            'task_diversity': 0.0,
            'convergence_speed': 0.0
        }

        # YAML brain structure
        self.brain_structure = {
            'knowledge_graph': {},
            'decision_frameworks': {},
            'execution_plans': {},
            'optimization_strategies': {}
        }

    async def initialize_swarm(self):
        """Initialize the fractal swarm"""
        print("🌀 INITIALIZING PHASE 2 FRACTAL SWARM (TURBO MODE)")
        print("=" * 50)
        print("🔍 Loading agent registry and creating swarm components...")

        # Create initial discovery tasks for ALL scouts
        scout_agents = [a for a in self.agents if a.role == 'scout']
        print(f"📋 Creating discovery tasks for {len(scout_agents)} scout agents...")
        for i, scout in enumerate(scout_agents):  # ALL scouts get tasks
            task = SwarmTask(
                task_id=f"discovery_{self.task_counter}",
                type="discovery",
                priority=1,
                data={"target": "canonical_files", "method": "metadata_analysis", "shard": i},
                assigned_to=None,  # Don't pre-assign - let assign_tasks handle it
                status="pending",
                created_at=time.time()
            )
            self.tasks.append(task)
            self.task_counter += 1
            if (i + 1) % 100 == 0:  # Progress every 100 tasks
                print(f"   → Created {i+1}/{len(scout_agents)} discovery tasks")

        # Create extraction tasks for ALL extractors
        extractor_agents = [a for a in self.agents if a.role == 'extractor']
        print(f"📋 Creating extraction tasks for {len(extractor_agents)} extractor agents...")
        for i, extractor in enumerate(extractor_agents):
            task = SwarmTask(
                task_id=f"extraction_{self.task_counter}",
                type="extraction",
                priority=2,
                data={"target": "constitutional_receipts", "method": "nlp_extraction", "shard": i},
                assigned_to=None,
                status="pending",
                created_at=time.time()
            )
            self.tasks.append(task)
            self.task_counter += 1
            if (i + 1) % 100 == 0:  # Progress every 100 tasks
                print(f"   → Created {i+1}/{len(extractor_agents)} extraction tasks")

        # Create validation tasks for ALL validators
        validator_agents = [a for a in self.agents if a.role == 'validator']
        print(f"📋 Creating validation tasks for {len(validator_agents)} validator agents...")
        for i, validator in enumerate(validator_agents):
            task = SwarmTask(
                task_id=f"validation_{self.task_counter}",
                type="validation",
                priority=3,
                data={"target": "swarm_findings", "method": "cross_validation", "shard": i},
                assigned_to=None,
                status="pending",
                created_at=time.time()
            )
            self.tasks.append(task)
            self.task_counter += 1
            if (i + 1) % 100 == 0:  # Progress every 100 tasks
                print(f"   → Created {i+1}/{len(validator_agents)} validation tasks")

        print(f"✅ TURBO Swarm initialized with {len(self.agents)} agents")
        print(f"   - Scouts: {len(scout_agents)} → {len([t for t in self.tasks if t.type == 'discovery'])} discovery tasks")
        print(f"   - Extractors: {len(extractor_agents)} → {len([t for t in self.tasks if t.type == 'extraction'])} extraction tasks")
        print(f"   - Validators: {len(validator_agents)} → {len([t for t in self.tasks if t.type == 'validation'])} validation tasks")
        print(f"   - TOTAL initial tasks: {len(self.tasks)} (MAX PARALLELIZATION)")
        print("🎯 Ready for TURBO execution - all agents have tasks assigned")

    async def execute_swarm_cycle(self):
        """Execute one swarm cycle"""
        print(f"\n🔄 SWARM CYCLE {self.optimizer.generation + 1}")

        # Assign tasks to idle agents
        await self.assign_tasks()

        # Execute tasks concurrently
        await self.execute_tasks()

        # Gossip communication
        await self.perform_gossip()

        # Update metrics
        self.update_metrics()

        # Evolve optimization strategies
        self.optimizer.evolve_population(self.metrics)

        # Update YAML brain
        self.update_brain_structure()

        print(f"📊 Metrics: Completion={self.metrics['completion_rate']:.2f}, "
              f"Comm Overhead={self.metrics['communication_overhead']:.2f}, "
              f"Diversity={self.metrics['task_diversity']:.2f}")

    async def assign_tasks(self):
        """Assign pending tasks to available agents"""
        idle_agents = [a for a in self.agents if a.status == 'active']
        pending_tasks = [t for t in self.tasks if t.status == 'pending']

        print(f"📋 TASK ASSIGNMENT: {len(idle_agents)} idle agents, {len(pending_tasks)} pending tasks")

        # Allow each agent to take MULTIPLE tasks (up to 3) for max utilization
        max_tasks_per_agent = 3
        total_assigned = 0

        for agent in idle_agents:
            # Find suitable tasks for this agent
            suitable_tasks = [t for t in pending_tasks if self.is_suitable_agent(agent, t)]
            tasks_to_assign = suitable_tasks[:max_tasks_per_agent]  # Up to 3 tasks per agent

            if tasks_to_assign:
                print(f"   → Agent {agent.worker_id[:8]} ({agent.role}): assigning {len(tasks_to_assign)} tasks")

            for task in tasks_to_assign:
                task.assigned_to = agent.worker_id
                task.status = 'in_progress'
                agent.status = 'busy'  # Mark busy even with multiple tasks
                pending_tasks.remove(task)
                total_assigned += 1

        print(f"✅ Task assignment complete: {total_assigned} tasks assigned to agents")
        print(f"   - Remaining pending tasks: {len(pending_tasks)}")
        print(f"   - Agents now busy: {len([a for a in self.agents if a.status == 'busy'])}")

    def is_suitable_agent(self, agent: SwarmAgent, task: SwarmTask) -> bool:
        """Check if agent is suitable for task"""
        if task.type == 'discovery' and agent.role == 'scout':
            return True
        elif task.type == 'extraction' and agent.role == 'extractor':
            return True
        elif task.type == 'validation' and agent.role == 'validator':
            return True
        return False

    async def execute_single_task(self, task: SwarmTask, agent: SwarmAgent):
        """Execute a single task (moved from nested function to method)"""
        # RESPECT provider rate limits - use round-robin for better distribution
        providers = ['anthropic', 'openai', 'google', 'groq', 'cohere', 'fireworks']
        # Use task index for deterministic provider assignment
        provider_index = hash(task.task_id) % len(providers)
        provider = providers[provider_index]

        async with self.provider_semaphores[provider]:  # Use class-level semaphore
            try:
                prompt = self.generate_task_prompt(task, agent)

                result = await asyncio.wait_for(
                    router.route_task(prompt, provider, max_tokens=1000),
                    timeout=60.0
                )

                # Process result
                self.process_task_result(task, agent, result)

                task.status = 'completed'
                # Only set agent to active if all their tasks are complete
                agent.tasks_completed += 1
                assigned_tasks = [t for t in self.tasks if t.assigned_to == agent.worker_id]
                active_tasks = [t for t in assigned_tasks if t.status == 'in_progress']
                if not active_tasks:
                    agent.status = 'active'

            except Exception as e:
                print(f"⚠️ Task {task.task_id} failed: {str(e)}")
                task.status = 'pending'  # Retry
                agent.status = 'active'

    async def execute_tasks(self):
        """Execute assigned tasks in batches with resource awareness"""
        # Build list of execution coroutines for in-progress assigned tasks
        execution_tasks = []
        for task in self.tasks:
            if task.status == 'in_progress' and task.assigned_to:
                agent = next((a for a in self.agents if a.worker_id == task.assigned_to), None)
                if agent:
                    execution_tasks.append(self.execute_single_task(task, agent))

        if not execution_tasks:
            print("ℹ️ No in-progress tasks to execute.")
            return

        # Check if infrastructure workers are running for resource sharing
        infra_active = os.path.exists('infrastructure_workers_status.json')
        if infra_active:
            # DUAL MODE: Share resources with infrastructure workers
            effective_batch_size = BATCH_SIZE
            print(f"🔄 DUAL MODE: Phase 2 using {effective_batch_size}, Infrastructure has {INFRASTRUCTURE_RESERVED}")
        else:
            # SOLO MODE: Infrastructure not running, use full capacity
            effective_batch_size = TOTAL_SYSTEM_CAPACITY
            print(f"🚀 SOLO MODE: Phase 2 using full capacity ({effective_batch_size})")

        num_providers = len(router.providers) if hasattr(router, 'providers') else 6
        approx_per_provider = max(1, effective_batch_size // max(1, num_providers))

        total_completed = 0

        # Human-readable header for PowerShell users
        print(f"🚀 MAX PARALLELIZATION: Starting execution with batch_size={effective_batch_size} (approx {approx_per_provider} tasks/provider)")

        for i in range(0, len(execution_tasks), effective_batch_size):
            batch = execution_tasks[i:i + effective_batch_size]
            batch_num = i // effective_batch_size + 1
            print("\n------------------------------------------------------------")
            print(f"🚀 EXECUTING BATCH {batch_num}: {len(batch)} concurrent tasks (rate-limited)")
            print(f"   • Tasks this batch: {len(batch)}")
            print(f"   • Expected per-provider split (approx): {approx_per_provider} each across {num_providers} providers")

            # Execute batch and handle any exceptions
            results = await asyncio.gather(*batch, return_exceptions=True)

            # Check for exceptions in results
            for j, result in enumerate(results):
                if isinstance(result, Exception):
                    task_idx = i + j
                    if task_idx < len(execution_tasks):
                        print(f"⚠️ Batch task {task_idx} failed with exception: {result}")

            total_completed += len(batch)
            pct = total_completed / len(execution_tasks) * 100
            print(f"✅ Completed batch {batch_num}: {total_completed}/{len(execution_tasks)} total ({pct:.1f}%)")

            # Keep short pause to allow rate-limit recovery and readable logs
            if i + effective_batch_size < len(execution_tasks):
                await asyncio.sleep(0.5)

        batches = (len(execution_tasks) + effective_batch_size - 1) // effective_batch_size
        print(f"\n✅ Completed all {len(execution_tasks)} parallel executions in {batches} batches")

    def generate_task_prompt(self, task: SwarmTask, agent: SwarmAgent) -> str:
        """Generate prompt for task execution"""
        if task.type == 'discovery':
            return f"""As a {agent.role} agent, discover canonical files in the Axiom-X codebase.
Focus on: metadata analysis, content hashing, ML classification.
Current knowledge: {json.dumps(agent.knowledge_base)}
Provide findings in JSON format."""
        elif task.type == 'extraction':
            return f"""As a {agent.role} agent, extract constitutional receipts from discovered files.
Use NLP and regex filtering, then deep learning entity extraction.
Current knowledge: {json.dumps(agent.knowledge_base)}
Provide extracted receipts in JSON format."""
        elif task.type == 'validation':
            return f"""As a {agent.role} agent, validate extracted receipts and swarm findings.
Cross-verify accuracy, consistency, and constitutional compliance.
Current knowledge: {json.dumps(agent.knowledge_base)}
Provide validation results in JSON format."""
        return "Execute assigned task."

    def process_task_result(self, task: SwarmTask, agent: SwarmAgent, result: TaskResult):
        """Process task execution result"""
        try:
            # Parse JSON response
            findings = json.loads(result.response)
            agent.knowledge_base.update(findings)

            # Update brain structure
            if task.type == 'discovery':
                self.brain_structure['knowledge_graph'].update(findings)
            elif task.type == 'extraction':
                self.brain_structure['execution_plans'].update(findings)
            elif task.type == 'validation':
                self.brain_structure['decision_frameworks'].update(findings)

        except json.JSONDecodeError:
            # Fallback: store raw response
            agent.knowledge_base[task.task_id] = result.response

    async def perform_gossip(self):
        """Perform gossip-based communication"""
        # Select random agents to initiate gossip
        initiators = random.sample(self.agents, min(10, len(self.agents)))

        for agent in initiators:
            # Create gossip message with agent's knowledge
            message = {
                'sender': agent.worker_id,
                'knowledge_update': agent.knowledge_base,
                'timestamp': time.time()
            }

            recipients = self.gossip.gossip_message(message, agent.worker_id, self.agents)

            # Simulate message delivery (in real impl, would be async network calls)
            for recipient_id in recipients:
                recipient = next((a for a in self.agents if a.worker_id == recipient_id), None)
                if recipient:
                    recipient.knowledge_base.update(message['knowledge_update'])
                    recipient.last_communication = time.time()

    def update_metrics(self):
        """Update swarm performance metrics"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.status == 'completed'])

        self.metrics['completion_rate'] = completed_tasks / max(total_tasks, 1)

        # Communication overhead (simplified)
        active_communications = sum(1 for a in self.agents if time.time() - a.last_communication < 60)
        self.metrics['communication_overhead'] = active_communications / max(len(self.agents), 1)

        # Task diversity
        task_types = [t.type for t in self.tasks]
        unique_types = len(set(task_types))
        self.metrics['task_diversity'] = unique_types / 3.0  # Max 3 types

        # Convergence speed (improvement in completion rate)
        self.metrics['convergence_speed'] = min(self.metrics['completion_rate'], 1.0)

    def update_brain_structure(self):
        """Update the YAML brain structure with swarm learnings"""
        self.brain_structure['optimization_strategies'] = {
            'current_generation': self.optimizer.generation,
            'best_fitness': self.optimizer.best_fitness,
            'active_strategy': self.optimizer.population[0] if self.optimizer.population else {}
        }

    def _extract_canonical_files_map(self) -> Dict[str, Any]:
        """Extract canonical files mapping from knowledge graph"""
        canonical_map = {
            'metadata': {
                'extraction_timestamp': datetime.now().isoformat(),
                'total_files_discovered': 0,
                'canonical_files_identified': 0
            },
            'file_mappings': {},
            'content_hashes': {},
            'file_categories': {}
        }

        knowledge_graph = self.brain_structure.get('knowledge_graph', {})

        # Process each finding in the knowledge graph
        for key, value in knowledge_graph.items():
            if isinstance(value, dict):
                # Extract file information
                if 'files' in value:
                    for file_info in value['files']:
                        if isinstance(file_info, dict) and 'path' in file_info:
                            file_path = file_info['path']
                            canonical_map['file_mappings'][file_path] = file_info

                            # Track content hashes for deduplication
                            if 'content_hash' in file_info:
                                content_hash = file_info['content_hash']
                                if content_hash not in canonical_map['content_hashes']:
                                    canonical_map['content_hashes'][content_hash] = []
                                canonical_map['content_hashes'][content_hash].append(file_path)

                            # Categorize files
                            if 'category' in file_info:
                                category = file_info['category']
                                if category not in canonical_map['file_categories']:
                                    canonical_map['file_categories'][category] = []
                                canonical_map['file_categories'][category].append(file_path)

        canonical_map['metadata']['total_files_discovered'] = len(canonical_map['file_mappings'])
        canonical_map['metadata']['canonical_files_identified'] = len([
            f for f in canonical_map['file_mappings'].values()
            if isinstance(f, dict) and f.get('is_canonical', False)
        ])

        return canonical_map

    def _extract_redundant_files_list(self) -> Dict[str, Any]:
        """Extract redundant files list from knowledge graph"""
        redundant_list = {
            'metadata': {
                'extraction_timestamp': datetime.now().isoformat(),
                'total_duplicate_groups': 0,
                'total_redundant_files': 0
            },
            'duplicate_groups': [],
            'redundancy_analysis': {}
        }

        knowledge_graph = self.brain_structure.get('knowledge_graph', {})

        # Build content hash to files mapping
        hash_to_files = {}
        for key, value in knowledge_graph.items():
            if isinstance(value, dict) and 'files' in value:
                for file_info in value['files']:
                    if isinstance(file_info, dict) and 'content_hash' in file_info:
                        content_hash = file_info['content_hash']
                        file_path = file_info.get('path', '')
                        if content_hash not in hash_to_files:
                            hash_to_files[content_hash] = []
                        hash_to_files[content_hash].append(file_path)

        # Identify duplicate groups (files with same content hash)
        duplicate_groups = []
        for content_hash, files in hash_to_files.items():
            if len(files) > 1:
                # Sort files, keep first as canonical, rest as duplicates
                sorted_files = sorted(files)
                canonical_file = sorted_files[0]
                duplicate_files = sorted_files[1:]

                duplicate_groups.append({
                    'content_hash': content_hash,
                    'canonical_file': canonical_file,
                    'duplicate_files': duplicate_files,
                    'redundancy_ratio': len(duplicate_files) / len(sorted_files)
                })

        redundant_list['duplicate_groups'] = duplicate_groups
        redundant_list['metadata']['total_duplicate_groups'] = len(duplicate_groups)
        redundant_list['metadata']['total_redundant_files'] = sum(
            len(group['duplicate_files']) for group in duplicate_groups
        )

        # Add redundancy analysis
        total_files = sum(len(files) for files in hash_to_files.values())
        unique_files = len(hash_to_files)
        redundant_list['redundancy_analysis'] = {
            'total_files_analyzed': total_files,
            'unique_content_files': unique_files,
            'redundancy_rate': (total_files - unique_files) / max(total_files, 1),
            'average_duplicates_per_group': len(duplicate_groups) / max(unique_files, 1)
        }

        return redundant_list

    async def run_swarm(self, max_cycles: int = 20):
        """Run the fractal swarm for specified cycles"""
        await self.initialize_swarm()

        for cycle in range(max_cycles):
            await self.execute_swarm_cycle()

            # Check for convergence
            if self.metrics['completion_rate'] > 0.95 and self.metrics['task_diversity'] > 0.8:
                print("🎯 Swarm convergence achieved!")
                break

        # Save results
        await self.save_results()

        print("\n🎯 PHASE 2 SWARM COMPLETE")
        print(f"📊 Final Metrics:")
        print(f"   - Cycles completed: {self.optimizer.generation}")
        print(f"   - Completion rate: {self.metrics['completion_rate']:.2f}")
        print(f"   - Best fitness: {self.optimizer.best_fitness:.3f}")
        print(f"   - Results saved to: {self.output_dir}")

    async def save_results(self):
        """Save swarm execution results"""
        print("\n💾 SAVING SWARM RESULTS...")

        results = {
            "metadata": {
                "phase": 2,
                "total_agents": len(self.agents),
                "total_tasks": len(self.tasks),
                "cycles_completed": self.optimizer.generation,
                "final_metrics": self.metrics,
                "start_time": datetime.now().isoformat(),
                "end_time": datetime.now().isoformat()
            },
            "agents": [asdict(agent) for agent in self.agents],
            "tasks": [asdict(task) for task in self.tasks],
            "brain_structure": self.brain_structure,
            "optimization_history": {
                "generations": self.optimizer.generation,
                "best_fitness": self.optimizer.best_fitness
            }
        }

        with open(self.output_dir / "SWARM_RESULTS.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)

        # Save YAML brain structure
        import yaml
        with open(self.output_dir / "AXIOM_BRAIN.yaml", 'w') as f:
            yaml.dump(self.brain_structure, f, default_flow_style=False)

        # Generate canonical files map from knowledge graph
        canonical_files_map = self._extract_canonical_files_map()
        with open(self.output_dir / "canonical_files_map.yaml", 'w') as f:
            yaml.dump(canonical_files_map, f, default_flow_style=False)

        # Generate redundant files list from knowledge graph
        redundant_files_list = self._extract_redundant_files_list()
        with open(self.output_dir / "redundant_files_list.json", 'w') as f:
            json.dump(redundant_files_list, f, indent=2)

        print(f"✅ Results saved to {self.output_dir}")
        print(f"   - SWARM_RESULTS.json")
        print(f"   - AXIOM_BRAIN.yaml")
        print(f"   - canonical_files_map.yaml")
        print(f"   - redundant_files_list.json")

async def run_phase2_swarm():
    """Main entry point for Phase 2 swarm execution"""
    print("🌀 AXIOM-X PHASE 2: FRACTAL SWARM EXECUTION")
    print("=" * 55)
    print("🔍 Starting TURBO mode with maximum parallelization...")
    print("📊 Loading 2,794 agents from registry...")

    try:
        coordinator = Phase2SwarmCoordinator()
        print("✅ Coordinator initialized")

        print("🚀 Starting swarm execution (20 cycles max)...")
        await coordinator.run_swarm(max_cycles=20)

    except Exception as e:
        print(f"❌ CRITICAL ERROR in swarm execution: {str(e)}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    asyncio.run(run_phase2_swarm())