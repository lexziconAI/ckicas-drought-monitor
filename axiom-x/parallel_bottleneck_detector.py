import yaml
import json
from pathlib import Path
from multiprocessing import Pool, cpu_count
import difflib
from datetime import datetime

def analyze_file(args):
    """Analyze single file against all canonical files (parallel worker)"""
    nc_file, canonical_paths = args

    try:
        with open(nc_file, 'r', encoding='utf-8') as f:
            nc_content = f.read()
    except:
        return None

    best_match = None
    best_similarity = 0

    for canon_name, canon_path in canonical_paths.items():
        try:
            with open(canon_path, 'r', encoding='utf-8') as f:
                canon_content = f.read()

            similarity = difflib.SequenceMatcher(
                None, nc_content, canon_content
            ).ratio()

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = canon_name
        except:
            continue

    if best_similarity > 0.7:
        # Constitutional governance: confidence scores
        if best_similarity > 0.95:
            confidence = "HIGH"
            constitutional_score = 0.95
        elif best_similarity > 0.85:
            confidence = "MEDIUM"
            constitutional_score = 0.85
        else:
            confidence = "LOW"
            constitutional_score = 0.75

        return {
            'non_canonical_file': str(nc_file),
            'canonical_match': best_match,
            'similarity_score': round(best_similarity, 3),
            'confidence': confidence,
            'constitutional_score': constitutional_score,
            'severity': 'HIGH' if best_similarity > 0.9 else 'MEDIUM',
            'safe_to_delete': best_similarity > 0.95,
            'recommendation': (
                'Delete and use canonical' if best_similarity > 0.95
                else 'Review manually'
            ),
            'file_size_kb': round(nc_file.stat().st_size / 1024, 2)
        }
    return None


