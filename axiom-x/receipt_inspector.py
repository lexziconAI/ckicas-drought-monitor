"""
Inspect receipt structure to understand why matching failed
"""

import json
from pathlib import Path

print("🔍 RECEIPT STRUCTURE INSPECTOR")
print("=" * 60)

axiom_dir = Path("C:/Users/regan/ID SYSTEM/axiom-x")

# Find receipt files
receipts_found = []
for json_file in axiom_dir.rglob("*.json"):
    if '__pycache__' in str(json_file):
        continue

    try:
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Check if it looks like a receipt
        if any(key in data for key in [
            'performance', 'ops_per_second', 'timestamp',
            'constitutional_score', 'breakthrough'
        ]):
            receipts_found.append({
                'path': str(json_file),
                'name': json_file.name,
                'data': data
            })
    except:
        pass

print(f"Found {len(receipts_found)} receipt files\n")

# Show structure of first 5 receipts
print("📋 SAMPLE RECEIPT STRUCTURES:\n")

for i, receipt in enumerate(receipts_found[:5], 1):
    print(f"Receipt {i}: {receipt['name']}")
    print("-" * 60)

    data = receipt['data']

    # Show top-level keys
    print(f"Top-level keys: {list(data.keys())}")

    # Show file reference (if any)
    file_refs = []
    for key in ['file', 'target', 'script', 'module', 'capability', 'target_file']:
        if key in data:
            file_refs.append(f"{key}: {data[key]}")

    if file_refs:
        print(f"File references: {', '.join(file_refs)}")
    else:
        print("File references: NONE FOUND ❌")

    # Show performance data (if any)
    perf_data = []
    if 'ops_per_second' in data:
        perf_data.append(f"ops_per_second: {data['ops_per_second']}")
    if 'performance' in data:
        if isinstance(data['performance'], dict):
            perf_data.append(f"performance: {data['performance']}")
        elif isinstance(data['performance'], list):
            perf_data.append(f"performance: [list with {len(data['performance'])} items]")
        else:
            perf_data.append(f"performance: {type(data['performance']).__name__}")
    if 'breakthrough' in data:
        perf_data.append(f"breakthrough: {data['breakthrough']}")

    if perf_data:
        print(f"Performance: {', '.join(perf_data)}")
    else:
        print("Performance: NONE FOUND ❌")

    print()

# Look for breakthrough mentions
print("\n🌟 BREAKTHROUGH INDICATORS:")
breakthrough_receipts = []
for receipt in receipts_found:
    data = receipt['data']

    # Debug: Check data type
    if not isinstance(data, dict):
        print(f"⚠️  Receipt {receipt['name']} has non-dict data: {type(data)}")
        continue

    # Check various locations for breakthrough
    has_breakthrough = False
    breakthrough_value = None

    if 'breakthrough' in data:
        has_breakthrough = True
        breakthrough_value = data['breakthrough']
    elif 'performance' in data:
        perf_obj = data['performance']
        if isinstance(perf_obj, dict):
            if 'breakthrough' in perf_obj:
                has_breakthrough = True
                breakthrough_value = perf_obj['breakthrough']
        elif isinstance(perf_obj, list):
            # Check if any item in the performance list has breakthrough
            for item in perf_obj:
                if isinstance(item, dict) and 'breakthrough' in item:
                    has_breakthrough = True
                    breakthrough_value = item['breakthrough']
                    break
        else:
            # Handle other types (string, number, etc.)
            pass

    if has_breakthrough and breakthrough_value:
        breakthrough_receipts.append({
            'name': receipt['name'],
            'breakthrough': breakthrough_value,
            'full_path': receipt['path']
        })

if breakthrough_receipts:
    print(f"Found {len(breakthrough_receipts)} receipts with breakthrough=true:")
    for br in breakthrough_receipts[:5]:
        print(f"  • {br['name']}")
        print(f"    Path: {br['full_path']}")
else:
    print("❌ No receipts found with breakthrough=true")
    print("   This might mean:")
    print("   1. Breakthroughs stored differently in receipts")
    print("   2. Receipt files don't contain this field")
    print("   3. Looking in wrong directory for receipts")

print("\n" + "=" * 60)