# diagnostic_canonical_paths.py
"""Quick check - why is canonical path building hanging?"""

import json
from pathlib import Path
import time

print("🔍 DIAGNOSTIC: Why is canonical_paths building slow?")
print("=" * 60)

# Load canonical files
with open('validated_canonical_map.json', 'r') as f:
    canonical_map = json.load(f)

canonical_files = list(canonical_map.keys())[:5]  # Just test first 5
print(f"Testing with first 5 canonical files...")

axiom_dir = Path(r"C:\Users\regan\ID SYSTEM\axiom-x")

for cf in canonical_files:
    print(f"\nSearching for: {cf}")
    print(f"  Type: {type(cf)}")
    print(f"  Length: {len(cf)}")

    start = time.time()

    # This is what's probably hanging
    try:
        matches = list(axiom_dir.rglob(cf))
        elapsed = time.time() - start

        print(f"  ✅ Found {len(matches)} matches in {elapsed:.2f}s")
        if matches:
            print(f"     First match: {matches[0]}")
    except Exception as e:
        elapsed = time.time() - start
        print(f"  ❌ ERROR after {elapsed:.2f}s: {e}")

    if elapsed > 5:
        print(f"  ⚠️ THIS ONE IS SLOW! Might be the problem!")
        break

print("\n💡 If any file took >5 seconds, that's the bottleneck!")