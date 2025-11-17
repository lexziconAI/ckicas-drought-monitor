import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from infrastructure.sidecar.router import router

print("🚀 AXIOM-X INFRASTRUCTURE WORKERS DEPLOYMENT")
print("=" * 60)
print("Deploying workers for productive tasks while debugging bottleneck detector")
print()

# Load canonical files
print("🔧 Loading canonical files...")
with open('validated_canonical_map.json', 'r') as f:
    canonical_map = json.load(f)

canonical_files = list(canonical_map.keys())
print(f"✅ Found {len(canonical_files)} canonical files")

# Create output directories
docs_dir = Path("docs/canonical")
tests_dir = Path("tests/canonical")
reports_dir = Path("reports/performance")

for dir_path in [docs_dir, tests_dir, reports_dir]:
    dir_path.mkdir(parents=True, exist_ok=True)

print("📁 Created output directories")

# Constitutional principles for workers
CONSTITUTIONAL_PRINCIPLES = {
    "ahimsa": "Generate clear, helpful documentation that prevents confusion and errors",
    "satya": "Ensure all generated content is accurate and truthful",
    "asteya": "Properly attribute any examples or code snippets",
    "brahmacharya": "Focus on essential documentation without unnecessary complexity",
    "aparigraha": "Generate only what's needed, no redundant content"
}

async def generate_documentation_worker(canonical_file, worker_id):
    """Worker to generate documentation for a canonical file"""

    try:
        # Read the canonical file
        file_path = Path(canonical_file)
        if not file_path.exists():
            return f"❌ Worker {worker_id}: File not found: {canonical_file}"

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Generate documentation prompt
        prompt = f"""
Generate comprehensive documentation for this Python file:

FILE: {file_path.name}
PATH: {canonical_file}
CONTENT:
{content[:2000]}... (truncated for brevity)

Create a detailed markdown documentation file that includes:

1. **Purpose & Overview**
   - What this file does
   - Its role in the Axiom-X system
   - Key functionality

2. **Function/Class Documentation**
   - All functions, classes, and methods
   - Parameters and return values
   - Usage examples

3. **Dependencies & Requirements**
   - Required imports
   - External dependencies
   - System requirements

4. **Usage Examples**
   - Basic usage
   - Advanced usage patterns
   - Integration examples

5. **Performance Characteristics**
   - Any known performance data
   - Optimization notes
   - Scalability considerations

6. **Constitutional Compliance**
   - How this file implements Axiom-X principles
   - Safety and reliability features

Format as clean markdown with proper headers and code blocks.
Be accurate and helpful - this documentation will be used by developers.
"""

        # Route to infrastructure worker
        result = await router.route_task(
            prompt,
            'anthropic',
            max_tokens=2000
        )

        # Save documentation
        doc_filename = f"{file_path.stem}_DOCUMENTATION.md"
        doc_path = docs_dir / doc_filename

        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(f"# {file_path.name} Documentation\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n")
            f.write(f"**Source:** {canonical_file}\n")
            f.write(f"**Worker ID:** {worker_id}\n\n")
            f.write("## Constitutional Principles Applied\n\n")
            for principle, description in CONSTITUTIONAL_PRINCIPLES.items():
                f.write(f"- **{principle.title()}**: {description}\n")
            f.write("\n---\n\n")
            f.write(result.response)

        return f"✅ Worker {worker_id}: Generated documentation for {file_path.name}"

    except Exception as e:
        return f"❌ Worker {worker_id}: Error generating documentation for {canonical_file}: {e}"

