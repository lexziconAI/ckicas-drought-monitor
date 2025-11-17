"""
OUTPUT-TO-SOURCE CORRELATOR - Phase 4
Link JSON outputs back to Python source files
"""

import json
from pathlib import Path
import re
from datetime import datetime, timedelta

print("🔗 OUTPUT-TO-SOURCE CORRELATOR")
print("=" * 60)

# Load extracted performance data
with open('extracted_performance_data.json', 'r') as f:
    performance_data = json.load(f)

# Load all Python files
axiom_dir = Path("C:/Users/regan/ID SYSTEM/axiom-x")
all_py_files = list(axiom_dir.rglob("*.py"))

print(f"Python files: {len(all_py_files)}")
print(f"JSON outputs with performance data: {len(performance_data)}")

correlations = []

for perf in performance_data:
    json_path = Path(perf['source_file'])

    # Strategy 1: Direct file reference in JSON
    if 'references_file' in perf and perf['references_file']:
        file_ref = perf['references_file']
        # Try to find matching Python file
        matches = [f for f in all_py_files if file_ref in str(f)]
        if matches:
            correlations.append({
                'json_output': json_path.name,
                'python_source': str(matches[0]),
                'confidence': 'high',
                'method': 'direct_reference',
                'metrics': perf['extracted_metrics']
            })
            continue

    # Strategy 2: Name similarity and pattern matching
    # Example: operation_quantum_bodhi_results_1761718125.json → quantum_bodhi_*.py
    json_stem = json_path.stem

    # Remove common prefixes/suffixes and extract meaningful parts
    cleaned_name = json_stem
    for prefix in ['results_', 'output_', 'benchmark_', 'test_', 'operation_', 'phase']:
        cleaned_name = cleaned_name.replace(prefix, '')

    # Split by underscores and look for meaningful components
    name_parts = cleaned_name.split('_')

    # Look for Python files that contain similar components
    similar_py_files = []
    for py_file in all_py_files:
        py_stem = py_file.stem.lower()
        json_lower = cleaned_name.lower()

        # Direct substring match
        if any(part in py_stem for part in name_parts if len(part) > 3):
            similarity = sum(1 for part in name_parts if len(part) > 3 and part in py_stem) / len([p for p in name_parts if len(p) > 3])
            if similarity > 0:
                similar_py_files.append((py_file, similarity))

        # Special case: quantum bodhi results → quantum_bodhi_*.py
        if 'quantum' in json_lower and 'bodhi' in json_lower:
            if 'quantum' in py_stem and 'bodhi' in py_stem:
                similar_py_files.append((py_file, 1.0))

        # Special case: fractal optimization results → fractal_optimization_*.py
        if 'fractal' in json_lower and 'optimization' in json_lower:
            if 'fractal' in py_stem and 'optimization' in py_stem:
                similar_py_files.append((py_file, 1.0))

        # Special case: army deployment results → fractal_army_*.py or *_army_*.py
        if 'army' in json_lower and 'deployment' in json_lower:
            if 'army' in py_stem or 'fractal' in py_stem:
                similar_py_files.append((py_file, 0.8))

    if similar_py_files:
        # Take best match
        best_match = max(similar_py_files, key=lambda x: x[1])
        confidence = 'high' if best_match[1] >= 0.8 else 'medium' if best_match[1] >= 0.5 else 'low'
        correlations.append({
            'json_output': json_path.name,
            'python_source': str(best_match[0]),
            'confidence': confidence,
            'method': 'name_similarity',
            'similarity_score': best_match[1],
            'metrics': perf['extracted_metrics']
        })
        continue

    # Strategy 3: Timestamp proximity (if timestamps are available)
    # Files modified within 24 hours of JSON creation likely related
    try:
        json_mtime = datetime.fromtimestamp(json_path.stat().st_mtime)

        nearby_py_files = []
        for py_file in all_py_files:
            py_mtime = datetime.fromtimestamp(py_file.stat().st_mtime)
            time_delta = abs((json_mtime - py_mtime).total_seconds())

            # Within 24 hours
            if time_delta < 86400:  # 24 hours in seconds
                nearby_py_files.append((py_file, time_delta))

        if nearby_py_files:
            # Closest in time
            closest = min(nearby_py_files, key=lambda x: x[1])
            correlations.append({
                'json_output': json_path.name,
                'python_source': str(closest[0]),
                'confidence': 'low',
                'method': 'timestamp_proximity',
                'time_delta_seconds': closest[1],
                'metrics': perf['extracted_metrics']
            })
    except:
        pass

