"""
Constitutional deletion manager with human approval
YAMA PRINCIPLE: Ahimsa (Non-harm) - No deletion without explicit consent
"""

import json
import yaml
from pathlib import Path
import shutil
from datetime import datetime

print("🗑️  CONSTITUTIONAL DELETION MANAGER")
print("=" * 60)
print("⚠️  AHIMSA PRINCIPLE: No deletion without your approval\n")

# Load canonical map
with open('validated_canonical_map.json', 'r') as f:
    canonical_data = json.load(f)

# Get canonical file names (not full paths)
canonical_files = set()
for full_path in canonical_data.keys():
    filename = Path(full_path).name
    canonical_files.add(filename)

# Load all Python files
axiom_dir = Path("C:/Users/regan/ID SYSTEM/axiom-x")
all_py_files = list(axiom_dir.rglob("*.py"))

# Build deletion plan
deletion_candidates = []

# Group files by base name
from collections import defaultdict
file_groups = defaultdict(list)

for py_file in all_py_files:
    if '__pycache__' in str(py_file):
        continue

    # Extract base name
    base = py_file.stem
    for pattern in ['_v1', '_v2', '_v3', '_v4', '_v5',
                    '_draft', '_old', '_legacy', '_backup', '_copy']:
        if pattern in base:
            base = base.split(pattern)[0]
            break

    file_groups[base].append(py_file)

# Find duplicates where canonical version exists
for base, files in file_groups.items():
    if len(files) > 1:
        # Check if any is canonical
        canonical_versions = [f for f in files if f.name in canonical_files]

        if canonical_versions:
            # Mark others as redundant
            canonical = canonical_versions[0]
            for f in files:
                if f != canonical:
                    deletion_candidates.append({
                        'file': str(f),
                        'name': f.name,
                        'size_mb': f.stat().st_size / (1024**2),
                        'canonical_alternative': canonical.name,
                        'reason': 'Superseded by performance-validated version'
                    })

print(f"📊 DELETION ANALYSIS:")
print(f"   Total files: {len(all_py_files)}")
print(f"   Canonical files: {len(canonical_files)}")
print(f"   Deletion candidates: {len(deletion_candidates)}")
print(f"   Space savings: {sum(d['size_mb'] for d in deletion_candidates):.1f} MB\n")

# Show top 20 candidates
print("🔍 TOP 20 DELETION CANDIDATES:")
print("-" * 60)
for i, candidate in enumerate(deletion_candidates[:20], 1):
    print(f"{i}. {candidate['name']} ({candidate['size_mb']:.2f} MB)")
    print(f"   → Keep instead: {candidate['canonical_alternative']}")
    print(f"   Reason: {candidate['reason']}\n")

# HUMAN APPROVAL GATE
print("=" * 60)
print("⚠️  CONSTITUTIONAL APPROVAL REQUIRED")
print("=" * 60)
response = input(f"\nReview complete. Delete {len(deletion_candidates)} redundant files? (yes/no): ")

if response.lower() != 'yes':
    print("\n❌ Deletion cancelled. No files modified.")
    print("💾 Deletion plan saved to: deletion_plan.json")
    with open('deletion_plan.json', 'w') as f:
        json.dump(deletion_candidates, f, indent=2)
    exit()

# Create backup directory
backup_dir = axiom_dir / "DELETED_FILES_BACKUP" / datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir.mkdir(parents=True, exist_ok=True)

print(f"\n📦 Creating backup at: {backup_dir}")

# Execute deletion with backup
deleted_count = 0
for candidate in deletion_candidates:
    try:
        file_path = Path(candidate['file'])

        # Backup first
        backup_path = backup_dir / file_path.name
        shutil.copy2(file_path, backup_path)

        # Delete original
        file_path.unlink()

        deleted_count += 1
        print(f"✅ Deleted: {file_path.name}")

    except Exception as e:
        print(f"❌ Failed to delete {file_path.name}: {e}")

print(f"\n" + "=" * 60)
print(f"✅ DELETION COMPLETE")
print(f"=" * 60)
print(f"   Deleted: {deleted_count}/{len(deletion_candidates)} files")
print(f"   Backup: {backup_dir}")
print(f"   Space freed: {sum(d['size_mb'] for d in deletion_candidates[:deleted_count]):.1f} MB")

# Create constitutional receipt
receipt = {
    'action': 'canonical_optimization_deletion',
    'timestamp': datetime.now().isoformat(),
    'yama_compliance': {
        'ahimsa': f'Human approval obtained, {deleted_count} files backed up',
        'satya': 'Deletion based on validated performance data',
        'asteya': 'Canonical files preserved and attributed',
        'brahmacharya': 'Efficient cleanup of redundant resources',
        'aparigraha': 'Letting go of outdated implementations'
    },
    'statistics': {
        'files_deleted': deleted_count,
        'space_freed_mb': sum(d['size_mb'] for d in deletion_candidates[:deleted_count]),
        'backup_location': str(backup_dir)
    },
    'constitutional_score': 1.0
}

with open('deletion_constitutional_receipt.json', 'w') as f:
    json.dump(receipt, f, indent=2)

print(f"\n📜 Constitutional receipt: deletion_constitutional_receipt.json")
print("\n🎉 Axiom-X brain optimized! Canonical files active.")