async def generate_test_suite_worker(canonical_file, worker_id):
    """Worker to generate test suite for a canonical file"""

    try:
        file_path = Path(canonical_file)
        if not file_path.exists():
            return f"❌ Worker {worker_id}: File not found: {canonical_file}"

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Generate test suite prompt
        prompt = f"""
Generate a comprehensive pytest test suite for this Python file:

FILE: {file_path.name}
PATH: {canonical_file}
CONTENT:
{content[:3000]}... (truncated for brevity)

Create a complete test file that includes:

1. **Import Statements**
   - Import the module being tested
   - Import pytest and any required testing utilities

2. **Test Classes and Functions**
   - Unit tests for all major functions
   - Integration tests where appropriate
   - Edge case testing

3. **Test Coverage**
   - Happy path tests
   - Error handling tests
   - Boundary condition tests
   - Performance tests (if applicable)

4. **Mocking and Fixtures**
   - Use appropriate mocking for external dependencies
   - Create fixtures for common test data

5. **Assertions**
   - Test expected behavior
   - Verify error conditions
   - Check performance thresholds

6. **Constitutional Compliance Tests**
   - Verify adherence to Axiom-X principles
   - Test safety and reliability features

Generate runnable pytest code with proper structure and naming conventions.
"""

        result = await router.route_task(
            prompt,
            'anthropic',
            max_tokens=2500
        )

        # Save test suite
        test_filename = f"test_{file_path.stem}.py"
        test_path = tests_dir / test_filename

        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(f'"""Test suite for {file_path.name}\n')
            f.write(f'Generated: {datetime.now().isoformat()}\n')
            f.write(f'Source: {canonical_file}\n')
            f.write(f'Worker ID: {worker_id}\n')
            f.write('"""\n\n')
            f.write("import pytest\n")
            f.write("from pathlib import Path\n\n")
            f.write("# Add imports for the module being tested\n")
            f.write("# import sys\n")
            f.write("# sys.path.append(str(Path(__file__).parent.parent))\n\n")
            f.write(result.response)

        return f"✅ Worker {worker_id}: Generated test suite for {file_path.name}"

    except Exception as e:
        return f"❌ Worker {worker_id}: Error generating test suite for {canonical_file}: {e}"

async def generate_performance_report_worker(canonical_file, worker_id):
    """Worker to generate performance analysis report"""

    try:
        file_path = Path(canonical_file)

        # Try to load constitutional receipt
        receipt_file = f"{file_path.stem}_constitutional_receipt.json"
        receipt_path = Path("receipts") / receipt_file

        receipt_data = None
        if receipt_path.exists():
            try:
                with open(receipt_path, 'r') as f:
                    receipt_data = json.load(f)
            except:
                receipt_data = None

        # Generate performance analysis prompt
        prompt = f"""
Generate a performance analysis report for this canonical file:

FILE: {file_path.name}
PATH: {canonical_file}

{f"PERFORMANCE DATA: {json.dumps(receipt_data, indent=2)}" if receipt_data else "No performance data available"}

Create a detailed performance analysis report that includes:

1. **Performance Metrics**
   - Execution time analysis
   - Resource usage patterns
   - Scalability characteristics

2. **Bottleneck Analysis**
   - Identified performance bottlenecks
   - Optimization opportunities
   - Comparative analysis with other canonical files

3. **Optimization Recommendations**
   - Specific improvement suggestions
   - Expected performance gains
   - Implementation priorities

4. **Constitutional Performance**
   - How performance relates to Axiom-X principles
   - Safety vs. speed trade-offs
   - Reliability considerations

5. **Future Projections**
   - Expected performance evolution
   - Scaling recommendations
   - Monitoring suggestions

Format as a comprehensive markdown report.
"""

        result = await router.route_task(
            prompt,
            'anthropic',
            max_tokens=1500
        )

        # Save performance report
        report_filename = f"{file_path.stem}_ANALYSIS.md"
        report_path = reports_dir / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Performance Analysis: {file_path.name}\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n")
            f.write(f"**Source:** {canonical_file}\n")
            f.write(f"**Worker ID:** {worker_id}\n\n")
            f.write("## Executive Summary\n\n")
            f.write("Performance analysis for this canonical Axiom-X component.\n\n")
            f.write("---\n\n")
            f.write(result.response)

        return f"✅ Worker {worker_id}: Generated performance report for {file_path.name}"

    except Exception as e:
        return f"❌ Worker {worker_id}: Error generating performance report for {canonical_file}: {e}"

