# simple_bottleneck_detector.py
"""
Simple sequential bottleneck detection - for testing
NO parallelization - just straightforward loop
"""

import json
from pathlib import Path
import difflib

print("🔍 SIMPLE SEQUENTIAL BOTTLENECK DETECTION")
print("=" * 60)

# Load canonical files
print("🔧 Loading canonical files...")
with open('validated_canonical_map.json', 'r') as f:
    canonical_map = json.load(f)

canonical_files = set(Path(k).name for k in canonical_map.keys())
print(f"✅ Canonical files loaded: {len(canonical_files)}")

# Find Python files in key directories
axiom_dir = Path(r"C:\Users\regan\ID SYSTEM\axiom-x")
target_dirs = ['core', 'infrastructure', 'ops', 'apps', 'agents']

all_python_files = []
for target_dir in target_dirs:
    dir_path = axiom_dir / target_dir
    if dir_path.exists():
        all_python_files.extend(dir_path.rglob("*.py"))

print(f"📁 Total Python files: {len(all_python_files)}")

# Filter to non-canonical
non_canonical = [f for f in all_python_files if f.name not in canonical_files]
print(f"🔍 Non-canonical to analyze: {len(non_canonical)}")

# Build canonical paths
canonical_paths = {}
for cf in canonical_files:
    matches = list(axiom_dir.rglob(cf))
    if matches:
        canonical_paths[cf] = matches[0]

print(f"\n🔄 Processing sequentially (no parallelization)...")
print("This helps us identify any problematic files\n")

redundant_candidates = []

for i, nc_file in enumerate(non_canonical, 1):
    print(f"[{i}/{len(non_canonical)}] Analyzing: {nc_file.name}...", end=' ')

    try:
        # Check file size first
        file_size = nc_file.stat().st_size
        if file_size > 1_000_000:  # 1MB
            print(f"⚠️ LARGE FILE ({file_size:,} bytes) - skipping")
            continue

        # Read file
        with open(nc_file, 'r', encoding='utf-8') as f:
            nc_content = f.read()

        best_match = None
        best_similarity = 0

        # Compare against each canonical
        for canon_name, canon_path in canonical_paths.items():
            try:
                with open(canon_path, 'r', encoding='utf-8') as f:
                    canon_content = f.read()

                similarity = difflib.SequenceMatcher(
                    None, nc_content, canon_content
                ).ratio()

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = canon_name
            except Exception as e:
                print(f"Error comparing with {canon_name}: {e}")
                continue

        if best_similarity > 0.7:
            print(f"✅ {best_similarity:.1%} similar to {best_match}")
            redundant_candidates.append({
                'non_canonical_file': str(nc_file),
                'canonical_match': best_match,
                'similarity_score': best_similarity,
                'severity': 'HIGH' if best_similarity > 0.9 else 'MEDIUM',
                'safe_to_delete': best_similarity > 0.95
            })
        else:
            print(f"✓ Unique ({best_similarity:.1%} max similarity)")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        continue

print(f"\n✅ Analysis complete!")
print(f"🎯 Found {len(redundant_candidates)} redundant files")

# Save results
output = {
    'total_analyzed': len(all_python_files),
    'canonical_files': len(canonical_files),
    'non_canonical': len(non_canonical),
    'redundant_candidates': redundant_candidates
}

with open('simple_bottleneck_analysis.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n💾 Saved: simple_bottleneck_analysis.json")

if redundant_candidates:
    print(f"\n🔥 REDUNDANT FILES FOUND:")
    for r in redundant_candidates:
        print(f"\n{Path(r['non_canonical_file']).name}")
        print(f"   Match: {r['canonical_match']}")
        print(f"   Similarity: {r['similarity_score']:.1%}")
else:
    print("\n✅ No redundant files found!")