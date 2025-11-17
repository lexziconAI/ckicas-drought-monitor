---
author: "Regan William DUFF"
company: "AXIOM INTELLIGENCE LIMITED"
company_number: "9287393"
date: "October 26, 2025"
cryptographic_signature: "570e49843eb8b5fe77bf1df3c5ee8d951d57cbb0c2000698dbe71c5a318f2bc4"
constitutional_compliance: "Satya, Asteya, Ahimsa"
provenance_hash: "3fec3343791dcab2ed0ece0f7d9fc4e33d348a453abc342fdbe9751adeca3beb"
---

# CMG Log⁴ Brain: Semantic Memory System

## Overview

The Log⁴ Brain gives CMG (Computational Meta-Governance) semantic memory through **transformer embeddings**. It turns your sprawling codebase, receipts, and policies into a searchable semantic map that enables:

✅ **Prior art discovery** - Find related code before writing  
✅ **Duplicate detection** - Spot near-duplicate proposals  
✅ **Semantic clustering** - Group related changes  
✅ **Design brief generation** - Create test plans before code exists  
✅ **Multi-scale analysis** - System → Subsystem → Module → Function

## Quick Start

### 1. Build the Index

```powershell
# From axiom-x root
python tools/cmg_build_index.py --out .cmg/index
```

**Result**: 2001 chunks indexed across 286 files  
**Model**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)  
**Time**: ~10 seconds on first run

### 2. Query the Index

```python
from cmg.src.embeddings import SemanticRetriever
from pathlib import Path

retriever = SemanticRetriever(Path(".cmg/index"))
results = retriever.query("telemetry aggregation privacy", k=5)

for hit in results:
    print(f"[{hit['kind']}] {hit['path']} (score={hit['score']:.3f})")
```

### 3. Run Log⁴ Analysis

```python
from cmg.src.semantic_retriever import Log4Analyzer

analyzer = Log4Analyzer(Path(".cmg/index"))
brief = analyzer.analyze("improve anomaly detection with ML", k=12)

print(f"Keywords: {brief.keywords}")
print(f"Top findings: {len(brief.top_findings)}")
print(f"Clusters: {len(brief.semantic_clusters)}")
```

### 4. Generate Policy Blueprint

```python
from cmg.src.blueprint_generator import BlueprintGenerator

generator = BlueprintGenerator(Path(".cmg/index"))
blueprint = generator.generate("Add rate limiting to API endpoints")

print(f"Prior art: {blueprint.prior_art}")
print(f"Scenarios: {[s.value for s in blueprint.simulation_scenarios]}")
print(f"Risks: {blueprint.risk_factors}")
print(f"Stakeholders: {blueprint.stakeholder_groups}")

# Save for review
path = generator.save_blueprint(blueprint)
```

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CMG Log⁴ Brain                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📁 Index (.cmg/index/)                                      │
│     ├── faiss.index         (FAISS flat index)              │
│     ├── meta.jsonl          (metadata store)                 │
│     └── manifest.json       (build info)                     │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  🧠 Embeddings (cmg/src/embeddings.py)                      │
│     ├── UnifiedEmbedder     (sentence-transformers)         │
│     ├── VectorStore         (FAISS + JSONL)                 │
│     ├── SemanticRetriever   (high-level queries)            │
│     └── semantic_fingerprint(SHA256 tagging)                │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  🔬 Log⁴ Analyzer (cmg/src/semantic_retriever.py)          │
│     └── Multi-scale analysis:                                │
│         Level 1: System-wide neighbors                       │
│         Level 2: Subsystem focus (policies/docs/tests)      │
│         Level 3: Module drilldown                            │
│         Level 4: Function granularity (keywords + clusters) │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  🎯 Blueprint Generator (cmg/src/blueprint_generator.py)    │
│     ├── Simulation scenario selection                        │
│     ├── Risk factor extraction                               │
│     ├── Acceptance criteria generation                       │
│     ├── Stakeholder identification                           │
│     └── Test plan drafting                                   │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  🔐 AuditBridge Integration (cmg/src/audit_bridge.py)      │
│     └── GovernanceReceipt.semantic_fingerprint              │
│         (16-char SHA256 tag for deduplication)              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Features

### 1. Semantic Retrieval

**Purpose**: Find relevant code/docs by meaning, not just keywords

```python
retriever = SemanticRetriever(Path(".cmg/index"))

# Natural language queries
results = retriever.query("differential privacy epsilon budget")

# Filter by type
policies = retriever.query("rate limiting", kind_filter=["policy"])
tests = retriever.query("anomaly detection", kind_filter=["test"])

# Get stats
stats = retriever.get_stats()
# -> {'total_records': 2001, 'model': '...', 'kinds': {...}}
```

### 2. Duplicate Detection

**Purpose**: Prevent redundant proposals by semantic similarity

