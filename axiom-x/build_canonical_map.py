import json
from pathlib import Path
from collections import defaultdict

print('BUILDING VALIDATED CANONICAL MAP')
print('=' * 50)

# Load correlations
with open('output_source_correlations.json', 'r') as f:
    correlations = json.load(f)

# Build canonical map with performance metrics
canonical_map = {}

for corr in correlations:
    python_file = corr['python_source']
    json_file = corr['json_output']
    confidence = corr['confidence']
    metrics = corr.get('metrics', {})

    # Extract key performance indicators
    performance_data = {
        'breakthrough_potential': 0.0,
        'constitutional_score': 0.0,
        'confidence': 0.0,
        'ops_per_second': 0,
        'speedup_factor': 1.0,
        'correlation_confidence': confidence,
        'source_json': json_file,
        'correlation_method': corr['method']
    }

    # Extract specific breakthrough values
    for metric, value in metrics.items():
        if isinstance(value, (int, float)):
            if abs(value - 25504) < 1:  # 25,504 ops/sec
                performance_data['ops_per_second'] = 25504
                performance_data['breakthrough_potential'] = max(performance_data['breakthrough_potential'], 1.0)
            elif abs(value - 11.4) < 0.1:  # 11.4x speedup
                performance_data['speedup_factor'] = 11.4
                performance_data['breakthrough_potential'] = max(performance_data['breakthrough_potential'], 0.9)
            elif abs(value - 10.0) < 0.1:  # 10.0 perfection score
                performance_data['breakthrough_potential'] = max(performance_data['breakthrough_potential'], 0.8)
            elif abs(value - 0.89) < 0.01:  # 0.89 constitutional score
                performance_data['constitutional_score'] = 0.89
                performance_data['breakthrough_potential'] = max(performance_data['breakthrough_potential'], 0.7)

    # Set confidence based on correlation level
    if confidence == 'high':
        performance_data['confidence'] = 0.9
    elif confidence == 'medium':
        performance_data['confidence'] = 0.7
    else:  # low
        performance_data['confidence'] = 0.5

    # Only include if we have some performance data
    if (performance_data['ops_per_second'] > 0 or
        performance_data['speedup_factor'] > 1.0 or
        performance_data['constitutional_score'] > 0 or
        performance_data['breakthrough_potential'] > 0):

        # If this Python file already has an entry, keep the better one
        if python_file in canonical_map:
            existing = canonical_map[python_file]
            # Prefer higher breakthrough potential, then higher confidence
            if (performance_data['breakthrough_potential'] > existing['breakthrough_potential'] or
                (performance_data['breakthrough_potential'] == existing['breakthrough_potential'] and
                 performance_data['confidence'] > existing['confidence'])):
                canonical_map[python_file] = performance_data
        else:
            canonical_map[python_file] = performance_data

# Sort by canonical selection criteria
sorted_files = sorted(canonical_map.items(),
                     key=lambda x: (x[1]['breakthrough_potential'],
                                   x[1]['constitutional_score'],
                                   x[1]['confidence'],
                                   x[1]['ops_per_second']),
                     reverse=True)

print(f'Total canonical files with performance data: {len(canonical_map)}')

# Show top canonical selections
print('\nTOP CANONICAL FILES BY PERFORMANCE:')
for i, (file_path, data) in enumerate(sorted_files[:20]):
    print(f'\n{i+1}. {Path(file_path).name}')
    print(f'   Breakthrough Potential: {data["breakthrough_potential"]:.1f}')
    print(f'   Constitutional Score: {data["constitutional_score"]:.2f}')
    print(f'   Ops/Sec: {data["ops_per_second"]:,}')
    print(f'   Speedup: {data["speedup_factor"]:.1f}x')
    print(f'   Confidence: {data["confidence"]:.1f}')
    print(f'   Source: {data["source_json"]}')

# Check for key files
key_files = [
    'fractal_optimization_orchestrator.py',
    'advanced_fractal_army_deployment.py',
    'advanced_fractal_worker_spawner.py',
    'advanced_coordination_orchestrator.py'
]

print(f'\nKEY CORE FILES STATUS:')
for key_file in key_files:
    found = any(key_file in fp for fp, _ in sorted_files)
    if found:
        entry = next((data for fp, data in sorted_files if key_file in fp), None)
        if entry:
            print(f'✓ {key_file}: Breakthrough {entry["breakthrough_potential"]:.1f}, Confidence {entry["confidence"]:.1f}')
    else:
        print(f'✗ {key_file}: Not found in canonical map')

# Save canonical map
with open('validated_canonical_map.json', 'w') as f:
    json.dump(canonical_map, f, indent=2)

print(f'\nCanonical map saved to validated_canonical_map.json')
print('=' * 50)