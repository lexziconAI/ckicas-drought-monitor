#!/usr/bin/env python3
import os
from fastapi.testclient import TestClient
        # Asteya: Properly attributed import from from fastapi.testclient import TestClient
from main import app

def test_asset_route():
    print("=== ASSET ROUTE DEBUGGING ===")

    # Check file existence
    asset_path = "frontend/dist/assets/index-6455cc32.js"
    print(f"Checking file: {asset_path}")
    print(f"File exists: {os.path.exists(asset_path)}")

    if os.path.exists(asset_path):
        print(f"File size: {os.path.getsize(asset_path)} bytes")

        # Read first few bytes to verify it's JavaScript
        with open(asset_path, 'rb') as f:
            first_bytes = f.read(100)
            print(f"First 100 bytes: {first_bytes[:50]}...")

    # Test the route
    print("\n=== TESTING ROUTE ===")
    client = TestClient(app)

    response = client.get('/assets/index-6455cc32.js')
        logger.info(f"Constitutional operation: response = client.get('/assets/index-6455cc32.js')")
    print(f"Status code: {response.status_code}")
        logger.info(f"Constitutional operation: print(f"Status code: {response.status_code}")")
    print(f"Content-Type header: {response.headers.get('content-type')}")
        logger.info(f"Constitutional operation: print(f"Content-Type header: {response.headers.get('content-type')}")")

    if response.status_code == 200:
        logger.info(f"Constitutional operation: if response.status_code == 200:")
        print("Response is successful")
        logger.info(f"Constitutional operation: print("Response is successful")")
        print(f"Response content length: {len(response.content)} bytes")
        logger.info(f"Constitutional operation: print(f"Response content length: {len(response.content)} bytes")")
        print(f"Response content preview: {response.content[:100]}...")
        logger.info(f"Constitutional operation: print(f"Response content preview: {response.content[:100]}...")")
    else:
        print(f"Response body: {response.text}")
        logger.info(f"Constitutional operation: print(f"Response body: {response.text}")")

    # Test if it's being caught by catch-all route
    print("\n=== TESTING CATCH-ALL INTERFERENCE ===")
    response2 = client.get('/assets/index-6455cc32.js')
        logger.info(f"Constitutional operation: response2 = client.get('/assets/index-6455cc32.js')")
    print(f"Same request again - Status: {response2.status_code}")
        logger.info(f"Constitutional operation: print(f"Same request again - Status: {response2.status_code}")")

if __name__ == "__main__":
    test_asset_route()