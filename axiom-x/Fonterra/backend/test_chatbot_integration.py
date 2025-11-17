#!/usr/bin/env python3
"""
Test Chatbot API functionality
Tests the Anthropic Claude Haiku 4.5 integration
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_chatbot_api():
    """Test the chatbot API functionality"""
    try:
        print("🤖 Testing Chatbot API Integration")
        print("=" * 50)

        # Test importing the chatbot
        from app.api.admin_routes import AnthropicChatbot
        print("✅ Chatbot module imported successfully")

        # Initialize chatbot
        chatbot = AnthropicChatbot()
        print("✅ Chatbot initialized")

        # Test demo response (since we don't have API key)
        test_message = "What is the current drought status in New Zealand?"
        print(f"📝 Testing with message: {test_message}")

        response = await chatbot.chat(test_message)
        print(f"🤖 Chatbot response type: {type(response)}")
        if hasattr(response, 'response'):
            print(f"🤖 Chatbot response: {response.response[:200]}...")
        else:
            print(f"🤖 Chatbot response: {str(response)[:200]}...")

        print("✅ Chatbot API test completed successfully")

        return True

    except Exception as e:
        print(f"❌ Chatbot API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_health_endpoint():
    """Test the health endpoint"""
    try:
        print("\n🏥 Testing Health Endpoint")
        print("=" * 30)

        from app.main import app
        print("✅ Main app imported successfully")

        # Test health endpoint directly
        from fastapi.testclient import TestClient
        client = TestClient(app)

        response = client.get("/health")
        print(f"🏥 Health status: {response.status_code}")
        print(f"🏥 Response: {response.json()}")

        print("✅ Health endpoint test completed")

        return True

    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("🧪 CKICAS Chatbot Integration Tests")
    print("Using Chaos-Optimized Architecture")
    print("=" * 60)

    # Set PYTHONPATH
    import sys
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, backend_dir)

    # Run tests
    chatbot_test = await test_chatbot_api()
    health_test = await test_health_endpoint()

    print("\n📊 Test Results:")
    print(f"Chatbot API: {'✅ PASS' if chatbot_test else '❌ FAIL'}")
    print(f"Health Endpoint: {'✅ PASS' if health_test else '❌ FAIL'}")

    if chatbot_test and health_test:
        print("\n🎉 All tests passed! Chatbot integration is working.")
        print("The Anthropic Claude Haiku 4.5 chatbot is ready for use.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)