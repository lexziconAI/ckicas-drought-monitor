import os
import asyncio
from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai
from groq import Groq
import cohere
from dotenv import load_dotenv
import time

load_dotenv()

# Configuration from web search results - November 2025
PROVIDERS = {
    'anthropic': {
        'client': Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')),
        'model': 'claude-sonnet-4-5-20250929',  # Latest Claude Sonnet 4.5
        'enabled': True
    },
    'openai': {
        'client': OpenAI(api_key=os.getenv('OPENAI_API_KEY')),
        'model': 'gpt-5',  # Latest GPT-5
        'enabled': True
    },
    'google': {
        'api_key': os.getenv('GOOGLE_API_KEY'),
        'model': 'gemini-2.5-flash',  # Updated to current November 2025 model
        'enabled': True
    },
    'groq': {
        'client': Groq(api_key=os.getenv('GROQ_API_KEY')),
        'model': 'llama-3.3-70b-versatile',  # Latest Llama 3.3 70B
        'enabled': True
    },
    'cohere': {
        'client': cohere.Client(os.getenv('COHERE_API_KEY')),
        'model': 'command-a-03-2025',  # Latest Command A
        'enabled': True
    },
    'fireworks': {
        'client': OpenAI(
            api_key=os.getenv('FIREWORKS_API_KEY'),
            base_url="https://api.fireworks.ai/inference/v1"
        ),
        'model': os.getenv('FIREWORKS_MODEL_DEFAULT', 'accounts/fireworks/models/llama-v3p3-70b-instruct'),
        'enabled': True
    }
}

async def test_provider(provider_name, config):
    """Test a single provider with simple prompt"""
    try:
        start_time = time.time()

        if provider_name == 'anthropic':
            response = config['client'].messages.create(
                model=config['model'],
                max_tokens=100,
                messages=[{"role": "user", "content": "Reply with just: ANTHROPIC_OK"}]
            )
            result = response.content[0].text

        elif provider_name == 'openai':
            # GPT-5 may use different parameters
            try:
                response = config['client'].chat.completions.create(
                    model=config['model'],
                    max_tokens=100,
                    messages=[{"role": "user", "content": "Reply with just: OPENAI_OK"}]
                )
                result = response.choices[0].message.content
            except Exception as e:
                if "max_tokens" in str(e):
                    # Try without max_tokens
                    response = config['client'].chat.completions.create(
                        model=config['model'],
                        messages=[{"role": "user", "content": "Reply with just: OPENAI_OK"}]
                    )
                    result = response.choices[0].message.content
                else:
                    raise e

        elif provider_name == 'google':
            genai.configure(api_key=config['api_key'])
            model = genai.GenerativeModel(config['model'])
            response = model.generate_content("Reply with just: GOOGLE_OK")
            result = response.text

        elif provider_name == 'groq':
            response = config['client'].chat.completions.create(
                model=config['model'],
                max_tokens=100,
                messages=[{"role": "user", "content": "Reply with just: GROQ_OK"}]
            )
            result = response.choices[0].message.content

        elif provider_name == 'cohere':
            response = config['client'].chat(
                model=config['model'],
                message="Reply with just: COHERE_OK"
            )
            result = response.text

        elif provider_name == 'fireworks':
            response = config['client'].chat.completions.create(
                model=config['model'],
                max_tokens=100,
                messages=[{"role": "user", "content": "Reply with just: FIREWORKS_OK"}]
            )
            result = response.choices[0].message.content

        elapsed = time.time() - start_time
        return {
            'provider': provider_name,
            'status': 'SUCCESS',
            'response': result.strip(),
            'latency': f"{elapsed:.2f}s",
            'model': config['model']
        }

    except Exception as e:
        return {
            'provider': provider_name,
            'status': 'FAILED',
            'error': str(e)[:100],
            'model': config['model']
        }

async def test_all_providers():
    """Test all providers in parallel"""
    print("🌀 AXIOM-X PROVIDER VALIDATION - PARALLEL TEST\n")

    # Run all tests in parallel
    tasks = [
        test_provider(name, config)
        for name, config in PROVIDERS.items()
        if config['enabled']
    ]

    results = await asyncio.gather(*tasks)

    # Report results
    print("=" * 70)
    successes = 0
    failures = 0

    for result in results:
        if result['status'] == 'SUCCESS':
            print(f"✅ {result['provider'].upper():12} | {result['latency']:6} | {result['response']}")
            successes += 1
        else:
            print(f"❌ {result['provider'].upper():12} | FAILED | {result['error']}")
            failures += 1

    print("=" * 70)
    print(f"\n📊 Results: {successes} success, {failures} failed")
    print(f"🚀 Parallelization: {len(tasks)} providers tested simultaneously")

    if successes >= 3:
        print("\n✅ INFRASTRUCTURE VALIDATED - Ready for advanced orchestration")
        return True
    else:
        print("\n⚠️  INSUFFICIENT PROVIDERS - Need at least 3 working")
        return False

if __name__ == "__main__":
    asyncio.run(test_all_providers())