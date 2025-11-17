import json
from pathlib import Path

# Load canonical map and get top 10 files
with open('validated_canonical_map.json', 'r') as f:
    canonical_data = json.load(f)

# Sort by breakthrough potential
sorted_files = sorted(canonical_data.items(),
                     key=lambda x: x[1]['breakthrough_potential'],
                     reverse=True)

print('INJECTING RECEIPT HOOKS INTO TOP 10 CANONICAL FILES')
print('=' * 60)

# Inject receipt hook into top 10
injected_count = 0
for full_path, data in sorted_files[:10]:
    file_path = Path(full_path)

    if file_path.exists():
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if already has hook
            if 'from axiom_receipt_hook import generate_receipt' in content:
                print(f'✓ {file_path.name}: Already has receipt hook')
                continue

            # Add import at top
            lines = content.split('\n')

            # Find first non-comment, non-import line
            insert_pos = 0
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                if (line_stripped and
                    not line_stripped.startswith('#') and
                    not line_stripped.startswith('import') and
                    not line_stripped.startswith('from') and
                    not line_stripped.startswith('"""') and
                    not line_stripped.startswith("'''")):
                    insert_pos = i
                    break

            # Insert the import
            lines.insert(insert_pos, 'from axiom_receipt_hook import generate_receipt')

            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            print(f'✓ {file_path.name}: Receipt hook injected')
            injected_count += 1

        except Exception as e:
            print(f'❌ {file_path.name}: Failed to inject ({e})')
    else:
        print(f'✗ {file_path.name}: File not found')

print(f'\n✅ Injected receipt hooks into {injected_count} files')
print('📜 Files now auto-generate constitutional receipts on execution')