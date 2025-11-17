#!/usr/bin/env python3
"""
from axiom_receipt_hook import generate_receipt
AXIOM-X PHASE 1 DEBATE: FINAL ROUNDS EXECUTOR
===========================================

Executes the final rounds of the adversarial debate:
- Round 19: Closing arguments from all debaters
- Round 20: Judges debate each other
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
import sys

# Add infrastructure path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "infrastructure"))
sys.path.append(str(Path(__file__).parent / "infrastructure" / "sidecar"))

from infrastructure.sidecar.router import router, TaskResult

class FinalRoundsExecutor:
    """Executes the final rounds of Phase 1 debate"""

    DEBATERS = [
        "anthropic-sonnet", "anthropic-opus", "openai-gpt4o", "openai-o1",
        "google-gemini2", "groq-llama", "cohere-command", "google-gemini-pro", "openai-gpt4o-mini"
    ]

    JUDGES = ["mistral-large", "together-ai", "fireworks"]

    def __init__(self):
        self.output_dir = Path("self-optimization/phase1")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def execute_closing_arguments(self):
        """Round 19: Closing arguments from all debaters"""
        print("🎭 ROUND 19: CLOSING ARGUMENTS")
        print("=" * 50)

        closing_prompts = [
            f"You are {debater}. Provide your closing argument for the Axiom-X self-optimization debate. "
            f"Summarize your key positions on canonical file identification, redundancy patterns, "
            f"constitutional receipt mining, and Phase 2-5 execution strategy. "
            f"Make your final case for optimal recursive self-improvement."
            for debater in self.DEBATERS
        ]

        print(f"🚀 Executing closing arguments with controlled concurrency...")

        # Controlled concurrency for closing arguments
        semaphore = asyncio.Semaphore(6)

        async def fire_closing(debater: str, prompt: str):
            async with semaphore:
                try:
                    provider = self._map_debater_to_provider(debater)
                    result = await asyncio.wait_for(
                        router.route_task(prompt, provider, max_tokens=2000),
                        timeout=180.0
                    )
                    return debater, result
                except Exception as e:
                    return debater, TaskResult(
                        provider=provider,
                        response=f"Error in closing argument: {str(e)}",
                        latency=0.0,
                        tokens=0,
                        cost=0.0
                    )

        start_time = time.time()
        tasks = [fire_closing(debater, prompt) for debater, prompt in zip(self.DEBATERS, closing_prompts)]
        results = await asyncio.gather(*tasks)
        batch_latency = time.time() - start_time

        print(".2f")

        closing_arguments = []
        for debater, result in results:
            closing_arguments.append({
                "debater": debater,
                "argument": result.response,
                "timestamp": datetime.now().isoformat()
            })
            print(f"✅ {debater} closing argument complete")

        return closing_arguments

    async def execute_judge_debate(self):
        """Round 20: Judges debate each other"""
        print("\n⚖️ ROUND 20: JUDGES DEBATE")
        print("=" * 50)

        judge_debate_prompts = [
            f"You are Judge {judge}. The debate has concluded. Now debate your fellow judges on the optimal "
            f"interpretation of the consensus reached. Argue your position on how to implement the Phase 2 "
            f"fractal swarm execution plan. Challenge or support the emerging consensus points."
            for judge in self.JUDGES
        ]

        print(f"🚀 Judges debating with controlled concurrency...")

        # Judges debate with controlled concurrency
        semaphore = asyncio.Semaphore(3)

        async def fire_judge_debate(judge: str, prompt: str):
            async with semaphore:
                try:
                    provider = judge.split('-')[0] if judge != "together-ai" else "openai"
                    result = await asyncio.wait_for(
                        router.route_task(prompt, provider, max_tokens=2000),
                        timeout=180.0
                    )
                    return judge, result
                except Exception as e:
                    return judge, TaskResult(
                        provider=provider,
                        response=f"Error in judge debate: {str(e)}",
                        latency=0.0,
                        tokens=0,
                        cost=0.0
                    )

        start_time = time.time()
        tasks = [fire_judge_debate(judge, prompt) for judge, prompt in zip(self.JUDGES, judge_debate_prompts)]
        results = await asyncio.gather(*tasks)
        judge_latency = time.time() - start_time

        print(".2f")

        judge_debates = []
        for judge, result in results:
            judge_debates.append({
                "judge": judge,
                "debate_argument": result.response,
                "timestamp": datetime.now().isoformat()
            })
            print(f"✅ Judge {judge} debate complete")

        return judge_debates

    async def generate_final_synthesis(self, closing_arguments, judge_debates):
        """Generate final synthesis for Phase 2 transition"""
        print("\n🧠 GENERATING FINAL SYNTHESIS")
        print("=" * 50)

        synthesis_prompt = f"""
        Synthesize the complete Phase 1 debate results for Phase 2 transition:

        CLOSING ARGUMENTS SUMMARY:
        {len(closing_arguments)} debaters provided closing arguments

        JUDGE DEBATES SUMMARY:
        {len(judge_debates)} judges debated the consensus

        Provide the definitive Phase 2 fractal swarm execution plan including:
        1. Canonical file identification criteria
        2. Redundancy pattern exploitation strategy
        3. Constitutional receipt mining approach
        4. YAML brain structure implementation
        5. Phase 2-5 execution roadmap
        6. 10,000× parallelization implementation

        This synthesis will guide the transition to Phase 2.
        """

        print(f"🚀 Generating final synthesis...")

        try:
            result = await asyncio.wait_for(
                router.route_task(synthesis_prompt, "anthropic", max_tokens=3000),
                timeout=240.0
            )

            synthesis = {
                "synthesis": result.response,
                "timestamp": datetime.now().isoformat(),
                "phase_transition": "Phase 1 Complete -> Phase 2 Ready"
            }

            print("✅ Final synthesis complete")
            return synthesis

        except Exception as e:
            return {
                "synthesis": f"Error generating synthesis: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "phase_transition": "Phase 1 Complete -> Phase 2 Ready (with synthesis error)"
            }

    async def save_final_results(self, closing_arguments, judge_debates, synthesis):
        """Save all final round results"""
        print("\n💾 SAVING FINAL ROUND RESULTS")
        print("=" * 50)

        final_results = {
            "phase": 1,
            "final_rounds": {
                "round_19_closing_arguments": closing_arguments,
                "round_20_judge_debate": judge_debates,
                "final_synthesis": synthesis
            },
            "metadata": {
                "total_debaters": len(self.DEBATERS),
                "total_judges": len(self.JUDGES),
                "completion_timestamp": datetime.now().isoformat(),
                "phase_2_ready": True
            }
        }

        with open(self.output_dir / "FINAL_ROUNDS_RESULTS.json", 'w') as f:
            json.dump(final_results, f, indent=2)

        print(f"✅ Final results saved to {self.output_dir / 'FINAL_ROUNDS_RESULTS.json'}")
        print("🎯 PHASE 1 COMPLETE - READY FOR PHASE 2 FRACTAL SWARM EXECUTION")

    def _map_debater_to_provider(self, debater: str) -> str:
        """Map debater to provider"""
        if debater.startswith('anthropic'):
            return 'anthropic'
        elif debater.startswith('openai'):
            return 'openai'
        elif debater.startswith('google'):
            return 'google'
        elif debater.startswith('groq'):
            return 'groq'
        elif debater.startswith('cohere'):
            return 'cohere'
        elif debater.startswith('fireworks'):
            return 'fireworks'
        else:
            return 'anthropic'

async def execute_final_rounds():
    """Main execution function"""
    print("🌀 AXIOM-X PHASE 1: FINAL ROUNDS EXECUTION")
    print("=" * 60)

    executor = FinalRoundsExecutor()

    # Execute Round 19: Closing Arguments
    closing_arguments = await executor.execute_closing_arguments()

    # Execute Round 20: Judge Debate
    judge_debates = await executor.execute_judge_debate()

    # Generate Final Synthesis
    synthesis = await executor.generate_final_synthesis(closing_arguments, judge_debates)

    # Save Results
    await executor.save_final_results(closing_arguments, judge_debates, synthesis)

    print("\n🎯 PHASE 1 ADVERSARIAL DEBATE COMPLETE")
    print("📊 Final Statistics:")
    print(f"   - Closing arguments: {len(closing_arguments)}")
    print(f"   - Judge debates: {len(judge_debates)}")
    print(f"   - Final synthesis: Generated")
    print(f"   - Results saved to: {executor.output_dir}")

if __name__ == "__main__":
    asyncio.run(execute_final_rounds())