```python
analyzer = Log4Analyzer(Path(".cmg/index"))

duplicates = analyzer.find_duplicates(
    "Add API throttling with 100 req/min limit",
    threshold=0.80,  # 80% similarity
    k=5
)

if duplicates:
    print(f"⚠️  Found {len(duplicates)} similar proposals")
    for dup in duplicates:
        print(f"  - {dup['path']} (score={dup['score']:.3f})")
```

### 3. Log⁴ Multi-Scale Analysis

**Purpose**: Analyze at 4 granularity levels before writing code

```python
brief = analyzer.analyze("improve telemetry aggregation", k=12)

# Level 1: System-wide (what's relevant?)
print(f"Top findings: {len(brief.top_findings)}")

# Level 2: Subsystem (policies, docs, tests, schemas)
for kind, hits in brief.neighbors_by_kind.items():
    print(f"  {kind}: {len(hits)} matches")

# Level 3: Module (drilldown into specific paths)
print(f"Module hits: {len(brief.module_drilldown)}")

# Level 4: Function (keywords + semantic clusters)
print(f"Keywords: {brief.keywords[:8]}")
print(f"Clusters: {len(brief.semantic_clusters)}")
```

### 4. Policy Blueprint Generation

**Purpose**: Auto-generate test plan + acceptance criteria from semantic analysis

```python
generator = BlueprintGenerator(Path(".cmg/index"))
blueprint = generator.generate("Add circuit breaker pattern", run_simulations=True)

# Prior art (files to review)
print(blueprint.prior_art)  # -> ['src/...', 'tests/...']

# Test plan
print(blueprint.simulation_scenarios)  # -> [BASELINE, ADVERSARIAL, DEGRADED]
print(blueprint.expected_impacts)  # -> {'baseline': {'latency_delta_ms': ...}}

# Acceptance criteria
print(blueprint.acceptance_criteria)
# -> ['All existing tests pass', 'No regression', ...]

# Risk assessment
print(blueprint.risk_factors)  # -> ['Breaking changes detected', ...]
print(blueprint.mitigation_strategies)  # -> ['Feature flag', 'Rollback plan', ...]

# Stakeholders
print(blueprint.stakeholder_groups)  # -> ['DEVELOPERS', 'OPERATIONS', ...]

# Save for review
path = generator.save_blueprint(blueprint)
```

### 5. Semantic Fingerprints

**Purpose**: Stable 16-char tags for receipts to enable fast deduplication heuristics

```python
from cmg.src.embeddings import semantic_fingerprint

text1 = "Implement DP with epsilon=1.0"
text2 = "Add privacy protection via DP epsilon 1.0"

fp1 = semantic_fingerprint(text1)  # -> '36a41b80bc88986f'
fp2 = semantic_fingerprint(text2)  # -> 'ad45333f083514a1'

# Different fingerprints = distinct proposals
# Same fingerprint = exact duplicate (rare, but fast to check)
```

### 6. AuditBridge Integration

**Purpose**: Tag all governance receipts with semantic fingerprints

```python
from cmg.src.audit_bridge import AuditBridge, SEADAttestation

bridge = AuditBridge("audit.log")

# Create receipt (automatically gets semantic_fingerprint)
receipt = bridge.create_receipt(
    policy_content={"max_requests": 100},
    action="propose",
    actor="test_user",
    justification="Prevent API abuse",
    risk_class="MEDIUM",
    sead_attestation=SEADAttestation(True, True, True, True, True, True, True)
)

print(receipt.semantic_fingerprint)  # -> 'bfb65bf9d42c4000'

# Later: query for similar receipts
analyzer = Log4Analyzer(Path(".cmg/index"))
similar = analyzer.find_duplicates(receipt.justification, threshold=0.75)
```

## Governance Integration

### Before Code is Written

```python
# 1. User submits goal
goal = "Add rate limiting to API gateway"

# 2. Generate design brief
analyzer = Log4Analyzer(Path(".cmg/index"))
brief = analyzer.analyze(goal, k=16)

# 3. Check for duplicates
duplicates = analyzer.find_duplicates(goal, threshold=0.75, k=5)
if duplicates:
    print("⚠️  Similar work exists:")
    for dup in duplicates[:3]:
        print(f"  - {dup['path']} (score={dup['score']:.3f})")
    # Decision: Link to prior work OR justify why this is different

# 4. Generate blueprint
generator = BlueprintGenerator(Path(".cmg/index"))
blueprint = generator.generate(goal, run_simulations=True)

# 5. Human reviews blueprint
# 6. IF approved -> create proposal via PolicyEngine
# 7. IF proposal passes governance -> implement
```

### During Voting

```python
# When stakeholders vote, show them:
# - brief.top_findings (prior art)
# - brief.semantic_clusters (affected subsystems)
# - blueprint.risk_factors (what could go wrong)
# - blueprint.similar_proposals (has this been tried before?)

# This enables informed voting without reading 10K lines of code
```

### After Implementation

```python
# Rebuild index to include new code
# (run this nightly or after large merges)
import subprocess
subprocess.run(["python", "tools/cmg_build_index.py", "--out", ".cmg/index"])
```

## Configuration

### Environment Variables

