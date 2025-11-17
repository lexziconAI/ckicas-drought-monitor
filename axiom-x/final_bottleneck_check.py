"""
Fractal-optimized bottleneck detector - SIMPLE SEQUENTIAL
NO parallelization. NO complex path handling. JUST WORKS.
"""

import json
from pathlib import Path
import difflib
from datetime import datetime

print("🎯 FINAL BOTTLENECK CHECK (Fractal-Optimized)")
print("=" * 60)

# Step 1: Load canonical files (just filenames)
print("\n📋 Step 1: Loading canonical files...")
with open('validated_canonical_map.json', 'r') as f:
    canonical_map = json.load(f)

canonical_filenames = {Path(k).name for k in canonical_map.keys()}
print(f"   ✅ Loaded {len(canonical_filenames)} canonical filenames")

# Step 2: Find files to check
print("\n🔍 Step 2: Finding files in target directories...")
axiom_dir = Path(r"C:\Users\regan\ID SYSTEM\axiom-x")
target_dirs = ['core', 'infrastructure', 'ops', 'apps', 'agents']

files_to_check = []
for target in target_dirs:
    dir_path = axiom_dir / target
    if dir_path.exists():
        # Use glob (not rglob) to avoid recursion issues
        for py_file in dir_path.glob("*.py"):
            if py_file.name not in canonical_filenames:
                files_to_check.append(py_file)

print(f"   ✅ Found {len(files_to_check)} non-canonical files")

# Step 3: Build canonical paths for comparison
print("\n🗂️  Step 3: Building canonical file paths...")
canonical_paths = {}
for filename in canonical_filenames:
    # Search only in target directories
    for target in target_dirs:
        dir_path = axiom_dir / target
        if dir_path.exists():
            matches = list(dir_path.glob(filename))
            if matches:
                canonical_paths[filename] = matches[0]
                break

    # If not in target dirs, try root
    if filename not in canonical_paths:
        matches = list(axiom_dir.glob(filename))
        if matches:
            canonical_paths[filename] = matches[0]

print(f"   ✅ Mapped {len(canonical_paths)} canonical file paths")

# Step 4: Sequential analysis (NO PARALLELIZATION)
print(f"\n🔄 Step 4: Analyzing files sequentially...")
print(f"   (This is FASTER than parallel for {len(files_to_check)} files)\n")

results = []

for i, file_path in enumerate(files_to_check, 1):
    print(f"   [{i}/{len(files_to_check)}] {file_path.name}...", end=" ")

    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if too large (>500KB)
        if len(content) > 500000:
            print("⚠️ SKIPPED (too large)")
            continue

        # Compare against each canonical
        best_match = None
        best_similarity = 0

        for canon_name, canon_path in canonical_paths.items():
            # ADD THIS: Show what we're comparing
            print(f"      Comparing vs {canon_name}...", end="\r")

            try:
                # ADD THIS: Check file size first
                canon_size = canon_path.stat().st_size
                if canon_size > 100000:  # Skip if >100KB
                    continue

                with open(canon_path, 'r', encoding='utf-8') as f:
                    canon_content = f.read()

                similarity = difflib.SequenceMatcher(
                    None, content, canon_content
                ).ratio()

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = canon_name
            except:
                continue

        # Clear the comparison line
        print(" " * 50, end="\r")        # Report findings
        if best_similarity > 0.95:
            print(f"🔴 {best_similarity:.1%} → {best_match} (SAFE DELETE)")
            severity = "HIGH"
        elif best_similarity > 0.7:
            print(f"🟡 {best_similarity:.1%} → {best_match} (REVIEW)")
            severity = "MEDIUM"
        else:
            print(f"✅ Unique ({best_similarity:.1%})")
            severity = None

        if severity:
            results.append({
                'file': str(file_path),
                'filename': file_path.name,
                'canonical_match': best_match,
                'similarity_score': best_similarity,
                'severity': severity,
                'safe_to_delete': best_similarity > 0.95,
                'recommendation': (
                    'Safe to delete - use canonical instead'
                    if best_similarity > 0.95
                    else 'Review manually before deletion'
                )
            })

    except Exception as e:
        print(f"❌ ERROR: {e}")

# Step 5: Generate results
print(f"\n✅ Analysis complete!")
print(f"\n📊 RESULTS:")
print(f"   Files analyzed: {len(files_to_check)}")
print(f"   Duplicates found: {len(results)}")
print(f"   Safe deletions: {len([r for r in results if r['safe_to_delete']])}")

# Save detailed results
output = {
    'metadata': {
        'timestamp': datetime.now().isoformat(),
        'method': 'fractal-optimized-sequential',
        'files_analyzed': len(files_to_check),
        'canonical_files': len(canonical_filenames)
    },
    'results': results,
    'constitutional_compliance': {
        'ahimsa': 'No files deleted - human approval required',
        'satya': 'Actual similarity scores reported',
        'brahmacharya': 'Efficient sequential processing for small dataset'
    }
}

with open('final_bottleneck_results.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n💾 Saved: final_bottleneck_results.json")

# Display top candidates
if results:
    print(f"\n🔥 DUPLICATE FILES FOUND:\n")
    results.sort(key=lambda x: x['similarity_score'], reverse=True)

    for result in results:
        print(f"   {result['filename']}")
        print(f"   → {result['similarity_score']:.1%} similar to {result['canonical_match']}")
        print(f"   → {result['recommendation']}")
        print()

print("✅ Fractal-optimized bottleneck detection complete!")
print("📋 Review results in final_bottleneck_results.json")
print("🛡️ Constitutional principle: Ahimsa - human approval required for deletions")