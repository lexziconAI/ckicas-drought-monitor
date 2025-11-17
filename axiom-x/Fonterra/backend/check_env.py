#!/usr/bin/env python3
"""
CKICAS Environment Configuration Checker
"""

import os
from dotenv import load_dotenv

def check_env_config():
    """Check current environment configuration"""
    load_dotenv()

    print('🔍 CKICAS Environment Configuration Check')
    print('=' * 50)

    # Check API keys
    openweather = os.getenv('OPENWEATHER_API_KEY')
    anthropic = os.getenv('ANTHROPIC_API_KEY')
    niwa = os.getenv('NIWA_API_KEY')

    print(f'OPENWEATHER_API_KEY: {"✅ Configured" if openweather and openweather != "your_openweather_api_key_here" else "❌ Not configured"}')
    print(f'ANTHROPIC_API_KEY: {"✅ Configured" if anthropic and anthropic != "your_anthropic_api_key_here" else "❌ Not configured (Demo mode active)"}')
    print(f'NIWA_API_KEY: {"✅ Configured" if niwa and niwa != "your_niwa_api_key_here" else "❌ Not configured"}')

    print()
    print('📋 System Configuration:')
    print(f'PORT: {os.getenv("PORT", "8000")}')
    print(f'ENVIRONMENT: {os.getenv("ENVIRONMENT", "development")}')
    print(f'DATABASE_URL: {os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/drought.db")}')

    print()
    print('🎯 Next Steps:')
    if not (openweather and openweather != "your_openweather_api_key_here"):
        print('1. Get OpenWeather API key: https://openweathermap.org/api')
        print('2. Update OPENWEATHER_API_KEY in .env file')
    else:
        print('✅ OpenWeather API ready!')

    if not (anthropic and anthropic != "your_anthropic_api_key_here"):
        print('• Anthropic API optional (demo mode active)')
    else:
        print('✅ Anthropic Claude API ready!')

    if not (niwa and niwa != "your_niwa_api_key_here"):
        print('• Email Dr. Jochen Schmidt for NIWA DataHub access')
    else:
        print('✅ NIWA DataHub API ready!')

if __name__ == '__main__':
    check_env_config()