```bash
# Model selection (default: all-MiniLM-L6-v2)
export CMG_EMBED_MODEL="sentence-transformers/all-MiniLM-L6-v2"
# Alternative (slower, more accurate):
# export CMG_EMBED_MODEL="BAAI/bge-large-en-v1.5"

# Index location (default: .cmg/index)
export CMG_INDEX_DIR=".cmg/index"
```

### Customization

**Chunk size** (in `tools/cmg_build_index.py`):
```python
CHUNK_CHARS = 1200      # Characters per chunk
CHUNK_OVERLAP = 200     # Overlap for context continuity
```

**File types** (in `tools/cmg_build_index.py`):
```python
INCLUDE_EXT = {".py", ".md", ".yaml", ".yml", ".json", ".txt"}
EXCLUDE_DIRS = {".git", ".venv", "__pycache__", ".cmg"}
```

**Similarity thresholds**:
```python
# Duplicate detection (0.0-1.0, higher = stricter)
duplicates = analyzer.find_duplicates(text, threshold=0.80)

# Similar = 0.70-0.80
# Likely duplicate = 0.80-0.90
# Exact duplicate = 0.90+
```

## Performance

**Index build time**: ~10 seconds for 286 files (2001 chunks)  
**Query latency**: <100ms for top-8 results  
**Memory usage**: ~200MB (index + model)  
**Disk space**: ~2MB for index  

**Scaling**:
- 10K files: ~30 seconds to build, ~150ms queries
- 100K files: Consider switching to FAISS IVF index

## Privacy & Security

### PII Redaction

The index builder automatically redacts:
- Email addresses → `[redacted-email]`
- IP addresses → `[redacted-ip]`
- API keys → `token=[redacted]`

**IMPORTANT**: Embeddings are derived data. Apply the same retention policy as your telemetry.

### No Cloud Dependency

All processing is **100% local**:
- Model: Downloaded once to `~/.cache/torch/sentence_transformers/`
- Index: Stored in `.cmg/index/`
- No API calls, no telemetry sent

### Regional Storage

If syncing across regions, put `.cmg/index/` under appropriate data governance.

## Troubleshooting

### "Vector index not found"

```bash
# Build the index first
python tools/cmg_build_index.py --out .cmg/index
```

### "ModuleNotFoundError: sentence_transformers"

```bash
# Install dependencies
pip install sentence-transformers faiss-cpu scikit-learn rich tqdm
```

### "FAISS IndexFlatIP dimension mismatch"

```bash
# Rebuild index (model dimension changed)
rm -rf .cmg/index
python tools/cmg_build_index.py --out .cmg/index
```

### Slow queries

```python
# Reduce k (number of results)
results = retriever.query("...", k=5)  # instead of k=50

# Or upgrade to FAISS IVF index for large codebases
```

## Testing

Run comprehensive integration test:

```bash
python tests/test_cmg_embeddings.py
```

**Expected output**:
```
✅ All 8 tests passed successfully!
🧠 CMG LOG⁴ BRAIN: OPERATIONAL ✅
```

Tests cover:
1. Semantic retrieval (2001 chunks)
2. Log⁴ multi-scale analysis (4 levels)
3. Duplicate detection
4. Semantic fingerprints
5. Policy blueprint generation
6. AuditBridge integration
7. Policy deduplication
8. Prior art retrieval

## Maintenance

### Rebuild Schedule

- **After large merges**: Immediately
- **Nightly**: Recommended for active repos
- **Weekly**: Minimum for stable repos

```bash
# Cron job example (Linux/Mac)
0 2 * * * cd /path/to/axiom-x && python tools/cmg_build_index.py --out .cmg/index
```

### Index Invalidation

Rebuild if:
- ✓ New modules added
- ✓ Major refactoring
- ✓ Policy changes
- ✓ Model upgrade

No rebuild needed for:
- ✗ Small bug fixes
- ✗ Comment changes
- ✗ Test updates (unless semantic meaning shifts)

## Next Steps

### Incremental Upgrades

1. **Policy blueprint generator enhancements**:
   - Auto-draft test code (not just test plan)
   - Generate SQL migrations from schema changes
   - Predict approval probability from similar votes

2. **Integration with sprint_runner.py**:
   - Call `Log4Analyzer.analyze()` before planning stage
   - Pass `brief.top_findings` as context to AI planner
   - Auto-link prior art in sprint tickets

3. **Voter assistance UI**:
   - Show `brief.semantic_clusters` as visual graph
   - Highlight `blueprint.risk_factors` with color coding
   - Display `similar_proposals` with diff view

4. **Model upgrades**:
   - Switch to `BAAI/bge-large-en-v1.5` for +10% accuracy
   - Fine-tune on your codebase for +20% accuracy
   - Add multilingual support for global teams

## References

- **FAISS**: https://github.com/facebookresearch/faiss
- **Sentence Transformers**: https://www.sbert.net/
- **Model card**: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- **CMG Constitution**: `cmg/CMG_CONSTITUTION.md`

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: 2025-10-21  
**Maintained by**: AXIOM-X Team
