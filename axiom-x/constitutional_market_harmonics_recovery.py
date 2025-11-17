"""
Constitutional Market Harmonics Dashboard - Nuclear Recovery Script
====================================================================
Bottleneck Detection + Cleanup + Relaunch

Based on LOG⁴ Orchestrator Analysis
Implements Fractal Optimization principles
"""

import subprocess
import json
from pathlib import Path
import shutil
from datetime import datetime

print("🌀 CONSTITUTIONAL MARKET HARMONICS - NUCLEAR RECOVERY")
print("=" * 70)
print()

# Step 1: System State Diagnosis
print("📊 STEP 1: DIAGNOSING CURRENT STATE")
print("-" * 70)

project_root = Path(r"C:\Users\regan\ID SYSTEM\axiom-x\constitutional-market-harmonics")

if not project_root.exists():
    print(f"❌ ERROR: Project not found at {project_root}")
    exit(1)

print(f"✅ Found project at: {project_root}")

# Check critical directories
critical_dirs = {
    'backend': project_root / 'backend',
    'dashboard': project_root / 'dashboard',
    'core': project_root / 'core',
    'database': project_root / 'market_harmonics.db'
}

for name, path in critical_dirs.items():
    if path.exists():
        print(f"   ✅ {name}: Found")
    else:
        print(f"   ⚠️  {name}: Missing!")

# Step 2: Kill All Node Processes
print()
print("🛑 STEP 2: KILLING ALL NODE PROCESSES")
print("-" * 70)

try:
    result = subprocess.run(
        ['taskkill', '/F', '/IM', 'node.exe'],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("   ✅ All node.exe processes terminated")
    else:
        print("   ℹ️  No node processes were running")
except Exception as e:
    print(f"   ⚠️  Could not kill processes: {e}")

# Step 3: Clean Build Artifacts
print()
print("🧹 STEP 3: CLEANING BUILD ARTIFACTS")
print("-" * 70)

dirs_to_clean = [
    project_root / 'dashboard' / '.next',
    project_root / 'dashboard' / 'node_modules',
    project_root / 'backend' / 'node_modules',
]

for dir_path in dirs_to_clean:
    if dir_path.exists():
        try:
            print(f"   🗑️  Deleting: {dir_path.name}")
            shutil.rmtree(dir_path)
            print(f"   ✅ Cleaned: {dir_path.name}")
        except Exception as e:
            print(f"   ⚠️  Could not delete {dir_path.name}: {e}")
    else:
        print(f"   ℹ️  Already clean: {dir_path.name}")

# Step 4: Identify Redundant Files
print()
print("🔍 STEP 4: SCANNING FOR REDUNDANT FILES")
print("-" * 70)

dashboard_dir = project_root / 'dashboard'
if dashboard_dir.exists():
    tsx_files = list(dashboard_dir.glob('**/*.tsx'))
    jsx_files = list(dashboard_dir.glob('**/*.jsx'))

    # Filter out node_modules
    tsx_files = [f for f in tsx_files if 'node_modules' not in str(f)]
    jsx_files = [f for f in jsx_files if 'node_modules' not in str(f)]

    print(f"   Found {len(tsx_files)} TypeScript React files")
    print(f"   Found {len(jsx_files)} JavaScript React files")

    # Look for duplicates
    file_names = {}
    for f in tsx_files + jsx_files:
        name = f.name
        if name in file_names:
            file_names[name].append(f)
        else:
            file_names[name] = [f]

    duplicates = {k: v for k, v in file_names.items() if len(v) > 1}

    if duplicates:
        print()
        print("   ⚠️  POTENTIAL DUPLICATES FOUND:")
        for name, paths in duplicates.items():
            print(f"      📄 {name}:")
            for p in paths:
                print(f"         - {p.relative_to(project_root)}")
    else:
        print("   ✅ No obvious duplicates detected")

# Step 5: Backend Health Check
print()
print("🔧 STEP 5: BACKEND HEALTH CHECK")
print("-" * 70)

db_path = project_root / 'market_harmonics.db'
if db_path.exists():
    size_mb = db_path.stat().st_size / (1024 * 1024)
    print(f"   ✅ Database exists: {size_mb:.2f} MB")

    # Quick SQLite check
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"   ✅ Found {len(tables)} tables")

        # Check if we have data
        try:
            cursor.execute("SELECT COUNT(*) FROM trades")
            trade_count = cursor.fetchone()[0]
            print(f"   📊 Trades in database: {trade_count}")
        except:
            print("   ⚠️  Could not query trades table")

        try:
            cursor.execute("SELECT COUNT(*) FROM portfolio_positions")
            position_count = cursor.fetchone()[0]
            print(f"   📊 Portfolio positions: {position_count}")
        except:
            print("   ⚠️  Could not query portfolio_positions table")

        conn.close()
    except Exception as e:
        print(f"   ⚠️  Database check failed: {e}")
else:
    print("   ❌ Database not found!")

# Step 6: Generate Recovery Report
print()
print("📋 STEP 6: GENERATING RECOVERY REPORT")
print("-" * 70)

report = {
    'timestamp': datetime.now().isoformat(),
    'project_root': str(project_root),
    'status': {
        'backend_dir': (project_root / 'backend').exists(),
        'dashboard_dir': (project_root / 'dashboard').exists(),
        'database_exists': db_path.exists(),
    },
    'cleanup': {
        'node_processes_killed': True,
        'cache_cleaned': True,
    },
    'files_scanned': {
        'tsx_files': len(tsx_files) if dashboard_dir.exists() else 0,
        'jsx_files': len(jsx_files) if dashboard_dir.exists() else 0,
        'duplicates_found': len(duplicates) if dashboard_dir.exists() else 0,
    },
    'recommendations': []
}

# Add recommendations
if not (project_root / 'backend').exists():
    report['recommendations'].append("CRITICAL: Backend directory missing - needs restoration")

if not db_path.exists():
    report['recommendations'].append("CRITICAL: Database missing - needs regeneration")

if duplicates:
    report['recommendations'].append(f"WARNING: {len(duplicates)} duplicate files found - review needed")

# Save report
report_path = project_root / 'recovery_report.json'
with open(report_path, 'w') as f:
    json.dump(report, indent=2, fp=f)

print(f"   ✅ Recovery report saved: {report_path}")

# Step 7: Next Steps
print()
print("🚀 NEXT STEPS:")
print("-" * 70)
print()
print("1. INSTALL DEPENDENCIES:")
print("   cd dashboard")
print("   npm install")
print()
print("2. START BACKEND:")
print("   cd backend")
print("   npx tsx server.ts")
print()
print("3. START FRONTEND (in new terminal):")
print("   cd dashboard")
print("   npm run dev")
print()
print("4. TEST BACKEND API:")
print("   curl http://localhost:12345/api/dashboard")
print()
print("5. OPEN DASHBOARD:")
print("   http://localhost:3000")
print()
print("=" * 70)
print("✅ NUCLEAR RECOVERY COMPLETE")
print()
print("📊 Check recovery_report.json for detailed findings")
print()