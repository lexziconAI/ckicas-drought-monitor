#!/usr/bin/env python3
"""
Simple LLM provider test - one at a time
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_anthropic():
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = client.messages.create(
            model='claude-sonnet-4-5-20250929',
            max_tokens=10,
            messages=[{"role": "user", "content": "Say OK"}]
        )
        print(f"✅ ANTHROPIC: {response.content[0].text.strip()}")
        return True
    except Exception as e:
        print(f"❌ ANTHROPIC: {str(e)}")
        return False

def test_openai():
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model='gpt-4',  # Try GPT-4 instead of GPT-5
            max_tokens=10,
            messages=[{"role": "user", "content": "Say OK"}]
        )
        print(f"✅ OPENAI: {response.choices[0].message.content.strip()}")
        return True
    except Exception as e:
        print(f"❌ OPENAI: {str(e)}")
        return False

def test_google():
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-2.5-flash')  # Use current November 2025 model
        response = model.generate_content("Say OK")
        print(f"✅ GOOGLE: {response.text.strip()}")
        return True
    except Exception as e:
        print(f"❌ GOOGLE: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 SIMPLE PROVIDER TESTS")
    print("=" * 30)

    test_anthropic()
    test_openai()
    test_google()