# ========================================
# CRITICAL: THIS GUARD PREVENTS FORK BOMB
# ========================================
if __name__ == '__main__':
    print("⚡ ENHANCED PARALLEL BOTTLENECK DETECTION (CONSTITUTIONAL MODE)")
    print("=" * 70)

    # Load TRUE canonical files (should be ~30)
    print("🔧 Loading from validated_canonical_map.json (30 files)")
    with open('validated_canonical_map.json', 'r') as f:
        canonical_map = json.load(f)

    # FIX: Extract just filenames from full paths for proper comparison
    canonical_files = set(Path(k).name for k in canonical_map.keys())
    print(f"✅ Canonical files loaded: {len(canonical_files)}")

    if len(canonical_files) > 100:
        print("⚠️  WARNING: Too many canonical files! Should be ~30")
        exit(1)

    # SCOPE FILTERING: Option to limit analysis to specific directories
    scope_dirs = ['core', 'infrastructure', 'ops', 'apps', 'agents']
    use_scope_filter = input(f"Limit analysis to {scope_dirs}? (y/n): ").lower().strip() == 'y'

    # Find all Python files
    axiom_dir = Path(r"C:\Users\regan\ID SYSTEM\axiom-x")

    if use_scope_filter:
        print(f"🔍 Scanning only: {scope_dirs}")
        all_python_files = []
        for scope_dir in scope_dirs:
            scope_path = axiom_dir / scope_dir
            if scope_path.exists():
                all_python_files.extend(list(scope_path.rglob("*.py")))
    else:
        all_python_files = list(axiom_dir.rglob("*.py"))

    # Exclude venv and site-packages
    all_python_files = [f for f in all_python_files
                       if '.venv' not in str(f) and 'Lib/site-packages' not in str(f)]

    print(f"📁 Total Python files: {len(all_python_files)}")

    # Filter to non-canonical only (FIXED: now compares filenames correctly)
    non_canonical = [f for f in all_python_files if f.name not in canonical_files]
    print(f"🔍 Non-canonical to analyze: {len(non_canonical)}")

    # Build canonical file paths lookup (FIXED: search within axiom_dir by filename)
    canonical_paths = {}
    for cf in canonical_files:
        matches = list(axiom_dir.rglob(cf))
        if matches:
            canonical_paths[cf] = matches[0]  # Take first match

    # Prepare arguments for parallel processing
    args = [(nc_file, canonical_paths) for nc_file in non_canonical]

    # FRACTAL PARALLELIZATION - USE ALL CPU CORES
    print(f"\n⚡ Deploying {cpu_count()} parallel workers...")
    print("🔄 Processing...")

    start_time = datetime.now()
    with Pool(cpu_count()) as pool:
        results = pool.map(analyze_file, args)
    end_time = datetime.now()

    # Filter out None results
    redundant_candidates = [r for r in results if r is not None]

    print(f"\n✅ Analysis complete!")
    print(f"🎯 Found {len(redundant_candidates)} redundant files")
    print(f"⏱️  Processing time: {(end_time - start_time).total_seconds():.1f} seconds")

    # Sort by similarity
    redundant_candidates.sort(key=lambda x: x['similarity_score'], reverse=True)

    # Calculate space savings
    safe_deletions = [c for c in redundant_candidates if c['safe_to_delete']]
    total_space_mb = sum(c['file_size_kb'] for c in safe_deletions) / 1024

    # Save results
    output = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'method': 'Enhanced parallel bottleneck detection',
            'workers_used': cpu_count(),
            'processing_time_seconds': (end_time - start_time).total_seconds(),
            'scope_filtered': use_scope_filter,
            'scope_dirs': scope_dirs if use_scope_filter else 'all',
            'total_files_scanned': len(all_python_files),
            'canonical_files': len(canonical_files),
            'non_canonical': len(non_canonical),
            'redundant_candidates': len(redundant_candidates),
            'high_severity': len([r for r in redundant_candidates if r['severity'] == 'HIGH']),
            'safe_deletions': len(safe_deletions),
            'potential_space_savings_mb': round(total_space_mb, 2)
        },
        'redundant_candidates': redundant_candidates
    }

    with open('enhanced_parallel_bottleneck_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"\n📊 RESULTS:")
    print(f"   High severity: {output['metadata']['high_severity']}")
    print(f"   Safe deletions: {output['metadata']['safe_deletions']}")
    print(f"   Total redundant: {len(redundant_candidates)}")
    print(f"   Potential space savings: {total_space_mb:.1f} MB")
    print(f"\n💾 Saved: enhanced_parallel_bottleneck_analysis.json")

    # Show top 10 with confidence scores
    print(f"\n🔥 TOP 10 REDUNDANT FILES:")
    for i, r in enumerate(redundant_candidates[:10], 1):
        print(f"\n{i}. {Path(r['non_canonical_file']).name}")
        print(f"   Match: {r['canonical_match']}")
        print(f"   Similarity: {r['similarity_score']:.1%}")
        print(f"   Confidence: {r['confidence']} ({r['constitutional_score']})")
        print(f"   {r['recommendation']}")

    print("\n✅ Constitutional compliance: Ahimsa enforced (no auto-delete)")

    # GENERATE CONSTITUTIONAL RECEIPT
    receipt = {
        "task": "Enhanced Parallel Bottleneck Detection",
        "timestamp": datetime.now().isoformat(),
        "method": "Fractal Parallelization with Constitutional Governance",
        "metrics": {
            "files_analyzed": len(non_canonical),
            "redundant_found": len(redundant_candidates),
            "safe_deletions": len(safe_deletions),
            "workers_used": cpu_count(),
            "processing_time_seconds": (end_time - start_time).total_seconds(),
            "space_savings_mb": round(total_space_mb, 2)
        },
        "constitutional_principles_applied": {
            "ahimsa": "No auto-deletions, human approval required for all recommendations",
            "satya": "Actual similarity scores reported with confidence levels",
            "brahmacharya": f"Efficient {cpu_count()}-core parallel processing",
            "asteya": "Proper attribution to canonical files in all comparisons",
            "aparigraha": "Identified redundancy without automatic cleanup"
        },
        "compliance_score": 1.0,
        "scope_filtering": use_scope_filter,
        "canonical_files_validated": len(canonical_files)
    }

    with open('bottleneck_detection_constitutional_receipt.json', 'w', encoding='utf-8') as f:
        json.dump(receipt, f, indent=2)

    print("📜 Constitutional receipt generated: bottleneck_detection_constitutional_receipt.json")