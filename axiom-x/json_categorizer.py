"""
JSON FILE CATEGORIZER - Phase 2
Scan all JSON files and categorize by content signatures
"""

import json
from pathlib import Path
from collections import defaultdict

print("🔍 JSON FILE CATEGORIZER")
print("=" * 60)

axiom_dir = Path("C:/Users/regan/ID SYSTEM/axiom-x")

# Categories based on field signatures
categories = defaultdict(list)

# Read the list of all JSON files
all_json_paths = []
print("Scanning ALL directories for JSON files (including .venv, node_modules)...")

# Use pathlib to find ALL JSON files - don't exclude anything except truly irrelevant dirs
exclude_patterns = ['__pycache__', '.git']
for json_file in axiom_dir.rglob("*.json"):
    # Only exclude truly irrelevant directories
    if not any(skip in str(json_file) for skip in exclude_patterns):
        all_json_paths.append(json_file)

print(f"Found {len(all_json_paths)} JSON files via comprehensive pathlib scan")

print(f"Found {len(all_json_paths)} JSON files to analyze\n")

print("Categorizing by content type...")

processed = 0
for json_file in all_json_paths:
    processed += 1
    if processed % 500 == 0:
        print(f"Processed {processed}/{len(all_json_paths)} files...")

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Category 1: EXECUTION RESULTS
        # Look for: results, output, execution, benchmark, test_results
        if any(key in data for key in [
            'results', 'output', 'execution_result', 'test_results',
            'benchmark', 'performance', 'metrics', 'statistics'
        ]):
            categories['execution_results'].append({
                'path': str(json_file),
                'name': json_file.name,
                'keys': list(data.keys())[:10]  # First 10 keys
            })

        # Category 2: PERFORMANCE BENCHMARKS
        # Look for: ops_per_second, throughput, latency, speedup
        if any(key in str(data).lower() for key in [
            'ops_per_second', 'ops/sec', 'throughput', 'latency',
            'speedup', 'performance_score', 'benchmark_result'
        ]):
            categories['performance_benchmarks'].append({
                'path': str(json_file),
                'name': json_file.name,
                'keys': list(data.keys())[:10]
            })

        # Category 3: BREAKTHROUGH INDICATORS
        # Look for: breakthrough, success, achievement, milestone
        if any(key in str(data).lower() for key in [
            'breakthrough', 'achievement', 'milestone', 'success',
            'optimal', 'best_result', 'peak_performance'
        ]):
            categories['breakthrough_indicators'].append({
                'path': str(json_file),
                'name': json_file.name,
                'keys': list(data.keys())[:10]
            })

        # Category 4: NUMERICAL EVIDENCE
        # Look for specific numbers we know (25504, 11.4, 10.0)
        content_str = str(data)
        if any(num in content_str for num in [
            '25504', '25,504',  # The ops/sec breakthrough
            '11.4', '11.40',    # The speedup multiplier
            '10.0', '10.00',    # Operation Phoenix score
            '0.89', '0.890'     # Constitutional score
        ]):
            categories['known_breakthrough_numbers'].append({
                'path': str(json_file),
                'name': json_file.name,
                'found_numbers': [n for n in ['25504', '11.4', '10.0', '0.89']
                                 if n in content_str]
            })

        # Category 5: TIMESTAMPS DURING BREAKTHROUGH PERIODS
        # Look for dates: Oct 2024 (known breakthrough period)
        if any(date in str(data) for date in [
            '2024-10', '2024-11',  # Recent breakthrough months
            'october 2024', 'november 2024'
        ]):
            categories['breakthrough_period_outputs'].append({
                'path': str(json_file),
                'name': json_file.name
            })

        # Category 6: AGENT/SWARM OUTPUTS
        # Look for: agents, swarm, coordinator, orchestrator
        if any(key in str(data).lower() for key in [
            'agent', 'swarm', 'coordinator', 'orchestrator',
            'parallel', 'concurrent', 'worker'
        ]):
            categories['agent_outputs'].append({
                'path': str(json_file),
                'name': json_file.name
            })

        # Category 7: FILE REFERENCES
        # Look for references to Python files (these link outputs to source)
        if any(key in data for key in [
            'file', 'script', 'module', 'source_file', 'target'
        ]):
            file_ref = data.get('file') or data.get('script') or data.get('module')
            categories['file_references'].append({
                'path': str(json_file),
                'name': json_file.name,
                'references': file_ref
            })

    except Exception as e:
        # Skip invalid/corrupted JSON
        categories['corrupted'].append(str(json_file))
        continue

# Print summary
print("\n" + "=" * 60)
print("CATEGORIZATION COMPLETE")
print("=" * 60)

for category, files in sorted(categories.items()):
    print(f"\n📊 {category.upper().replace('_', ' ')}: {len(files)} files")

    # Show top 5 examples
    if files and category != 'corrupted':
        print("   Top examples:")
        for item in files[:5]:
            if isinstance(item, dict):
                print(f"   • {item['name']}")
                if 'found_numbers' in item:
                    print(f"     Numbers: {item['found_numbers']}")
            else:
                print(f"   • {Path(item).name}")

print("\n" + "=" * 60)

# CRITICAL: Focus on high-value categories
print("\n🎯 HIGH-VALUE TARGETS FOR DEEP ANALYSIS:")
print(f"   1. Known breakthrough numbers: {len(categories['known_breakthrough_numbers'])} files")
print(f"   2. Performance benchmarks: {len(categories['performance_benchmarks'])} files")
print(f"   3. Breakthrough indicators: {len(categories['breakthrough_indicators'])} files")
print(f"   4. Execution results: {len(categories['execution_results'])} files")

# Save detailed results
with open('json_categorization_results.json', 'w') as f:
    json.dump(dict(categories), f, indent=2)

print(f"\n💾 Detailed results saved to: json_categorization_results.json")
print("\n" + "=" * 60)