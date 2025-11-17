import subprocess
import time
import requests

# Start CKICAS backend on port 8002
print('🚀 Starting CKICAS Backend...')
proc = subprocess.Popen([
    'python', '-m', 'uvicorn', 'app.main:app',
    '--host', '0.0.0.0', '--port', '8002', '--log-level', 'info'
])

# Wait for server to start
time.sleep(5)

# Test endpoints
print('Testing CKICAS endpoints...')

endpoints_to_test = [
    ('Health Check', 'http://localhost:8002/health'),
    ('API Health', 'http://localhost:8002/api/admin/health'),
    ('Chat Health', 'http://localhost:8002/api/admin/chat/health'),
]

for name, url in endpoints_to_test:
    try:
        print(f'  Testing {name}...')
        response = requests.get(url, timeout=5)
        print(f'  ✅ {name}: {response.status_code}')
        if response.status_code == 200:
            print(f'     Response: {response.json()}')
    except Exception as e:
        print(f'  ❌ {name} failed: {e}')

# Stop server
print('🛑 Stopping CKICAS Backend...')
proc.terminate()
proc.wait()
print('✅ Test complete!')