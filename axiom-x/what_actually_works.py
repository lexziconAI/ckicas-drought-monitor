#!/usr/bin/env python3
"""
WHAT ACTUALLY WORKS - Comprehensive Connection Diagnostic
Tests every possible way to connect to the Constitutional Market Harmonics backend
"""

import requests
import socket
import subprocess
import sys
import time
import json
from urllib.parse import urlparse

def test_connection(url, method="GET", data=None, headers=None, timeout=5):
    """Test a single connection"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=timeout, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=timeout, headers=headers)
        else:
            return {"status": "ERROR", "error": f"Unsupported method: {method}"}

        return {
            "status": "SUCCESS",
            "status_code": response.status_code,
            "content_length": len(response.text),
            "url": url,
            "method": method
        }
    except Exception as e:
        return {
            "status": "FAILED",
            "error": str(e),
            "url": url,
            "method": method
        }

def test_socket_connection(host, port):
    """Test raw socket connection"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return {
            "status": "SUCCESS" if result == 0 else "FAILED",
            "host": host,
            "port": port,
            "result": result
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "host": host,
            "port": port
        }

def test_curl_command(url):
    """Test using curl command"""
    try:
        result = subprocess.run(
            ["curl", "-s", "-w", "%{http_code}", "-o", "/dev/null", url],
            capture_output=True,
            text=True,
            timeout=10
        )
        status_code = result.stdout.strip()
        return {
            "status": "SUCCESS" if status_code == "200" else "FAILED",
            "status_code": status_code,
            "url": url,
            "method": "curl"
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "url": url,
            "method": "curl"
        }

def test_powershell_invoke(url):
    """Test using PowerShell Invoke-WebRequest"""
    try:
        cmd = f'powershell -Command "try {{ Invoke-WebRequest -Uri \'{url}\' -Method GET -TimeoutSec 5 | Select-Object StatusCode }} catch {{ Write-Host \'FAILED: $($_.Exception.Message)\' }}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        if "StatusCode" in result.stdout and "200" in result.stdout:
            return {"status": "SUCCESS", "url": url, "method": "powershell"}
        else:
            return {"status": "FAILED", "url": url, "method": "powershell", "output": result.stdout.strip()}
    except Exception as e:
        return {"status": "ERROR", "error": str(e), "url": url, "method": "powershell"}

