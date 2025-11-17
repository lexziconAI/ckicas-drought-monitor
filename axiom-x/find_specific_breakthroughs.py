import json
from pathlib import Path

# Load correlations
with open('output_source_correlations.json', 'r') as f:
    correlations = json.load(f)

# Find correlations with the specific breakthrough values
specific_breakthroughs = []

for corr in correlations:
    has_25504 = False
    has_11_4 = False
    has_10_0 = False
    has_0_89 = False

    for metric, value in corr.get('metrics', {}).items():
        if isinstance(value, (int, float)):
            if abs(value - 25504) < 1:
                has_25504 = True
            elif abs(value - 11.4) < 0.1:
                has_11_4 = True
            elif abs(value - 10.0) < 0.1:
                has_10_0 = True
            elif abs(value - 0.89) < 0.01:
                has_0_89 = True

    if has_25504 or has_11_4 or has_10_0 or has_0_89:
        breakthrough_types = []
        if has_25504: breakthrough_types.append('25,504 ops/sec')
        if has_11_4: breakthrough_types.append('11.4x speedup')
        if has_10_0: breakthrough_types.append('10.0 perfection score')
        if has_0_89: breakthrough_types.append('0.89 constitutional score')

        specific_breakthroughs.append({
            **corr,
            'breakthrough_types': breakthrough_types
        })

print(f'Correlations with specific breakthrough values: {len(specific_breakthroughs)}')

# Show details
for i, corr in enumerate(specific_breakthroughs[:5]):
    print(f'\n{i+1}. {Path(corr["python_source"]).name}')
    print(f'   Output: {corr["json_output"]}')
    print(f'   Confidence: {corr["confidence"]}')
    print(f'   Breakthrough Types: {corr["breakthrough_types"]}')
    print(f'   Method: {corr["method"]}')

# Check if fractal_optimization_orchestrator.py is among them
fractal_found = any('fractal_optimization_orchestrator.py' in corr['python_source'] for corr in specific_breakthroughs)
print(f'\nFractal optimization orchestrator found: {fractal_found}')

if fractal_found:
    fractal_corr = next(corr for corr in specific_breakthroughs if 'fractal_optimization_orchestrator.py' in corr['python_source'])
    print(f'Fractal orchestrator correlation: {fractal_corr["json_output"]} (confidence: {fractal_corr["confidence"]})')