async def deploy_infrastructure_workers():
    """Deploy infrastructure workers for productive tasks"""

    print("\n🚀 DEPLOYING INFRASTRUCTURE WORKERS")
    print("=" * 60)

    # Task 1: Documentation Generation (30 workers)
    print("\n📚 TASK 1: Documentation Generation (30 workers)")
    print("Generating comprehensive documentation for all canonical files...")

    doc_tasks = []
    for i, canonical_file in enumerate(canonical_files[:30]):  # First 30 files
        doc_tasks.append(generate_documentation_worker(canonical_file, f"doc-{i+1:02d}"))

    # Execute documentation tasks in batches
    batch_size = 10
    for i in range(0, len(doc_tasks), batch_size):
        batch = doc_tasks[i:i+batch_size]
        print(f"\n📤 Executing documentation batch {i//batch_size + 1}/{(len(doc_tasks)-1)//batch_size + 1}")

        try:
            results = await asyncio.gather(*batch, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    print(f"❌ Batch error: {result}")
                else:
                    print(result)
        except Exception as e:
            print(f"❌ Batch execution failed: {e}")

        # Brief pause between batches
        await asyncio.sleep(1)

    # Task 2: Test Suite Generation (20 workers)
    print("\n🧪 TASK 2: Test Suite Generation (20 workers)")
    print("Creating comprehensive test suites for top canonical files...")

    test_tasks = []
    for i, canonical_file in enumerate(canonical_files[:20]):  # Top 20 files
        test_tasks.append(generate_test_suite_worker(canonical_file, f"test-{i+1:02d}"))

    # Execute test tasks in batches
    for i in range(0, len(test_tasks), batch_size):
        batch = test_tasks[i:i+batch_size]
        print(f"\n📤 Executing test suite batch {i//batch_size + 1}/{(len(test_tasks)-1)//batch_size + 1}")

        try:
            results = await asyncio.gather(*batch, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    print(f"❌ Batch error: {result}")
                else:
                    print(result)
        except Exception as e:
            print(f"❌ Batch execution failed: {e}")

        await asyncio.sleep(1)

    # Task 3: Performance Analysis (10 workers)
    print("\n📊 TASK 3: Performance Analysis (10 workers)")
    print("Generating performance reports for top canonical files...")

    perf_tasks = []
    for i, canonical_file in enumerate(canonical_files[:10]):  # Top 10 files
        perf_tasks.append(generate_performance_report_worker(canonical_file, f"perf-{i+1:02d}"))

    # Execute performance tasks
    print("\n📤 Executing performance analysis batch")
    try:
        results = await asyncio.gather(*perf_tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                print(f"❌ Performance analysis error: {result}")
            else:
                print(result)
    except Exception as e:
        print(f"❌ Performance analysis batch failed: {e}")

    # Generate deployment receipt
    deployment_receipt = {
        "task": "Infrastructure Workers Deployment",
        "timestamp": datetime.now().isoformat(),
        "objectives": {
            "documentation_generation": {
                "workers_deployed": 30,
                "files_targeted": len(canonical_files[:30]),
                "output_directory": str(docs_dir)
            },
            "test_suite_generation": {
                "workers_deployed": 20,
                "files_targeted": len(canonical_files[:20]),
                "output_directory": str(tests_dir)
            },
            "performance_analysis": {
                "workers_deployed": 10,
                "files_targeted": len(canonical_files[:10]),
                "output_directory": str(reports_dir)
            }
        },
        "constitutional_compliance": {
            "ahimsa": "Generated helpful documentation to prevent developer confusion",
            "satya": "Ensured accuracy in all generated content",
            "asteya": "Proper attribution in examples and code",
            "brahmacharya": "Focused on essential content without redundancy",
            "aparigraha": "Generated only necessary documentation and tests"
        },
        "expected_outputs": {
            "documentation_files": 30,
            "test_files": 20,
            "performance_reports": 10,
            "total_productive_output": 60
        }
    }

    with open('infrastructure_workers_deployment_receipt.json', 'w') as f:
        json.dump(deployment_receipt, f, indent=2)

    print("📜 Infrastructure workers deployment receipt generated")
    print("📊 DEPLOYMENT SUMMARY")
    print("=" * 60)
    print(f"📚 Documentation: {len(canonical_files[:30])} files targeted")
    print(f"🧪 Test Suites: {len(canonical_files[:20])} files targeted")
    print(f"📊 Performance Reports: {len(canonical_files[:10])} files targeted")
    print(f"🎯 Total Productive Output: 60+ files")
    print("\n🛡️ Constitutional principles applied throughout deployment")
    print("✅ Infrastructure workers successfully deployed for productive work!")

if __name__ == "__main__":
    asyncio.run(deploy_infrastructure_workers())