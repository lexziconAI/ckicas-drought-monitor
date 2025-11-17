#!/usr/bin/env python3
"""
AXIOM-X LATENCY OPTIMIZATION SMOKE TEST
========================================

Tests parallelization strategies to optimize LLM API latency.
Measures improvements from increasing batch sizes and concurrent calls.
"""

import asyncio
import time
import json
import statistics
from typing import List, Dict, Any
from pathlib import Path
import sys

# Add infrastructure path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "infrastructure"))
sys.path.append(str(Path(__file__).parent.parent / "infrastructure" / "sidecar"))

from infrastructure.sidecar.router import router

class LatencyOptimizer:
    """Tests different parallelization strategies for latency optimization"""

    def __init__(self):
        self.test_prompts = [
            "Reply with exactly: TEST_1",
            "Reply with exactly: TEST_2",
            "Reply with exactly: TEST_3",
            "Reply with exactly: TEST_4",
            "Reply with exactly: TEST_5",
            "Reply with exactly: TEST_6",
            "Reply with exactly: TEST_7",
            "Reply with exactly: TEST_8",
            "Reply with exactly: TEST_9",
            "Reply with exactly: TEST_10"
        ]

    async def test_batch_size(self, batch_size: int, num_batches: int = 3) -> Dict[str, Any]:
        """Test latency with specific batch size"""
        print(f"\n🧪 Testing batch size: {batch_size}")

        batch_latencies = []
        total_latencies = []

        for batch_num in range(num_batches):
            print(f"  Batch {batch_num + 1}/{num_batches}...")

            # Create batches
            batches = []
            for i in range(0, len(self.test_prompts), batch_size):
                batch = self.test_prompts[i:i + batch_size]
                batches.append(batch)

            batch_start = time.time()

            # Process batches sequentially with small delays
            all_results = []
            for batch_idx, batch in enumerate(batches):
                batch_start_time = time.time()

                # Execute batch in parallel
                tasks = [router.route_task(prompt, "auto") for prompt in batch]
                results = await asyncio.gather(*tasks)

                batch_latency = time.time() - batch_start_time
                batch_latencies.append(batch_latency)
                all_results.extend(results)

                # Small delay between batches to respect rate limits
                if batch_idx < len(batches) - 1:
                    await asyncio.sleep(0.5)

            total_latency = time.time() - batch_start
            total_latencies.append(total_latency)

            print(".2f")

        return {
            "batch_size": batch_size,
            "avg_batch_latency": statistics.mean(batch_latencies),
            "avg_total_latency": statistics.mean(total_latencies),
            "min_total_latency": min(total_latencies),
            "max_total_latency": max(total_latencies),
            "throughput": len(self.test_prompts) / statistics.mean(total_latencies)
        }

    async def test_concurrent_limit(self, concurrent_limit: int, num_tests: int = 3) -> Dict[str, Any]:
        """Test latency with semaphore limiting concurrent calls"""
        print(f"\n🔥 Testing concurrent limit: {concurrent_limit}")

        semaphore = asyncio.Semaphore(concurrent_limit)
        total_latencies = []

        async def limited_route(prompt: str) -> Any:
            async with semaphore:
                return await router.route_task(prompt, "auto")

        for test_num in range(num_tests):
            print(f"  Test {test_num + 1}/{num_tests}...")

            start_time = time.time()

            # Execute all prompts with concurrency limit
            tasks = [limited_route(prompt) for prompt in self.test_prompts]
            results = await asyncio.gather(*tasks)

            total_latency = time.time() - start_time
            total_latencies.append(total_latency)

            print(".2f")

        return {
            "concurrent_limit": concurrent_limit,
            "avg_total_latency": statistics.mean(total_latencies),
            "min_total_latency": min(total_latencies),
            "max_total_latency": max(total_latencies),
            "throughput": len(self.test_prompts) / statistics.mean(total_latencies)
        }

    async def run_optimization_tests(self):
        """Run comprehensive latency optimization tests"""
        print("🚀 AXIOM-X LATENCY OPTIMIZATION SMOKE TESTS")
        print("=" * 60)

        results = {
            "batch_size_tests": [],
            "concurrency_tests": [],
            "recommendations": {}
        }

        # Test different batch sizes
        print("\n📊 TESTING BATCH SIZE IMPACT")
        batch_sizes = [1, 2, 3, 4, 5, 6, 8, 10]

        for batch_size in batch_sizes:
            result = await self.test_batch_size(batch_size)
            results["batch_size_tests"].append(result)

        # Test different concurrency limits
        print("\n⚡ TESTING CONCURRENCY LIMIT IMPACT")
        concurrent_limits = [3, 5, 8, 10, 15, 20]

        for limit in concurrent_limits:
            result = await self.test_concurrent_limit(limit)
            results["concurrency_tests"].append(result)

        # Analyze results
        await self.analyze_results(results)

        # Save results
        output_file = Path("self-optimization/latency_optimization_results.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n💾 Results saved to {output_file}")

    async def analyze_results(self, results: Dict[str, Any]):
        """Analyze test results and provide recommendations"""
        print("\n📈 ANALYSIS & RECOMMENDATIONS")
        print("=" * 40)

        # Find optimal batch size
        batch_tests = results["batch_size_tests"]
        if batch_tests:
            best_batch = max(batch_tests, key=lambda x: x["throughput"])
            print("🏆 Best Batch Size Performance:")
            print(f"   Size: {best_batch['batch_size']}")
            print(".2f")
            print(".2f")

        # Find optimal concurrency
        concurrency_tests = results["concurrency_tests"]
        if concurrency_tests:
            best_concurrency = max(concurrency_tests, key=lambda x: x["throughput"])
            print("🏆 Best Concurrency Performance:")
            print(f"   Limit: {best_concurrency['concurrent_limit']}")
            print(".2f")
            print(".2f")

        # Calculate improvements
        if len(batch_tests) > 1:
            baseline_throughput = batch_tests[0]["throughput"]  # batch_size = 1
            max_throughput = max(t["throughput"] for t in batch_tests)
            improvement = ((max_throughput - baseline_throughput) / baseline_throughput) * 100
            print(".1f")

        if len(concurrency_tests) > 1:
            baseline_throughput = concurrency_tests[0]["throughput"]  # concurrent_limit = 3
            max_throughput = max(t["throughput"] for t in concurrency_tests)
            improvement = ((max_throughput - baseline_throughput) / baseline_throughput) * 100
            print(".1f")

        # Recommendations
        recommendations = {}

        if batch_tests:
            optimal_batch = max(batch_tests, key=lambda x: x["throughput"])
            recommendations["optimal_batch_size"] = optimal_batch["batch_size"]
            recommendations["expected_throughput_batch"] = optimal_batch["throughput"]

        if concurrency_tests:
            optimal_concurrency = max(concurrency_tests, key=lambda x: x["throughput"])
            recommendations["optimal_concurrency_limit"] = optimal_concurrency["concurrent_limit"]
            recommendations["expected_throughput_concurrency"] = optimal_concurrency["throughput"]

        # Combined recommendation
        if batch_tests and concurrency_tests:
            best_batch = max(batch_tests, key=lambda x: x["throughput"])
            best_concurrency = max(concurrency_tests, key=lambda x: x["throughput"])

            recommendations["combined_strategy"] = {
                "batch_size": best_batch["batch_size"],
                "concurrency_limit": best_concurrency["concurrent_limit"],
                "estimated_total_throughput": min(best_batch["throughput"], best_concurrency["throughput"])
            }

        results["recommendations"] = recommendations

        print("\n🎯 RECOMMENDATIONS:")
        print(f"   Optimal batch size: {recommendations.get('optimal_batch_size', 'N/A')}")
        print(f"   Optimal concurrency: {recommendations.get('optimal_concurrency_limit', 'N/A')}")
        print(".1f")

async def main():
    """Main entry point"""
    optimizer = LatencyOptimizer()
    await optimizer.run_optimization_tests()

if __name__ == "__main__":
    asyncio.run(main())