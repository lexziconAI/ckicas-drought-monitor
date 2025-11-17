import yaml
import json
import difflib
from pathlib import Path

print("🔍 RECURSIVE BOTTLENECK DETECTION")
print("=" * 60)

# Load canonical truth
with open('canonical_files_map.yaml', 'r', encoding='utf-8') as f:
    canonical_map = yaml.safe_load(f)

canonical_files = {}
for capability, data in canonical_map.get('capabilities', {}).items():
    canonical_files[data['canonical_file']] = {
        'path': data['canonical_path'],
        'capability': capability
    }

print(f"Canonical files loaded: {len(canonical_files)}")

# Scan entire Axiom-X directory (excluding venv)
axiom_dir = Path(r"C:\Users\regan\ID SYSTEM\axiom-x")
all_python_files = []

# Recursively find all Python files, excluding venv
for py_file in axiom_dir.rglob("*.py"):
    if '.venv' not in str(py_file):
        all_python_files.append(py_file)

print(f"Total Python files found: {len(all_python_files)}")

# Get canonical file names
canonical_names = set(canonical_files.keys())
non_canonical = [f for f in all_python_files if f.name not in canonical_names]

print(f"Non-canonical files: {len(non_canonical)}")

# Analyze for semantic similarity
redundant_candidates = []

# Process in batches to avoid memory issues
batch_size = 50
total_processed = 0

for i in range(0, len(non_canonical), batch_size):
    batch = non_canonical[i:i+batch_size]

    for nc_file in batch:
        try:
            # Read non-canonical file
            with open(nc_file, 'r', encoding='utf-8') as f:
                nc_content = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            continue

        # Compare against each canonical
        for canon_name, canon_data in canonical_files.items():
            try:
                # Read canonical file
                canon_path = Path(canon_data['path'])
                if not canon_path.exists():
                    continue

                with open(canon_path, 'r', encoding='utf-8') as f:
                    canon_content = f.read()
            except (UnicodeDecodeError, FileNotFoundError):
                continue

            # Check similarity
            similarity = difflib.SequenceMatcher(None, nc_content, canon_content).ratio()

            # Only flag high similarity (>70%)
            if similarity > 0.7:
                redundant_candidates.append({
                    'non_canonical_file': str(nc_file),
                    'canonical_equivalent': canon_name,
                    'canonical_capability': canon_data['capability'],
                    'similarity_score': round(similarity, 3),
                    'severity': 'HIGH' if similarity > 0.9 else 'MEDIUM',
                    'safe_to_delete': similarity > 0.95,
                    'recommendation': 'Delete and use canonical' if similarity > 0.95 else 'Review manually',
                    'file_size_kb': round(nc_file.stat().st_size / 1024, 2)
                })

    total_processed += len(batch)
    print(f"Processed {total_processed}/{len(non_canonical)} files...")

# Sort by severity and similarity
redundant_candidates.sort(key=lambda x: (x['severity'], x['similarity_score']), reverse=True)

print(f"\n🎯 Found {len(redundant_candidates)} redundant files")

# Calculate space savings
safe_deletions = [c for c in redundant_candidates if c['safe_to_delete']]
total_space_mb = sum(c['file_size_kb'] for c in safe_deletions) / 1024

# Save results
analysis_result = {
    'metadata': {
        'generated': '2025-11-09',
        'total_files_scanned': len(all_python_files),
        'canonical_files': len(canonical_files),
        'non_canonical': len(non_canonical),
        'redundant_candidates': len(redundant_candidates),
        'high_severity': len([r for r in redundant_candidates if r['severity'] == 'HIGH']),
        'safe_deletions': len(safe_deletions),
        'potential_space_savings_mb': round(total_space_mb, 2)
    },
    'redundant_candidates': redundant_candidates
}

with open('redundant_files_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_result, f, indent=2)

print("💾 Saved: redundant_files_analysis.json")
print(f"📊 High severity redundancies: {len([r for r in redundant_candidates if r['severity'] == 'HIGH'])}")
print(f"🗑️ Safe deletions: {len(safe_deletions)}")
print(f"💾 Potential space savings: {total_space_mb:.1f} MB")