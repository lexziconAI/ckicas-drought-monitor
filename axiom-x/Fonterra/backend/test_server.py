import subprocess
import time
import requests

# Start server in background
print('Starting server...')
proc = subprocess.Popen([
    'python', '-c', '''
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting test...")
    try:
        yield
    except Exception as e:
        print(f"❌ Runtime error: {e}")
    finally:
        print("🛑 Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/test")
async def test_endpoint():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8018, log_level="info")
'''
])

# Wait for server to start
time.sleep(3)

# Test the endpoint
print('Testing endpoint...')
try:
    response = requests.get('http://localhost:8018/test', timeout=5)
    print(f'Success! Status: {response.status_code}')
    print(f'Response: {response.json()}')
except Exception as e:
    print(f'Failed: {e}')

# Stop server
print('Stopping server...')
proc.terminate()
proc.wait()
print('Done.')