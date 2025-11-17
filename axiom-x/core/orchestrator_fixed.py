#!/usr/bin/env python3
"""
AXIOM-X RECURSIVE SELF-OPTIMIZATION: PHASE 1 - ADVERSARIAL DEBATE ORCHESTRATOR
==============================================================================

Orchestrates multi-provider adversarial debate for self-optimization strategy.
Manages 9 debaters + 3 judges across 50+ turns with game theory dynamics.

Capabilities:
- Multi-provider debate coordination
- Game theory mechanisms (prisoner's dilemma, tit-for-tat)
- Constitutional validation
- Resonance tracking via Lyapunov exponents
- Cryptographic provenance with Ed25519 signatures
"""

import os
import asyncio
import json
import time
import hashlib
import hmac
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import numpy as np
from pathlib import Path
import sys

# Add infrastructure path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "infrastructure"))
sys.path.append(str(Path(__file__).parent.parent / "infrastructure" / "sidecar"))

from infrastructure.sidecar.router import router, TaskResult
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DebateTurn:
    """Represents a single turn in the debate"""
    turn: int
    debater: str
    role: str
    argument: str
    evidence: List[str]
    challenges: List[str]
    game_theory_position: str  # cooperate|defect|punish|reward
    timestamp: str
    constitutional_score: float
    signature: str

@dataclass
class JudgeEvaluation:
    """Judge evaluation of debate quality"""
    judge: str
    turn: int
    argument_quality: float  # 0.0-1.0
    evidence_strength: float  # 0.0-1.0
    challenge_validity: float  # 0.0-1.0
    cooperation_benefit: float  # 0.0-1.0
    total_score: float
    veto_called: bool
    feedback: str

class ConstitutionalValidator:
    """Validates Yama principles compliance"""

    YAMA_PRINCIPLES = [
        "ahimsa",  # non-harm
        "satya",   # truth
        "asteya",  # non-stealing
        "brahmacharya",  # right energy use
        "aparigraha"     # non-hoarding
    ]

    def validate_turn(self, turn: DebateTurn) -> float:
        """Return constitutional compliance score 0.0-1.0"""
        # Simple heuristic validation - in practice would use ML model
        violations = 0

        # Check for harmful content
        harmful_keywords = ["harm", "damage", "destroy", "exploit"]
        if any(kw in turn.argument.lower() for kw in harmful_keywords):
            violations += 1

        # Check for truth claims without evidence
        if len(turn.evidence) == 0 and "proven" in turn.argument.lower():
            violations += 0.5

        # Check for cooperation vs defection
        if turn.game_theory_position == "defect":
            violations += 0.2

        compliance = max(0.0, 1.0 - (violations / 2.0))
        return compliance

class GameTheoryEngine:
    """Manages game theory dynamics in the debate"""

    def __init__(self):
        self.reputation_scores = {}
        self.cooperation_history = {}

    def update_reputation(self, debater: str, action: str, outcome: float):
        """Update debater reputation based on actions"""
        if debater not in self.reputation_scores:
            self.reputation_scores[debater] = 1.0

        # Reward cooperation, penalize defection
        if action == "cooperate":
            self.reputation_scores[debater] += outcome * 0.1
        elif action == "defect":
            self.reputation_scores[debater] -= 0.2

        # Bound between 0.1 and 2.0
        self.reputation_scores[debater] = max(0.1, min(2.0, self.reputation_scores[debater]))

    def should_cooperate(self, debater: str, opponent: str) -> bool:
        """Tit-for-tat strategy with forgiveness"""
        if opponent not in self.cooperation_history:
            return True  # Start with cooperation

        history = self.cooperation_history[opponent]
        if len(history) == 0:
            return True

        # Cooperate if opponent cooperated last time
        return history[-1] == "cooperate"

class ChaosDynamicsTracker:
    """Tracks debate convergence using strange attractors"""

    def __init__(self):
        self.embeddings = []
        self.lyapunov_exponents = []

    def add_turn_embedding(self, embedding: List[float]):
        """Add turn embedding for convergence analysis"""
        self.embeddings.append(embedding)

        if len(self.embeddings) >= 3:
            # Calculate Lyapunov exponent approximation
            distances = []
            for i in range(len(self.embeddings) - 1):
                dist = np.linalg.norm(
                    np.array(self.embeddings[i+1]) - np.array(self.embeddings[i])
                )
                distances.append(dist)

            if distances:
                lyapunov = np.mean(np.log(distances))
                self.lyapunov_exponents.append(lyapunov)

    def calculate_resonance(self) -> float:
        """Calculate debate resonance (convergence) score"""
        if len(self.lyapunov_exponents) < 2:
            return 0.0

        # Resonance = 1 / (1 + average Lyapunov exponent)
        # Lower chaos = higher resonance
        avg_lyapunov = np.mean(self.lyapunov_exponents[-10:])  # Last 10 measurements
        resonance = 1.0 / (1.0 + abs(avg_lyapunov))

        return min(1.0, resonance)

