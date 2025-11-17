import asyncio
import sys
from pathlib import Path

# Add infrastructure path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "infrastructure"))
sys.path.append(str(Path(__file__).parent / "infrastructure" / "sidecar"))

from infrastructure.sidecar.router import router

async def test_single_debate():
    prompt = "You are anthropic-sonnet. Provide your opening thesis on optimal Axiom-X self-optimization strategy. Focus on: How should we identify canonical implementations? What redundancy patterns matter most? How to mine constitutional receipts effectively?"

    print("Testing single debate turn...")
    result = await router.route_task(prompt, "anthropic")
    print(f"Response: {result.response[:200]}...")
    print(f"Success! Latency: {result.latency:.2f}s")

if __name__ == "__main__":
    asyncio.run(test_single_debate())