import json
from pathlib import Path

# Load correlations
with open('output_source_correlations.json', 'r') as f:
    correlations = json.load(f)

# Find the top breakthrough correlation
breakthrough_correlations = []
for corr in correlations:
    breakthrough_values = []
    for metric, value in corr.get('metrics', {}).items():
        if isinstance(value, (int, float)):
            if abs(value - 25504) < 1:
                breakthrough_values.append('25,504 ops/sec')
            elif abs(value - 11.4) < 0.1:
                breakthrough_values.append('11.4x speedup')
            elif abs(value - 10.0) < 0.1:
                breakthrough_values.append('10.0 perfection score')
            elif abs(value - 0.89) < 0.01:
                breakthrough_values.append('0.89 constitutional score')

    if breakthrough_values:
        breakthrough_correlations.append({
            **corr,
            'breakthrough_values': breakthrough_values
        })

# Sort by number of breakthrough values
breakthrough_correlations.sort(key=lambda x: len(x['breakthrough_values']), reverse=True)

# Show details of top correlation
if breakthrough_correlations:
    top = breakthrough_correlations[0]
    print('TOP BREAKTHROUGH CORRELATION DETAILS:')
    print(f'Python Source: {Path(top["python_source"]).name}')
    print(f'JSON Output: {top["json_output"]}')
    print(f'Confidence: {top["confidence"]}')
    print(f'Breakthrough Values Found: {len(top["breakthrough_values"])}')
    print(f'Values: {top["breakthrough_values"]}')
    print(f'Method: {top["method"]}')

    # Show some metrics
    print(f'Sample Metrics: {dict(list(top.get("metrics", {}).items())[:10])}')