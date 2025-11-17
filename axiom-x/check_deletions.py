from pathlib import Path
from collections import defaultdict

# Load canonical map
import json
with open('validated_canonical_map.json', 'r') as f:
    canonical_data = json.load(f)

canonical_files = set()
for full_path in canonical_data.keys():
    filename = Path(full_path).name
    canonical_files.add(filename)

print('CHECKING FOR VERSIONED DUPLICATES')
print('=' * 50)

# Load all Python files
axiom_dir = Path('C:/Users/regan/ID SYSTEM/axiom-x')
all_py_files = list(axiom_dir.rglob('*.py'))
all_py_files = [f for f in all_py_files if '__pycache__' not in str(f)]

# Look for files with version patterns
versioned_files = []
patterns = ['_v1', '_v2', '_v3', '_v4', '_v5',
           '_draft', '_old', '_legacy', '_backup', '_copy']

for py_file in all_py_files:
    for pattern in patterns:
        if pattern in py_file.stem:
            versioned_files.append(py_file)
            break

print(f'Files with version patterns: {len(versioned_files)}')

# Group by base name
file_groups = defaultdict(list)
for py_file in versioned_files:
    base = py_file.stem
    for pattern in patterns:
        if pattern in base:
            base = base.split(pattern)[0]
            break

    file_groups[base].append(py_file)

print(f'Unique base names with versions: {len(file_groups)}')

# Check which have canonical versions
deletion_candidates = []
for base, files in file_groups.items():
    # Look for canonical version (without version suffix)
    canonical_name = f'{base}.py'
    if canonical_name in canonical_files:
        # Mark versioned files for deletion
        for f in files:
            deletion_candidates.append({
                'file': str(f),
                'name': f.name,
                'canonical_alternative': canonical_name
            })

print(f'Potential deletions: {len(deletion_candidates)}')

if deletion_candidates:
    print('\nSAMPLE DELETION CANDIDATES:')
    for i, candidate in enumerate(deletion_candidates[:10]):
        print(f'{i+1}. {candidate["name"]} -> keep {candidate["canonical_alternative"]}')

    total_space = sum(Path(c['file']).stat().st_size for c in deletion_candidates) / (1024**2)
    print(f'\nTotal space savings: {total_space:.1f} MB')
else:
    print('\nNo versioned duplicate files found to delete!')