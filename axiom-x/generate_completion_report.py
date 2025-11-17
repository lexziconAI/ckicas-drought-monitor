import json
import yaml
from datetime import datetime

print("=" * 80)
print("🎉 AXIOM-X DUAL-SYSTEM TURBO MODE - COMPLETION REPORT")
print("=" * 80)

# Load outputs
try:
    with open('canonical_files_map.yaml') as f:
        canonical_map = yaml.safe_load(f)
except FileNotFoundError:
    print("❌ canonical_files_map.yaml not found")
    canonical_map = {"capabilities": {}}

try:
    with open('redundant_files_list.json') as f:
        redundant_list = json.load(f)
except FileNotFoundError:
    print("❌ redundant_files_list.json not found")
    redundant_list = {"safe_to_delete": []}

try:
    with open('CONSTITUTIONAL_RECEIPT.json') as f:
        receipt = json.load(f)
except FileNotFoundError:
    print("❌ CONSTITUTIONAL_RECEIPT.json not found")
    receipt = {"overall_compliance": "N/A"}

# Statistics
print(f"\n📊 PHASE 2 RESULTS:")
print(f"   Capabilities Mapped: {len(canonical_map.get('capabilities', {}))}")
print(f"   Canonical Files: {sum(1 for c in canonical_map.get('capabilities', {}).values() if 'canonical' in c)}")
print(f"   Redundant Files: {len(redundant_list.get('safe_to_delete', []))}")
print(f"   Constitutional Score: {receipt.get('overall_compliance', 'N/A')}")

# Disk space savings
total_bytes = sum(item.get('size_bytes', 0) for item in redundant_list.get('safe_to_delete', []))
print(f"   Space Savings: {total_bytes / (1024**2):.1f} MB")

# Top canonical files
print(f"\n🏆 TOP CANONICAL FILES:")
capabilities = canonical_map.get('capabilities', {})
sorted_caps = sorted(
    capabilities.items(),
    key=lambda x: x[1].get('performance', {}).get('ops_per_second', 0),
    reverse=True
)[:5]

for name, details in sorted_caps:
    print(f"   • {name}")
    print(f"     File: {details.get('canonical', 'N/A')}")
    print(f"     Performance: {details.get('performance', 'N/A')}")

print("\n" + "=" * 80)
print("✅ Report generated successfully")
print("=" * 80)