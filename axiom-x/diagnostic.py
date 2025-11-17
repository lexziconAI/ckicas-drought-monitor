import yaml
import json

print('=' * 60)
print('DIAGNOSTIC: What is in each file?')
print('=' * 60)

# Check execution-validated map (should be ~30)
print('\n1️⃣ execution_validated_canonical_map.yaml:')
try:
    with open('execution_validated_canonical_map.yaml', 'r') as f:
        data = yaml.safe_load(f)
        perf = data.get('file_performance', {})
        print(f'   Entries: {len(perf)}')
        print(f'   First 3: {list(perf.keys())[:3]}')
except Exception as e:
    print(f'   Error: {e}')

# Check canonical files map (might be huge)
print('\n2️⃣ canonical_files_map.yaml:')
try:
    with open('canonical_files_map.yaml', 'r') as f:
        data = yaml.safe_load(f)
        if isinstance(data, dict):
            print(f'   Keys: {list(data.keys())}')
            for key, value in data.items():
                if isinstance(value, dict):
                    print(f'   {key}: {len(value)} entries')
        else:
            print(f'   Type: {type(data)}')
except Exception as e:
    print(f'   Error: {e}')

# Check validated map (for comparison)
print('\n3️⃣ validated_canonical_map.json:')
try:
    with open('validated_canonical_map.json', 'r') as f:
        data = json.load(f)
        print(f'   Entries: {len(data)}')
        print(f'   First 3: {list(data.keys())[:3]}')
except Exception as e:
    print(f'   Error: {e}')

# Check master brain (if it exists)
print('\n4️⃣ axiom_x_master_brain.yaml:')
try:
    with open('axiom_x_master_brain.yaml', 'r') as f:
        data = yaml.safe_load(f)
        print(f'   Top-level keys: {list(data.keys())}')
        if 'canonical_files' in data:
            canonical_files = data['canonical_files']
            print(f'   Canonical files count: {canonical_files.get("total", "unknown")}')
except Exception as e:
    print(f'   Error: {e}')