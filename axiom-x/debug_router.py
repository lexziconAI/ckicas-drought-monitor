#!/usr/bin/env python3
"""
AXIOM-X LLM ROUTER DEBUG SCRIPT
Tests each provider individually to identify failures
"""

import os
import asyncio
import sys
from dotenv import load_dotenv

load_dotenv()

async def test_single_provider(provider_name):
    """Test a single provider with detailed error reporting"""
    print(f"\n🧪 Testing {provider_name.upper()}...")

    try:
        if provider_name == 'anthropic':
            from anthropic import Anthropic
            client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            response = client.messages.create(
                model='claude-sonnet-4-5-20250929',
                max_tokens=50,
                messages=[{"role": "user", "content": "Say 'ANTHROPIC_OK'"}]
            )
            result = response.content[0].text
            print(f"✅ ANTHROPIC: {result.strip()}")

        elif provider_name == 'openai':
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            response = client.chat.completions.create(
                model='gpt-5',
                max_tokens=50,
                messages=[{"role": "user", "content": "Say 'OPENAI_OK'"}]
            )
            result = response.choices[0].message.content
            print(f"✅ OPENAI: {result.strip()}")

        elif provider_name == 'google':
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content("Say 'GOOGLE_OK'")
            result = response.text
            print(f"✅ GOOGLE: {result.strip()}")

        elif provider_name == 'groq':
            from groq import Groq
            client = Groq(api_key=os.getenv('GROQ_API_KEY'))
            response = client.chat.completions.create(
                model='llama-3.3-70b-versatile',
                max_tokens=50,
                messages=[{"role": "user", "content": "Say 'GROQ_OK'"}]
            )
            result = response.choices[0].message.content
            print(f"✅ GROQ: {result.strip()}")

        elif provider_name == 'cohere':
            import cohere
            client = cohere.Client(os.getenv('COHERE_API_KEY'))
            response = client.chat(
                model='command-a-03-2025',
                message="Say 'COHERE_OK'",
                max_tokens=50
            )
            result = response.text
            print(f"✅ COHERE: {result.strip()}")

        elif provider_name == 'fireworks':
            from openai import OpenAI
            client = OpenAI(
                api_key=os.getenv('FIREWORKS_API_KEY'),
                base_url="https://api.fireworks.ai/inference/v1"
            )
            response = client.chat.completions.create(
                model='accounts/fireworks/models/llama-v3p3-70b-instruct',
                max_tokens=50,
                messages=[{"role": "user", "content": "Say 'FIREWORKS_OK'"}]
            )
            result = response.choices[0].message.content
            print(f"✅ FIREWORKS: {result.strip()}")

        return True

    except Exception as e:
        print(f"❌ {provider_name.upper()}: {str(e)}")
        return False

async def debug_router():
    """Debug the LLM router by testing each provider"""
    print("🔍 AXIOM-X LLM ROUTER DEBUG")
    print("=" * 50)

    providers = ['anthropic', 'openai', 'google', 'groq', 'cohere', 'fireworks']
    working = 0
    failed = 0

    for provider in providers:
        if await test_single_provider(provider):
            working += 1
        else:
            failed += 1

    print(f"\n📊 RESULTS: {working} working, {failed} failed")

    if working == 0:
        print("🚨 CRITICAL: No providers working!")
        print("   Check API keys and network connectivity")
    elif working < 3:
        print("⚠️  WARNING: Limited provider availability")
        print("   TURBO mode may be degraded")
    else:
        print("✅ GOOD: Sufficient providers available")

    return working > 0

if __name__ == "__main__":
    asyncio.run(debug_router())