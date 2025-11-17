#!/usr/bin/env python3
"""
Test the actual router that TURBO uses
"""

import asyncio
import sys
sys.path.append('.')

from infrastructure.sidecar.router import router

async def test_router():
    """Test the router with a simple task"""
    print("🔍 TESTING AXIOM-X ROUTER")
    print("=" * 30)

    test_task = "Say 'ROUTER_TEST_OK' and nothing else."

    try:
        # Test auto-routing
        print("Testing auto-routing...")
        result = await router.route_task(test_task)
        print(f"✅ Auto-route result: {result.response.strip()}")
        print(f"   Provider: {result.provider}, Latency: {result.latency:.2f}s")

        # Test specific providers
        providers = ["anthropic", "openai", "google", "groq", "cohere", "fireworks"]
        working_providers = []

        for provider in providers:
            try:
                print(f"\nTesting {provider}...")
                result = await router.route_task(test_task, provider)
                if "ROUTER_TEST_OK" in result.response:
                    print(f"✅ {provider}: {result.response.strip()}")
                    working_providers.append(provider)
                else:
                    print(f"⚠️  {provider}: Unexpected response - {result.response[:50]}...")
            except Exception as e:
                print(f"❌ {provider}: {str(e)}")

        print(f"\n📊 WORKING PROVIDERS: {len(working_providers)}/{len(providers)}")
        print(f"   Working: {', '.join(working_providers)}")

        if len(working_providers) >= 4:
            print("✅ TURBO MODE READY")
            return True
        else:
            print("❌ INSUFFICIENT PROVIDERS")
            return False

    except Exception as e:
        print(f"❌ ROUTER TEST FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_router())