import subprocess
import time
import requests
import json

# Start CKICAS backend
print('🚀 Starting CKICAS Backend...')
proc = subprocess.Popen([
    'python', '-m', 'uvicorn', 'app.main:app',
    '--host', '0.0.0.0', '--port', '8001', '--log-level', 'info'
])

# Wait for server to start
time.sleep(5)

# Test endpoints with detailed error reporting
print('Testing CKICAS endpoints...')

endpoints_to_test = [
    ('Health Check', 'http://localhost:8001/health'),
    ('API Health', 'http://localhost:8001/api/admin/health'),
    ('Chat Health', 'http://localhost:8001/api/admin/chat/health'),
]

for name, url in endpoints_to_test:
    try:
        print(f'\n  Testing {name} ({url})...')
        response = requests.get(url, timeout=10)
        print(f'  ✅ Status: {response.status_code}')

        if response.status_code == 200:
            try:
                data = response.json()
                print(f'     Response: {json.dumps(data, indent=2)[:500]}...')
            except:
                print(f'     Raw Response: {response.text[:500]}...')
        else:
            print(f'  ❌ Error Response:')
            try:
                error_data = response.json()
                print(f'     {json.dumps(error_data, indent=2)}')
            except:
                print(f'     Raw Error: {response.text}')

    except requests.exceptions.RequestException as e:
        print(f'  ❌ Request failed: {e}')

# Stop server
print('\n🛑 Stopping CKICAS Backend...')
proc.terminate()
proc.wait()
print('✅ Test complete!')