class Phase1Orchestrator:
    """Main orchestrator for Phase 1 adversarial debate"""

    DEBATERS = [
        "anthropic-sonnet", "anthropic-opus", "openai-gpt4o", "openai-o1",
        "google-gemini2", "groq-llama", "cohere-command", "google-gemini-pro", "openai-gpt4o-mini"
    ]

    JUDGES = ["mistral-large", "together-ai", "fireworks"]

    def __init__(self, output_dir: str = "self-optimization/phase1", mission: str = ""):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.debate_log = []
        self.judge_evaluations = []
        self.constitutional_validator = ConstitutionalValidator()
        self.game_theory = GameTheoryEngine()
        self.chaos_tracker = ChaosDynamicsTracker()

        # Debate configuration
        self.min_turns_per_debater = 50
        self.max_turns_per_debater = 100
        self.convergence_threshold = 0.85
        self.timeout_hours = 3
        self.max_rounds = 20  # User specified max 20 rounds

        # Tracking
        self.turn_counts = {debater: 0 for debater in self.DEBATERS}
        self.start_time = None
        self.judge_veto_called = False
        self.mission = mission

    async def initialize_debate(self):
        """Initialize the debate with opening statements"""
        print("[*] INITIALIZING PHASE 1 ADVERSARIAL DEBATE")
        print("=" * 60)

        self.start_time = time.time()

        # Opening thesis statements from each debater
        opening_prompts = [
            f"MISSION BRIEFING:\n{self.mission}\n\nYou are {debater}. Provide your opening thesis on optimal Axiom-X self-optimization strategy. Focus on: How should we identify canonical implementations? What redundancy patterns matter most? How to mine constitutional receipts effectively?"
            for debater in self.DEBATERS
        ]

        print(f"[+] Generating {len(opening_prompts)} opening statements with BALANCED HIGH CONCURRENCY...")

        # BALANCED CONCURRENCY: 6 simultaneous API calls for optimal throughput without overload
        semaphore = asyncio.Semaphore(6)

        async def fire_opening(debater: str, prompt: str):
            async with semaphore:
                try:
                    # Map debater to provider
                    if debater.startswith('anthropic'):
                        provider = 'anthropic'
                    elif debater.startswith('openai'):
                        provider = 'openai'
                    elif debater.startswith('google'):
                        provider = 'google'
                    elif debater.startswith('groq'):
                        provider = 'groq'
                    elif debater.startswith('cohere'):
                        provider = 'cohere'
                    elif debater.startswith('fireworks'):
                        provider = 'fireworks'
                    else:
                        provider = 'anthropic'  # fallback

                    result = await asyncio.wait_for(
                        router.route_task(prompt, provider, max_tokens=1500),
                        timeout=180.0  # 3 minute timeout for max reliability
                    )
                    return debater, result
                except Exception as e:
                    return debater, TaskResult(
                        provider=provider,
                        response=f"Error: {str(e)} for {debater} opening statement",
                        latency=0.0,
                        tokens=0,
                        cost=0.0
                    )

        # BALANCED HIGH CONCURRENCY: Fire all 9 debaters with controlled parallelism
        start_time = time.time()
        tasks = [fire_opening(debater, prompt) for debater, prompt in zip(self.DEBATERS, opening_prompts)]
        # Use return_exceptions=True to prevent cancellation of all tasks when one fails
        results = await asyncio.gather(*tasks, return_exceptions=True)

        batch_latency = time.time() - start_time

        # Process results (handle exceptions gracefully). results may contain Exception objects
        for idx, item in enumerate(results):
            turn_num = idx + 1
            if isinstance(item, Exception):
                debater = self.DEBATERS[idx] if idx < len(self.DEBATERS) else f"debater_{idx}"
                print(f"[!] Exception for {debater}: {str(item)}")
                result = TaskResult(
                    provider="error",
                    response=f"Exception during opening statement: {str(item)}",
                    latency=0.0,
                    tokens=0,
                    cost=0.0
                )
            else:
                # Expected shape: (debater, TaskResult)
                try:
                    debater, result = item
                except Exception:
                    debater = self.DEBATERS[idx] if idx < len(self.DEBATERS) else f"debater_{idx}"
                    result = TaskResult(
                        provider="error",
                        response=f"Malformed result for {debater}",
                        latency=0.0,
                        tokens=0,
                        cost=0.0
                    )

            turn = DebateTurn(
                turn=turn_num,
                debater=debater,
                role="Thesis Proposal",
                argument=result.response,
                evidence=[],  # Opening statements have no prior evidence
                challenges=[],
                game_theory_position="cooperate",  # Start cooperative
                timestamp=datetime.now().isoformat(),
                constitutional_score=self.constitutional_validator.validate_turn(
                    DebateTurn(0, "", "", result.response, [], [], "", "", 0.0, "")
                ),
                signature=self._generate_signature(result.response)
            )

            self.debate_log.append(turn)
            self.turn_counts[debater] += 1

            # Add to chaos tracking (simplified embedding)
            words = result.response.split()[:10]
            if len(words) < 10:
                words.extend([''] * (10 - len(words)))
            embedding = [hash(word) % 1000 for word in words]
            self.chaos_tracker.add_turn_embedding(embedding)

        print(f"[+] Opening statements complete. Debate log: {len(self.debate_log)} turns")

    async def execute_debate_round(self, round_num: int):
        """Execute a single debate round with all debaters"""
        print(f"\n[*] DEBATE ROUND {round_num}")

        # BALANCED HIGH CONCURRENCY: Execute all debaters with controlled parallelism
        # 6 simultaneous API calls for optimal throughput without system overload
        semaphore = asyncio.Semaphore(6)

        async def fire_debate(debater: str, prompt: str, provider: str):
            async with semaphore:
                try:
                    return debater, await asyncio.wait_for(
                        router.route_task(prompt, provider, max_tokens=2000),
                        timeout=180.0  # Increased timeout for reliability
                    )
                except Exception as e:
                    return debater, TaskResult(
                        provider=provider,
                        response=f"Error: {str(e)} for {debater}",
                        latency=0.0,
                        tokens=0,
                        cost=0.0
                    )

        print(f"[+] BALANCED HIGH CONCURRENCY: {len(self.DEBATERS)} debaters firing with 6 simultaneous calls...")

        # Prepare all tasks
        debate_tasks = []
        for debater in self.DEBATERS:
            # Build context from recent turns
            context = self._build_debate_context(debater, recent_turns=5)

            prompt = f"""You are {debater} in turn {len(self.debate_log) + 1}.

Recent debate context:
{context}

Your role: Antithesis/Counter-argument
Provide a counter-argument or refinement to the previous positions.
Consider game theory: Should you cooperate (build on others' ideas) or defect (challenge strongly)?
Current resonance: {self.chaos_tracker.calculate_resonance():.3f}

Focus areas:
1. Challenge weak assumptions in previous arguments
2. Propose specific self-optimization strategies
3. Address constitutional compliance
4. Consider 10,000x parallelization implications

Game theory position (cooperate|defect|punish|reward):"""

            # Map debater to provider
            if debater.startswith('anthropic'):
                provider = 'anthropic'
            elif debater.startswith('openai'):
                provider = 'openai'
            elif debater.startswith('google'):
                provider = 'google'
            elif debater.startswith('groq'):
                provider = 'groq'
            elif debater.startswith('cohere'):
                provider = 'cohere'
            elif debater.startswith('fireworks'):
                provider = 'fireworks'
            else:
                provider = 'anthropic'  # fallback

            debate_tasks.append(fire_debate(debater, prompt, provider))

        # BALANCED HIGH CONCURRENCY: Fire all 9 debaters with controlled parallelism
        start_time = time.time()
        results = await asyncio.gather(*debate_tasks, return_exceptions=True)
        batch_latency = time.time() - start_time

        # Process results (handle exceptions gracefully)
        for idx, item in enumerate(results):
            if isinstance(item, Exception):
                debater = self.DEBATERS[idx] if idx < len(self.DEBATERS) else f"debater_{idx}"
                print(f"[!] Exception for {debater}: {str(item)}")
                result = TaskResult(
                    provider="error",
                    response=f"Exception during debate round: {str(item)}",
                    latency=0.0,
                    tokens=0,
                    cost=0.0
                )
            else:
                try:
                    debater, result = item
                except Exception:
                    debater = self.DEBATERS[idx] if idx < len(self.DEBATERS) else f"debater_{idx}"
                    result = TaskResult(
                        provider="error",
                        response=f"Malformed result for {debater}",
                        latency=0.0,
                        tokens=0,
                        cost=0.0
                    )

            # Parse game theory position from response
            response_lines = result.response.split('\n')
            game_theory_pos = "cooperate"  # default

            for line in response_lines:
                if "game theory position" in line.lower():
                    if "defect" in line.lower():
                        game_theory_pos = "defect"
                    elif "punish" in line.lower():
                        game_theory_pos = "punish"
                    elif "reward" in line.lower():
                        game_theory_pos = "reward"

            turn = DebateTurn(
                turn=len(self.debate_log) + 1,
                debater=debater,
                role="Counter-Argument",
                argument=result.response,
                evidence=self._extract_evidence(result.response),
                challenges=self._extract_challenges(result.response),
                game_theory_position=game_theory_pos,
                timestamp=datetime.now().isoformat(),
                constitutional_score=self.constitutional_validator.validate_turn(
                    DebateTurn(0, "", "", result.response, [], [], "", "", 0.0, "")
                ),
                signature=self._generate_signature(result.response)
            )

            self.debate_log.append(turn)
            self.turn_counts[debater] += 1

            # Update game theory
            self.game_theory.update_reputation(debater, game_theory_pos, turn.constitutional_score)

            # Add to chaos tracking
            words = result.response.split()[:10]
            if len(words) < 10:
                words.extend([''] * (10 - len(words)))
            embedding = [hash(word) % 1000 for word in words]
            self.chaos_tracker.add_turn_embedding(embedding)

        # Judge evaluation
        await self._execute_judge_evaluation(round_num)

        # Check for judge vetoes
        if any(eval.veto_called for eval in self.judge_evaluations[-len(self.JUDGES):]):
            self.judge_veto_called = True
            print(f"[!] Judge veto called in round {round_num} - stopping debate early")

        resonance = self.chaos_tracker.calculate_resonance()
        print(f"Resonance: {resonance:.3f}")

    def _build_debate_context(self, debater: str, recent_turns: int = 5) -> str:
        """Build context string from recent debate turns"""
        recent = self.debate_log[-recent_turns:] if len(self.debate_log) >= recent_turns else self.debate_log

        context_lines = []
        for turn in recent:
            if turn.debater != debater:  # Don't include own previous turns
                context_lines.append(f"{turn.debater} (Turn {turn.turn}): {turn.argument[:200]}...")

        return "\n".join(context_lines)

    def _extract_evidence(self, response: str) -> List[str]:
        """Extract evidence references from response"""
        # Simple extraction - look for receipt mentions
        evidence = []
        if "receipt" in response.lower():
            evidence.append("constitutional_receipt_reference")
        if "performance" in response.lower():
            evidence.append("performance_metric")
        if "validation" in response.lower():
            evidence.append("validation_result")
        return evidence

    def _extract_challenges(self, response: str) -> List[str]:
        """Extract challenges from response"""
        challenges = []
        challenge_keywords = ["however", "but", "challenge", "weak", "incorrect"]
        if any(kw in response.lower() for kw in challenge_keywords):
            challenges.append("methodological_challenge")
        return challenges

    async def _execute_judge_evaluation(self, round_num: int):
        """Have judges evaluate the current debate state"""
        judge_prompts = [
            f"You are judge {judge}. Evaluate the quality of debate round {round_num}. "
            f"Current resonance: {self.chaos_tracker.calculate_resonance():.3f}. "
            f"Rate argument quality, evidence strength, challenge validity, cooperation benefit (0.0-1.0 each). "
            f"Call veto if serious constitutional violation detected or if consensus has been reached and further rounds might be detrimental."
            for judge in self.JUDGES
        ]

        # BALANCED HIGH CONCURRENCY: Execute all judges with controlled parallelism
        # 6 simultaneous API calls for optimal throughput
        semaphore = asyncio.Semaphore(6)

        async def fire_judge(prompt: str, judge: str):
            async with semaphore:
                try:
                    provider = judge.split('-')[0] if judge != "together-ai" else "openai"
                    return judge, await asyncio.wait_for(
                        router.route_task(prompt, provider, max_tokens=1500),
                        timeout=120.0  # Increased timeout
                    )
                except Exception as e:
                    return judge, TaskResult(
                        provider=provider,
                        response=f"Error: {str(e)} for judge evaluation",
                        latency=0.0,
                        tokens=0,
                        cost=0.0
                    )

        print(f"[*] BALANCED HIGH CONCURRENCY: {len(self.JUDGES)} judges firing with 6 simultaneous calls...")

        start_time = time.time()
        judge_tasks = [fire_judge(prompt, judge) for prompt, judge in zip(judge_prompts, self.JUDGES)]
        results = await asyncio.gather(*judge_tasks, return_exceptions=True)
        judge_latency = time.time() - start_time

        # Process judge results safely
        for idx, item in enumerate(results):
            if isinstance(item, Exception):
                judge = self.JUDGES[idx] if idx < len(self.JUDGES) else f"judge_{idx}"
                print(f"[!] Exception for judge {judge}: {str(item)}")
                result = TaskResult(
                    provider="error",
                    response=f"Exception during judge evaluation: {str(item)}",
                    latency=0.0,
                    tokens=0,
                    cost=0.0
                )
            else:
                try:
                    judge, result = item
                except Exception:
                    judge = self.JUDGES[idx] if idx < len(self.JUDGES) else f"judge_{idx}"
                    result = TaskResult(
                        provider="error",
                        response=f"Malformed result for {judge}",
                        latency=0.0,
                        tokens=0,
                        cost=0.0
                    )

            # Parse judge scores (simplified parsing)
            scores = self._parse_judge_scores(result.response)

            evaluation = JudgeEvaluation(
                judge=judge,
                turn=round_num,
                argument_quality=scores.get('argument_quality', 0.5),
                evidence_strength=scores.get('evidence_strength', 0.5),
                challenge_validity=scores.get('challenge_validity', 0.5),
                cooperation_benefit=scores.get('cooperation_benefit', 0.5),
                total_score=sum(scores.values()) / len(scores) if scores else 0.5,
                veto_called="veto" in result.response.lower(),
                feedback=result.response[:500]
            )

            self.judge_evaluations.append(evaluation)

    def _parse_judge_scores(self, response: str) -> Dict[str, float]:
        """Parse numerical scores from judge response"""
        scores = {}
        lines = response.split('\n')

        for line in lines:
            line = line.lower().strip()
            if 'argument quality' in line:
                scores['argument_quality'] = self._extract_score(line)
            elif 'evidence strength' in line:
                scores['evidence_strength'] = self._extract_score(line)
            elif 'challenge validity' in line:
                scores['challenge_validity'] = self._extract_score(line)
            elif 'cooperation benefit' in line:
                scores['cooperation_benefit'] = self._extract_score(line)

        return scores

    def _extract_score(self, line: str) -> float:
        """Extract numerical score from text line"""
        import re
        numbers = re.findall(r'0\.\d+|1\.0', line)
        return float(numbers[0]) if numbers else 0.5

    def _generate_signature(self, content: str) -> str:
        """Generate Ed25519 signature for content (simplified)"""
        # In practice, would use proper Ed25519 signing
        # For demo, use HMAC-SHA256
        key = os.getenv('PROVENANCE_KEY_PATH', 'demo_key').encode()
        signature = hmac.new(key, content.encode(), hashlib.sha256).hexdigest()
        return signature

    def check_convergence(self) -> bool:
        """Check if debate has converged"""
        resonance = self.chaos_tracker.calculate_resonance()
        min_turns_met = all(count >= self.min_turns_per_debater for count in self.turn_counts.values())

        elapsed_hours = (time.time() - self.start_time) / 3600
        timeout_reached = elapsed_hours >= self.timeout_hours

        print(f"Resonance: {resonance:.3f}")
        return (resonance >= self.convergence_threshold and min_turns_met) or timeout_reached or self.judge_veto_called

    async def save_results(self):
        """Save debate results to files"""
        print("\n[*] SAVING DEBATE RESULTS...")

        # Save debate log
        debate_data = {
            "metadata": {
                "phase": 1,
                "total_turns": len(self.debate_log),
                "debaters": self.DEBATERS,
                "judges": self.JUDGES,
                "final_resonance": self.chaos_tracker.calculate_resonance(),
                "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                "end_time": datetime.now().isoformat()
            },
            "turns": [asdict(turn) for turn in self.debate_log],
            "judge_evaluations": [asdict(eval) for eval in self.judge_evaluations],
            "turn_counts": self.turn_counts,
            "reputation_scores": self.game_theory.reputation_scores
        }

        with open(self.output_dir / "DEBATE_LOG.json", 'w') as f:
            json.dump(debate_data, f, indent=2)

        # Generate synthesis
        await self._generate_synthesis()

        print(f"[+] Results saved to {self.output_dir}")

    async def _generate_synthesis(self):
        """Generate debate synthesis using judges"""
        synthesis_prompt = f"""
        Synthesize the key consensus points from this {len(self.debate_log)}-turn debate.
        Focus on:
        1. Optimal self-optimization strategy
        2. Canonical file identification criteria
        3. Receipt mining approaches
        4. YAML brain structure recommendations
        5. Phase 2-5 execution plan

        Debate summary:
        - Total turns: {len(self.debate_log)}
        - Final resonance: {self.chaos_tracker.calculate_resonance():.3f}
        - Participating debaters: {len(self.DEBATERS)}
        - Judge evaluations: {len(self.judge_evaluations)}

        Provide actionable recommendations for Phase 2 fractal swarm execution.
        """

        # BALANCED HIGH CONCURRENCY: Execute all judges simultaneously for synthesis
        # 6 simultaneous API calls for optimal throughput
        semaphore = asyncio.Semaphore(6)

        async def fire_synthesis(prompt: str, judge: str):
            async with semaphore:
                try:
                    provider = judge.split('-')[0]
                    return judge, await asyncio.wait_for(
                        router.route_task(prompt, provider, max_tokens=2000),
                        timeout=180.0  # Increased timeout for synthesis
                    )
                except Exception as e:
                    return judge, TaskResult(
                        provider=provider,
                        response=f"Error: {str(e)} for synthesis",
                        latency=0.0,
                        tokens=0,
                        cost=0.0
                    )

        print(f"[*] BALANCED HIGH CONCURRENCY: {len(self.JUDGES)} judges firing with 6 simultaneous calls for synthesis...")

        start_time = time.time()
        synthesis_tasks = [fire_synthesis(synthesis_prompt, judge) for judge in self.JUDGES]
        results = await asyncio.gather(*synthesis_tasks, return_exceptions=True)
        synthesis_latency = time.time() - start_time

        # Build synthesis safely
        judge_syntheses = []
        consensus_sources = []
        for idx, item in enumerate(results):
            if isinstance(item, Exception):
                judge = self.JUDGES[idx] if idx < len(self.JUDGES) else f"judge_{idx}"
                content = f"Exception: {str(item)}"
                tr = TaskResult("error", content, 0.0, 0, 0.0)
            else:
                try:
                    judge, result = item
                    content = result.response
                    tr = result
                except Exception:
                    judge = self.JUDGES[idx] if idx < len(self.JUDGES) else f"judge_{idx}"
                    content = "Malformed result"
                    tr = TaskResult("error", content, 0.0, 0, 0.0)

            judge_syntheses.append({"judge": judge, "content": content})
            consensus_sources.append(tr)

        synthesis = {
            "synthesis_timestamp": datetime.now().isoformat(),
            "judge_syntheses": judge_syntheses,
            "consensus_points": self._extract_consensus(consensus_sources)
        }

        with open(self.output_dir / "DEBATE_SYNTHESIS.json", 'w') as f:
            json.dump(synthesis, f, indent=2)

        return synthesis

    async def execute_closing_arguments(self):
        """Run a single closing-argument round where each debater produces a closing summary."""
        print("\n[*] EXECUTING CLOSING ARGUMENTS (All debaters)")
        semaphore = asyncio.Semaphore(6)

        async def fire_closing(debater: str):
            prompt = f"You are {debater}. Provide a concise closing argument (max 500 tokens) summarizing your main proposals and actionable steps for Phase 2-5. Highlight risks and constitutional compliance." 
            async with semaphore:
                try:
                    provider = 'anthropic' if debater.startswith('anthropic') else (
                        'openai' if debater.startswith('openai') else (
                        'google' if debater.startswith('google') else 'anthropic'))
                    return debater, await asyncio.wait_for(router.route_task(prompt, provider, max_tokens=1000), timeout=120.0)
                except Exception as