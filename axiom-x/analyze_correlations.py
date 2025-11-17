import json
from pathlib import Path

print('ANALYZING OUTPUT-SOURCE CORRELATIONS')
print('=' * 50)

# Load correlations (streaming to avoid memory issues)
correlations = []
with open('output_source_correlations.json', 'r') as f:
    correlations = json.load(f)

print(f'Total correlations: {len(correlations)}')

# Analyze by confidence
confidence_counts = {}
method_counts = {}
breakthrough_correlations = []

for corr in correlations:
    conf = corr['confidence']
    confidence_counts[conf] = confidence_counts.get(conf, 0) + 1

    method = corr['method']
    method_counts[method] = method_counts.get(method, 0) + 1

    # Check for breakthrough data
    has_breakthrough = False
    breakthrough_values = []

    for metric, value in corr.get('metrics', {}).items():
        if isinstance(value, (int, float)):
            if abs(value - 25504) < 1:  # 25,504 ops/sec
                has_breakthrough = True
                breakthrough_values.append('25,504 ops/sec')
            elif abs(value - 11.4) < 0.1:  # 11.4x speedup
                has_breakthrough = True
                breakthrough_values.append('11.4x speedup')
            elif abs(value - 10.0) < 0.1:  # 10.0 perfection score
                has_breakthrough = True
                breakthrough_values.append('10.0 perfection score')
            elif abs(value - 0.89) < 0.01:  # 0.89 constitutional score
                has_breakthrough = True
                breakthrough_values.append('0.89 constitutional score')

    if has_breakthrough:
        breakthrough_correlations.append({
            **corr,
            'breakthrough_values': breakthrough_values
        })

print(f'Confidence levels: {confidence_counts}')
print(f'Methods used: {method_counts}')
print(f'Correlations with breakthrough data: {len(breakthrough_correlations)}')

# Show top breakthrough correlations
print('\nTOP BREAKTHROUGH CORRELATIONS:')
breakthrough_correlations.sort(key=lambda x: len(x['breakthrough_values']), reverse=True)

for i, corr in enumerate(breakthrough_correlations[:10]):
    print(f'\n{i+1}. {Path(corr["python_source"]).name}')
    print(f'   Output: {corr["json_output"]}')
    print(f'   Confidence: {corr["confidence"]}')
    print(f'   Breakthrough Values: {len(corr["breakthrough_values"])}')

print('\n' + '=' * 50)