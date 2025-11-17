#!/usr/bin/env python3
"""
Complete LLM provider test - all providers
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_provider(provider_name):
    """Test a single provider"""
    print(f"\n🧪 Testing {provider_name.upper()}...")

    try:
        if provider_name == 'anthropic':
            from anthropic import Anthropic
            client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            response = client.messages.create(
                model='claude-sonnet-4-5-20250929',
                max_tokens=10,
                messages=[{"role": "user", "content": "Say OK"}]
            )
            result = response.content[0].text.strip()

        elif provider_name == 'openai':
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            response = client.chat.completions.create(
                model='gpt-5',
                max_tokens=10,
                messages=[{"role": "user", "content": "Say OK"}]
            )
            result = response.choices[0].message.content.strip()

        elif provider_name == 'google':
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content("Say OK")
            result = response.text.strip()

        elif provider_name == 'groq':
            from groq import Groq
            client = Groq(api_key=os.getenv('GROQ_API_KEY'))
            response = client.chat.completions.create(
                model='llama-3.3-70b-versatile',
                max_tokens=10,
                messages=[{"role": "user", "content": "Say OK"}]
            )
            result = response.choices[0].message.content.strip()

        elif provider_name == 'cohere':
            import cohere
            client = cohere.Client(os.getenv('COHERE_API_KEY'))
            response = client.chat(
                model='command-a-03-2025',
                message="Say OK",
                max_tokens=10
            )
            result = response.text.strip()

        elif provider_name == 'fireworks':
            from openai import OpenAI
            client = OpenAI(
                api_key=os.getenv('FIREWORKS_API_KEY'),
                base_url="https://api.fireworks.ai/inference/v1"
            )
            response = client.chat.completions.create(
                model='accounts/fireworks/models/llama-v3p3-70b-instruct',
                max_tokens=10,
                messages=[{"role": "user", "content": "Say OK"}]
            )
            result = response.choices[0].message.content.strip()

        print(f"✅ {provider_name.upper()}: {result}")
        return True

    except Exception as e:
        print(f"❌ {provider_name.upper()}: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 COMPLETE PROVIDER TESTS")
    print("=" * 40)

    providers = ['anthropic', 'openai', 'google', 'groq', 'cohere', 'fireworks']
    working = 0

    for provider in providers:
        if test_provider(provider):
            working += 1

    print(f"\n📊 RESULTS: {working}/{len(providers)} providers working")

    if working >= 4:
        print("✅ TURBO MODE READY - Sufficient providers available")
    else:
        print("⚠️  LIMITED PROVIDERS - TURBO mode may be degraded")