print(f"\n✅ Correlated {len(correlations)} JSON outputs to Python sources")

# Save correlations
with open('output_source_correlations.json', 'w') as f:
    json.dump(correlations, f, indent=2)

print(f"💾 Saved to: output_source_correlations.json")

# Show high-confidence correlations with breakthrough data
print("\n🌟 HIGH-CONFIDENCE CORRELATIONS WITH BREAKTHROUGH METRICS:")

high_conf = [c for c in correlations if c['confidence'] == 'high']
breakthrough_correlations = []

for corr in high_conf:
    # Check if has breakthrough metrics
    has_breakthrough = False
    breakthrough_values = []

    for metric, value in corr.get('metrics', {}).items():
        if isinstance(value, (int, float)):
            # Check for known breakthrough values
            if abs(value - 25504) < 1:  # 25,504 ops/sec
                has_breakthrough = True
                breakthrough_values.append(f"25,504 ops/sec")
            elif abs(value - 11.4) < 0.1:  # 11.4x speedup
                has_breakthrough = True
                breakthrough_values.append("11.4x speedup")
            elif abs(value - 10.0) < 0.1:  # 10.0 perfection score
                has_breakthrough = True
                breakthrough_values.append("10.0 perfection score")
            elif abs(value - 0.89) < 0.01:  # 0.89 constitutional score
                has_breakthrough = True
                breakthrough_values.append("0.89 constitutional score")
            # Also check for very high performance values
            elif value > 1000000:  # Million+ ops
                has_breakthrough = True
                breakthrough_values.append(f"{value:,.0f} ops")

    if has_breakthrough:
        breakthrough_correlations.append({
            **corr,
            'breakthrough_values': breakthrough_values
        })

# Sort by most breakthrough values
breakthrough_correlations.sort(key=lambda x: len(x['breakthrough_values']), reverse=True)

for corr in breakthrough_correlations[:20]:  # Show top 20
    print(f"\n{Path(corr['python_source']).name}")
    print(f"   Output: {corr['json_output']}")
    print(f"   Method: {corr['method']} (confidence: {corr['confidence']})")
    print(f"   Breakthrough Values: {', '.join(corr['breakthrough_values'])}")
    if 'similarity_score' in corr:
        print(f"   Similarity: {corr['similarity_score']:.2f}")

print("\n" + "=" * 60)

# Summary statistics
print("CORRELATION SUMMARY:")
print(f"Total correlations: {len(correlations)}")
print(f"High confidence: {len([c for c in correlations if c['confidence'] == 'high'])}")
print(f"Medium confidence: {len([c for c in correlations if c['confidence'] == 'medium'])}")
print(f"Low confidence: {len([c for c in correlations if c['confidence'] == 'low'])}")
print(f"With breakthrough data: {len(breakthrough_correlations)}")

print("\n🎯 KEY FINDINGS:")
if breakthrough_correlations:
    # Find the file with the most breakthrough values
    top_file = max(breakthrough_correlations, key=lambda x: len(x['breakthrough_values']))
    print(f"   Top correlated file: {Path(top_file['python_source']).name}")
    print(f"   Breakthrough metrics: {len(top_file['breakthrough_values'])}")
    print(f"   Values: {', '.join(top_file['breakthrough_values'])}")

print("\n" + "=" * 60)