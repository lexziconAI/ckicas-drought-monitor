#!/usr/bin/env python3
"""
🚨 CONSTITUTIONAL AI REALITY CHECK DIAGNOSTIC
==============================================

Principle: Satya (Truth) - Test claims vs reality
Offender: IDE claiming success without verification
Violation: AI Hallucination - unverified success claims

This script tests ACTUAL state vs IDE claims.
"""

import socket
import subprocess
import sys
import time
from pathlib import Path

def run_command(cmd, shell=True):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=10)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def test_port(host, port):
    """Test if port is actually accessible"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_processes():
    """Check if Node.js processes are actually running"""
    print("🔍 CHECKING PROCESSES...")
    print("=" * 50)

    # Check for node processes
    code, stdout, stderr = run_command("tasklist /FI \"IMAGENAME eq node.exe\" /NH")
    if code == 0 and stdout.strip():
        print("✅ Node.js processes found:")
        lines = stdout.strip().split('\n')
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    print(f"   PID: {parts[1]} - {parts[0]}")
    else:
        print("❌ NO Node.js processes running!")
        return False

    return True

def check_ports():
    """Check if ports are actually listening"""
    print("\n🔍 CHECKING PORTS...")
    print("=" * 50)

    # Check port 3000
    code, stdout, stderr = run_command('netstat -ano | findstr ":3000"')
    if code == 0 and stdout.strip():
        print("✅ Port 3000 is listening:")
        lines = stdout.strip().split('\n')
        for line in lines:
            if line.strip():
                print(f"   {line.strip()}")
    else:
        print("❌ Port 3000 is NOT listening!")
        return False

    # Check port 3002
    code, stdout, stderr = run_command('netstat -ano | findstr ":3002"')
    if code == 0 and stdout.strip():
        print("✅ Port 3002 is listening (API server):")
        lines = stdout.strip().split('\n')
        for line in lines:
            if line.strip():
                print(f"   {line.strip()}")
    else:
        print("❌ Port 3002 is NOT listening!")

    return True

def test_connections():
    """Test actual HTTP connections"""
    print("\n🔍 TESTING CONNECTIONS...")
    print("=" * 50)

    urls = [
        ("localhost", 3000, "Next.js Dashboard"),
        ("127.0.0.1", 3000, "Next.js Dashboard (IPv4)"),
        ("localhost", 3002, "API Server"),
        ("127.0.0.1", 3002, "API Server (IPv4)")
    ]

    results = {}
    for host, port, desc in urls:
        print(f"Testing {desc} ({host}:{port})...")

        # Test socket connection
        socket_ok = test_port(host, port)
        print(f"   Socket: {'✅' if socket_ok else '❌'}")

        # Test HTTP connection
        try:
            import urllib.request
            req = urllib.request.Request(f"http://{host}:{port}/", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                http_ok = response.status == 200
                print(f"   HTTP: ✅ (Status: {response.status})")
        except Exception as e:
            http_ok = False
            print(f"   HTTP: ❌ ({str(e)[:50]}...)")

        results[f"{host}:{port}"] = socket_ok or http_ok

    return results

def analyze_findings(processes_ok, ports_ok, connections):
    """Analyze findings and provide recommendations"""
    print("\n🎯 ANALYSIS & RECOMMENDATIONS")
    print("=" * 50)

    issues = []

    if not processes_ok:
        issues.append("❌ No Node.js processes running")
        print("CRITICAL: Next.js server is not running!")
        print("SOLUTION: Restart with: cd dashboard && pnpm dev --port 3000 --hostname 127.0.0.1")

    if not ports_ok:
        issues.append("❌ Port 3000 not listening")
        print("CRITICAL: Port 3000 is not bound!")
        print("SOLUTION: Check Next.js startup errors")

    working_connections = [k for k, v in connections.items() if v]
    failed_connections = [k for k, v in connections.items() if not v]

    if working_connections:
        print(f"✅ Working: {', '.join(working_connections)}")

    if failed_connections:
        print(f"❌ Failed: {', '.join(failed_connections)}")
        issues.append(f"Connection failures: {failed_connections}")

    # API server status
    api_working = any("3002" in k and v for k, v in connections.items())
    frontend_working = any("3000" in k and v for k, v in connections.items())

    print(f"\n📊 STATUS SUMMARY:")
    print(f"   API Server (3002): {'✅' if api_working else '❌'}")
    print(f"   Frontend (3000): {'✅' if frontend_working else '❌'}")

    if api_working and not frontend_working:
        print("\n🎯 RECOMMENDATION: Use HTML Dashboard Workaround")
        print("   Since API works but Next.js doesn't, create:")
        print("   dashboard/public/index.html")
        print("   This will work immediately!")

    elif not api_working and not frontend_working:
        print("\n🎯 RECOMMENDATION: Restart Both Servers")
        print("   1. cd dashboard")
        print("   2. node api-server.js (in one terminal)")
        print("   3. pnpm dev --port 3000 --hostname 127.0.0.1 (in another)")

    elif frontend_working:
        print("\n🎯 SUCCESS: Dashboard is working!")
        print("   Access: http://localhost:3000")

    return issues

def main():
    print("🚨 CONSTITUTIONAL AI REALITY CHECK")
    print("Principle: Satya (Truth)")
    print("Testing IDE claims vs actual reality...")
    print()

    # Run all checks
    processes_ok = check_processes()
    ports_ok = check_ports()
    connections = test_connections()

    # Analyze and report
    issues = analyze_findings(processes_ok, ports_ok, connections)

    print("\n" + "=" * 50)
    if issues:
        print("❌ ISSUES FOUND - IDE CLAIMS WERE INCORRECT")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("✅ NO ISSUES - IDE CLAIMS WERE ACCURATE")

    print("\nRemember: Always test claims, never trust unverified AI output!")
    print("=" * 50)

if __name__ == "__main__":
    main()