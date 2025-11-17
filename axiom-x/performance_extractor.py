"""
PERFORMANCE DATA EXTRACTOR - Phase 3
Extract performance data from high-value JSON files
"""

import json
from pathlib import Path
from datetime import datetime

print("⛏️  PERFORMANCE DATA EXTRACTOR")
print("=" * 60)

# Load categorization results
with open('json_categorization_results.json', 'r') as f:
    categories = json.load(f)

# Priority order for mining
priority_categories = [
    'known_breakthrough_numbers',
    'performance_benchmarks',
    'breakthrough_indicators',
    'execution_results'
]

all_performance_data = []

for category in priority_categories:
    files = categories.get(category, [])
    print(f"\n🔍 Mining: {category} ({len(files)} files)")

    processed = 0
    for file_info in files:
        processed += 1
        if processed % 100 == 0:
            print(f"  Processed {processed}/{len(files)} files in {category}...")

        if isinstance(file_info, str):
            file_path = file_info
        else:
            file_path = file_info.get('path')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract performance indicators (CAST WIDE NET)
            perf_data = {
                'source_file': file_path,
                'source_name': Path(file_path).name,
                'category': category,
                'extracted_metrics': {}
            }

            # Recursively search for performance keywords
            def extract_metrics(obj, prefix=''):
                """Recursively extract any performance-related data"""
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        # Performance indicators
                        if any(kw in key.lower() for kw in [
                            'ops', 'throughput', 'latency', 'speedup',
                            'performance', 'benchmark', 'score', 'rating',
                            'breakthrough', 'optimal', 'peak', 'best',
                            'efficiency', 'improvement', 'gain', 'delta',
                            'multiplier', 'factor', 'ratio', 'percentage'
                        ]):
                            perf_data['extracted_metrics'][f"{prefix}{key}"] = value

                        # Also check for known breakthrough values in any numeric field
                        if isinstance(value, (int, float)) and value in [25504, 11.4, 10.0, 0.89]:
                            perf_data['extracted_metrics'][f"{prefix}{key}_breakthrough"] = value

                        # Recurse into nested structures
                        extract_metrics(value, f"{prefix}{key}.")

                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        extract_metrics(item, f"{prefix}[{i}].")

            extract_metrics(data)

            # Also check for file references
            for key in ['file', 'script', 'module', 'source_file', 'target', 'python_file', 'source']:
                if key in data:
                    file_ref = data.get(key)
                    if file_ref:
                        perf_data['references_file'] = str(file_ref)

            # Add timestamp
            for key in ['timestamp', 'created', 'execution_time', 'run_date', 'date']:
                if key in data:
                    perf_data['timestamp'] = data[key]

            # Only keep if we found performance data
            if perf_data['extracted_metrics']:
                all_performance_data.append(perf_data)
                metrics_count = len(perf_data['extracted_metrics'])
                if metrics_count > 5:  # Only show files with substantial metrics
                    print(f"   ✅ {Path(file_path).name}: {metrics_count} metrics")

        except Exception as e:
            continue

print("\n" + "=" * 60)
print(f"📊 EXTRACTION COMPLETE: {len(all_performance_data)} files with performance data")
print("=" * 60)

# Save comprehensive results
with open('extracted_performance_data.json', 'w') as f:
    json.dump(all_performance_data, f, indent=2)

print(f"\n💾 Saved to: extracted_performance_data.json")

# Show top performers
print("\n🌟 TOP PERFORMANCE INDICATORS FOUND:")

# Group by metric type
metric_summary = {}
for perf in all_performance_data:
    for metric, value in perf['extracted_metrics'].items():
        if isinstance(value, (int, float)):
            if metric not in metric_summary:
                metric_summary[metric] = []
            metric_summary[metric].append({
                'value': value,
                'source': perf['source_name'],
                'category': perf['category'],
                'file_ref': perf.get('references_file', 'unknown')
            })

# Show highest values for each metric (top 20)
shown_metrics = 0
for metric, values in sorted(metric_summary.items(), key=lambda x: max(v['value'] for v in x[1]), reverse=True):
    if shown_metrics >= 20:
        break

    if len(values) > 0:
        top_value = max(values, key=lambda x: x['value'])
        print(f"\n{metric}:")
        print(f"   Peak: {top_value['value']}")
        print(f"   Source: {top_value['source']} ({top_value['category']})")
        if top_value['file_ref'] != 'unknown':
            print(f"   References: {top_value['file_ref']}")
        shown_metrics += 1

print("\n" + "=" * 60)

# Special focus on breakthrough values
print("🎯 BREAKTHROUGH VALUE ANALYSIS:")
breakthrough_values = {
    25504: "25,504 ops/sec",
    11.4: "11.4x speedup",
    10.0: "10.0 perfection score",
    0.89: "0.89 constitutional score"
}

for target_value, description in breakthrough_values.items():
    found_files = []
    for perf in all_performance_data:
        for metric, value in perf['extracted_metrics'].items():
            if isinstance(value, (int, float)) and abs(value - target_value) < 0.01:
                found_files.append({
                    'file': perf['source_name'],
                    'metric': metric,
                    'category': perf['category']
                })

    if found_files:
        print(f"\n{description} ({target_value}):")
        for found in found_files[:5]:  # Show top 5
            print(f"   • {found['file']} - {found['metric']} ({found['category']})")
        if len(found_files) > 5:
            print(f"   ... and {len(found_files) - 5} more files")

print("\n" + "=" * 60)