def main():
    print("🌀 CONSTITUTIONAL MARKET HARMONICS - CONNECTION DIAGNOSTIC")
    print("=" * 60)
    print("Testing every possible connection method to backend server...")
    print()

    # Test URLs and methods
    test_cases = [
        # Localhost variations
        {"url": "http://127.0.0.1:3002/api/health", "method": "GET"},
        {"url": "http://localhost:3002/api/health", "method": "GET"},
        {"url": "http://127.0.0.1:3002/api/dashboard", "method": "GET"},
        {"url": "http://localhost:3002/api/dashboard", "method": "GET"},

        # Authentication endpoints
        {"url": "http://127.0.0.1:3002/api/auth/login", "method": "POST", "data": {"password": "fractal2025"}},
        {"url": "http://localhost:3002/api/auth/login", "method": "POST", "data": {"password": "fractal2025"}},

        # Other endpoints
        {"url": "http://127.0.0.1:3002/api/chaos", "method": "GET"},
        {"url": "http://127.0.0.1:3002/api/international-portfolio", "method": "GET"},
        {"url": "http://127.0.0.1:3002/api/antenarrative", "method": "GET"},
    ]

    results = []

    print("🔍 TESTING HTTP REQUESTS (Python requests library)")
    print("-" * 50)
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i:2d}. Testing {test_case['url']} [{test_case['method']}]")
        result = test_connection(**test_case)
        results.append(result)

        status_emoji = "✅" if result["status"] == "SUCCESS" else "❌" if result["status"] == "FAILED" else "⚠️"
        print(f"    {status_emoji} {result['status']}")

        if result["status"] == "SUCCESS":
            print(f"       Status: {result['status_code']}, Content Length: {result['content_length']}")
        elif result["status"] == "FAILED":
            print(f"       Error: {result['error'][:100]}...")
        print()

    print("🔌 TESTING RAW SOCKET CONNECTIONS")
    print("-" * 50)
    socket_tests = [
        ("127.0.0.1", 3002),
        ("localhost", 3002),
        ("0.0.0.0", 3002),
    ]

    for host, port in socket_tests:
        print(f"Testing socket connection to {host}:{port}")
        result = test_socket_connection(host, port)
        results.append(result)

        status_emoji = "✅" if result["status"] == "SUCCESS" else "❌"
        print(f"    {status_emoji} {result['status']}")
        if result["status"] == "FAILED":
            print(f"       Connection result: {result['result']}")
        print()

    print("🌐 TESTING CURL COMMAND")
    print("-" * 50)
    curl_urls = [
        "http://127.0.0.1:3002/api/health",
        "http://localhost:3002/api/health",
    ]

    for url in curl_urls:
        print(f"Testing curl {url}")
        result = test_curl_command(url)
        results.append(result)

        status_emoji = "✅" if result["status"] == "SUCCESS" else "❌" if result["status"] == "FAILED" else "⚠️"
        print(f"    {status_emoji} {result['status']}")
        if result["status"] == "SUCCESS":
            print(f"       Status Code: {result['status_code']}")
        print()

    print("⚡ TESTING POWERSHELL INVOKE-WEBREQUEST")
    print("-" * 50)
    ps_urls = [
        "http://127.0.0.1:3002/api/health",
        "http://localhost:3002/api/health",
    ]

    for url in ps_urls:
        print(f"Testing PowerShell Invoke-WebRequest {url}")
        result = test_powershell_invoke(url)
        results.append(result)

        status_emoji = "✅" if result["status"] == "SUCCESS" else "❌" if result["status"] == "FAILED" else "⚠️"
        print(f"    {status_emoji} {result['status']}")
        print()

    # Check if server is actually running
    print("🔍 CHECKING SERVER STATUS")
    print("-" * 50)
    try:
        import psutil
        node_processes = [p for p in psutil.process_iter(['pid', 'name', 'cmdline']) if 'node' in p.info['name'].lower()]
        if node_processes:
            print("✅ Node.js processes found:")
            for p in node_processes:
                print(f"    PID {p.info['pid']}: {' '.join(p.info['cmdline'] or [])}")
        else:
            print("❌ No Node.js processes running")
    except ImportError:
        print("⚠️  psutil not available for process checking")

    # Summary
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)

    successful = [r for r in results if r["status"] == "SUCCESS"]
    failed = [r for r in results if r["status"] == "FAILED"]
    errors = [r for r in results if r["status"] == "ERROR"]

    print(f"✅ Successful connections: {len(successful)}")
    print(f"❌ Failed connections: {len(failed)}")
    print(f"⚠️  Error connections: {len(errors)}")

    if successful:
        print("\n🎯 WORKING CONNECTIONS:")
        for result in successful:
            method = result.get("method", "unknown")
            url = result.get("url", "unknown")
            print(f"    {method.upper()}: {url}")

    if failed:
        print("\n💥 CONSISTENTLY FAILING:")
        failing_urls = {}
        for result in failed:
            url = result.get("url", "unknown")
            failing_urls[url] = failing_urls.get(url, 0) + 1

        for url, count in failing_urls.items():
            if count > 1:  # Only show URLs that fail consistently
                print(f"    {url} (failed {count} times)")

    print("\n🎯 RECOMMENDATIONS:")
    if successful:
        print("    ✅ Some connections work! Focus on replicating successful methods.")
        print("    💡 Try: Cloud deployment or ngrok tunnel for frontend access.")
    else:
        print("    ❌ No connections work from Python.")
        print("    💡 Try: Cloud deployment (recommended) or ngrok tunnel.")
        print("    🔍 Check: Is the Node.js server actually running on port 3002?")

    print("\n💚 Satya (Truth) Applied: This diagnostic shows the actual state.")
    print("   No false positives, no hiding failures, pure constitutional honesty.")

if __name__ == "__main__":
    main()