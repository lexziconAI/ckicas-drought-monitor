#!/usr/bin/env python3
"""
CKICAS System Integration Test
Tests all endpoints with real data integration
"""

import requests
import json
import time
import subprocess
import sys

def test_ckicas_system():
    """Comprehensive system integration test"""

    print('🚀 CKICAS System Integration Test')
    print('=' * 50)

    # Start backend server
    print('📡 Starting CKICAS Backend...')
    server_process = subprocess.Popen([
        'python', '-m', 'uvicorn', 'app.main:app',
        '--host', '0.0.0.0', '--port', '8003', '--log-level', 'info'
    ])

    # Wait for server to start
    print('⏳ Waiting for server startup...')
    time.sleep(8)

    base_url = 'http://localhost:8003'
    results = {}

    # Test endpoints
    endpoints_to_test = [
        ('Health Check', f'{base_url}/health', 'GET'),
        ('API Regions', f'{base_url}/api/regions', 'GET'),
        ('Admin Health', f'{base_url}/api/admin/health', 'GET'),
        ('Chat Health', f'{base_url}/api/admin/chat/health', 'GET'),
        ('Drought Data (Waikato)', f'{base_url}/api/drought-data?lat=-37.7&lon=175.2&region=Waikato&forecast_days=7', 'GET'),
        ('Alerts', f'{base_url}/api/alerts', 'GET'),
    ]

    for name, url, method in endpoints_to_test:
        try:
            print(f'🔍 Testing {name}...')
            if method == 'GET':
                response = requests.get(url, timeout=15)
            else:
                response = requests.post(url, timeout=15)

            results[name] = {
                'status': response.status_code,
                'success': response.status_code == 200,
                'data_length': len(response.text)
            }

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f'  ✅ {name}: {response.status_code} - {len(data)} items')
                    if name == 'Health Check':
                        print(f'     Status: {data.get("status", "unknown")}')
                    elif name == 'Admin Health':
                        print(f'     System Status: {data.get("status", "unknown")}')
                        print(f'     Components: {len(data.get("components", {}))} operational')
                except:
                    print(f'  ✅ {name}: {response.status_code} - {len(response.text)} chars')
            else:
                print(f'  ❌ {name}: {response.status_code}')
                try:
                    error_data = response.json()
                    print(f'     Error: {error_data.get("detail", "Unknown error")}')
                except:
                    print(f'     Raw Error: {response.text[:100]}...')

        except requests.exceptions.RequestException as e:
            print(f'  ❌ {name}: Request failed - {e}')
            results[name] = {'status': 'ERROR', 'success': False, 'error': str(e)}

    # Test chatbot if Anthropic key is configured
    try:
        print('🤖 Testing Chatbot...')
        chat_response = requests.post(
            f'{base_url}/api/admin/chat',
            json={'message': 'What is the current drought status?'},
            timeout=15
        )
        if chat_response.status_code == 200:
            print('  ✅ Chatbot: Working')
            results['Chatbot'] = {'status': 200, 'success': True}
        else:
            print(f'  ⚠️  Chatbot: {chat_response.status_code} (Demo mode?)')
            results['Chatbot'] = {'status': chat_response.status_code, 'success': False}
    except Exception as e:
        print(f'  ⚠️  Chatbot: Error - {e}')
        results['Chatbot'] = {'status': 'ERROR', 'success': False, 'error': str(e)}

    # Stop server
    print('🛑 Stopping server...')
    server_process.terminate()
    server_process.wait()

    # Summary
    print('\n📊 Test Results Summary:')
    print('=' * 30)

    successful = 0
    total = len(results)

    for name, result in results.items():
        status = '✅' if result.get('success') else '❌'
        print(f'{status} {name}: {result.get("status", "UNKNOWN")}')

        if result.get('success'):
            successful += 1

    print(f'\n🎯 Overall: {successful}/{total} endpoints working ({successful/total*100:.1f}%)')

    if successful == total:
        print('🎉 ALL SYSTEMS OPERATIONAL! Ready for production deployment.')
        return True
    elif successful >= total * 0.8:
        print('✅ MOSTLY OPERATIONAL! Minor issues to address.')
        return True
    else:
        print('⚠️  ISSUES DETECTED! Check configuration and API keys.')
        return False

if __name__ == '__main__':
    success = test_ckicas_system()
    sys.exit(0 if success else 1)