#!/usr/bin/env python3
"""
Test script for Phase2 _single_agent_scout resilience
Simulates router responses to validate retry/backoff and JSON parsing fixes
"""

import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, patch
from dataclasses import dataclass

# Import the classes we need
from phase2_constitutional_swarm import Phase2SwarmOrchestrator, SwarmAgent

@dataclass
class MockTaskResult:
    response: str
    provider: str = "mock"
    latency: float = 0.1
    tokens: int = 10
    cost: float = 0.01

async def test_single_agent_scout_resilience():
    """Test _single_agent_scout with various mock responses"""
    print("🧪 TESTING Phase2 Scout Resilience")

    # Create orchestrator
    orchestrator = Phase2SwarmOrchestrator()

    # Create test agent
    agent = SwarmAgent(
        agent_id="test_scout_001",
        role="amendment_scout",
        amendment_target="Amendment 1",
        swarm_tier=1,
        capabilities=["source_identification"]
    )

    # Test cases: (description, mock_response, expected_behavior)
    test_cases = [
        ("Valid JSON array", '["U.S. Constitution (Official)", "12th Amendment Ratification Documents"]', "should return list"),
        ("Empty response", "", "should retry and fail gracefully"),
        ("Malformed JSON", '{"invalid": json}', "should retry and fail gracefully"),
        ("No brackets", "U.S. Constitution (Official), 12th Amendment Ratification Documents", "should retry and fail gracefully"),
        ("Partial JSON", '["U.S. Constitution (Official)"', "should retry and fail gracefully"),
    ]

    for desc, mock_resp, expected in test_cases:
        print(f"\n📋 Testing: {desc}")

        # Mock the router.route_task method
        async def mock_route_task(task, provider, max_tokens):
            return MockTaskResult(response=mock_resp)

        with patch.object(orchestrator.router, 'route_task', side_effect=mock_route_task):
            try:
                result = await orchestrator._single_agent_scout("Amendment 1", agent)
                print(f"   ✅ Result: {result}")
                print(f"   Expected: {expected}")
                if expected == "should return list" and isinstance(result, list):
                    print("   🎯 SUCCESS: Returned valid list")
                elif expected in ["should retry and fail gracefully"] and result == []:
                    print("   🎯 SUCCESS: Failed gracefully with empty list")
                else:
                    print("   ❌ UNEXPECTED: Result doesn't match expectation")
            except Exception as e:
                print(f"   ❌ ERROR: {e}")

    # Check if debug files were created
    debug_dir = orchestrator.output_dir / "debug_responses"
    if debug_dir.exists():
        debug_files = list(debug_dir.glob("*.txt"))
        print(f"\n📁 Debug files created: {len(debug_files)}")
        for f in debug_files[:3]:  # Show first 3
            print(f"   - {f.name}")
    else:
        print("\n📁 No debug files created (expected for successful cases)")

    print("\n🏁 Test completed")

if __name__ == "__main__":
    asyncio.run(test_single_agent_scout_resilience())