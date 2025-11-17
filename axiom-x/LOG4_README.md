---
author: "Regan William DUFF"
company: "AXIOM INTELLIGENCE LIMITED"
company_number: "9287393"
date: "October 26, 2025"
cryptographic_signature: "f608d0ec64524206e5ecca16d69888d9940ea37320990d7197cf360d4fe4b179"
constitutional_compliance: "Satya, Asteya, Ahimsa"
provenance_hash: "b3a4cb2328d035948d9f797e17080c285cac6cb501cb742c44a4ca85088c00d2"
---

# AXIOM-X LOG⁴ Framework

**Version:** 8.1.0-log4  
**Status:** Patch-only upgrade with cross-platform support

## Overview

LOG⁴ is a comprehensive structural-antifragility framework that extends LOG³ with:

- **Cross-platform file locking** (Windows/POSIX)
- **Multi-resource budget envelopes** ($/kWh/CO₂/tokens/time)
- **Circuit breakers** for fault tolerance
- **Proof-of-capacity system** with reputation tracking
- **Just-in-time verification** and allocation
- **Chaos engineering** tools for testing
- **Tamper-evident audit logs** with HMAC signatures

## Architecture

```
src/axiom/
├── core/               # Transactional I/O with cross-platform locks
│   ├── transactional_io.py
│   └── __init__.py
├── integrity/          # Cross-platform locking
│   ├── lockshim.py
│   └── __init__.py
├── proof/              # Resource envelopes and proof runners
│   ├── resource_envelope.py
│   ├── runner_integration.py
│   ├── runner.py
│   └── __init__.py
├── storage/            # Coordination, compression, autosave
│   ├── coordination.py
│   ├── compression.py
│   ├── autosave.py
│   └── __init__.py
├── capacity/           # Proof-of-capacity system
│   ├── proof_system.py
│   ├── verification.py
│   └── __init__.py
└── testing/            # Integrity harness and chaos injection
    ├── integrity_harness.py
    ├── integrity_audit.py
    └── __init__.py
```

## Key Features

### 1. Cross-Platform Locking (`axiom.integrity.lockshim`)

Provides unified advisory file locking:
- **Windows:** `msvcrt.locking()` with retry logic
- **POSIX:** `fcntl.flock()` with exclusive/shared modes
- **Fallback:** PID-based `.lock` files

```python
from axiom.integrity import file_lock

with file_lock("/path/to/file.txt", exclusive=True):
    # Protected file operations
    pass
```

### 2. Transactional I/O (`axiom.core.transactional_io`)

Enhanced atomic file operations:
- Write to temp file in **same directory** (same volume for atomic rename)
- SHA256 verification before commit
- Automatic backup with rollback capability
- Advisory locks prevent concurrent writes

```python
from axiom.core import TransactionalWriter

writer = TransactionalWriter(backup_dir="backups")
result = writer.write_file(
    filepath="output.json",
    content='{"key": "value"}',
    min_lines=1
)
```

### 3. Resource Envelopes (`axiom.proof.resource_envelope`)

Multi-resource budget tracking with graceful degradation:

```python
from axiom.proof import ResourceEnvelope, ResourceType

envelope = ResourceEnvelope({
    ResourceType.COST_USD: 10.0,
    ResourceType.TOKENS: 100000,
    ResourceType.ENERGY_KWH: 5.0
})

# Reserve resources
envelope.reserve_resources({
    ResourceType.COST_USD: 0.5,
    ResourceType.TOKENS: 5000
})

# Consume from reserved
envelope.consume_resources({
    ResourceType.COST_USD: 0.5,
    ResourceType.TOKENS: 5000
}, from_reserved=True)

# Check degradation
print(envelope.degradation_level)  # OPTIMAL, REDUCED, MINIMAL, or EMERGENCY
```

### 4. Circuit Breakers (`axiom.proof.runner_integration`)

Fault-tolerant operation execution:

```python
from axiom.proof import ResourceEnvelope, ResourceType
from axiom.proof.runner_integration import ProofRunner

envelope = ResourceEnvelope({ResourceType.COST_USD: 10.0})
runner = ProofRunner(envelope)

runner.register_circuit_breaker("my_op", failure_threshold=5, timeout_sec=60)

def risky_operation():
    # Your code here
    return "success"

result = runner.execute_with_protection(
    operation_name="my_op",
    operation=risky_operation,
    resource_cost={ResourceType.COST_USD: 0.1},
    circuit_breaker="my_op"
)
```

### 5. Storage Coordination (`axiom.storage`)

Intent locks prevent conflicting operations:

```python
from axiom.storage import Coordinator, SnapshotCompressor, AutosaveManager

coordinator = Coordinator()
coordinator.start_watchdog()

# Compression won't proceed if writes are active
compressor = SnapshotCompressor(
    source_dir="data",
    output_dir="snapshots",
    coordinator=coordinator
)

result = compressor.compress(snapshot_id="backup_001")

# Autosave respects compression windows
autosave = AutosaveManager(coordinator, interval_sec=120)
autosave.register_callback("data_save", lambda: {"status": "ok"})
autosave.start()
```

### 6. Capacity Proof System (`axiom.capacity`)

Cryptographic proof-of-capacity with reputation:

```python
from axiom.capacity import CapacityProofSystem, JITVerifier
from axiom.capacity.verification import AllocationRequest

# Create proof system
proof_system = CapacityProofSystem(difficulty_target=4)

# Provider commits capacity
commitment = proof_system.create_commitment(
    provider_id="worker_001",
    resource_type="compute",
    capacity_units=100.0,
    duration_sec=3600.0
)

# Issue challenge
challenge = proof_system.issue_challenge(commitment.commitment_id)

# Provider solves challenge (proof-of-work)
# ... provider computes solution ...

# Verify response
is_valid = proof_system.verify_response(
    challenge.challenge_id,
    "worker_001",
    solution
)

# JIT allocation with reputation-based degradation
verifier = JITVerifier(proof_system)
request = AllocationRequest(
    request_id="req_1",
    provider_id="worker_001",
    resource_type="compute",
    requested_units=50.0
)

allocation = verifier.request_allocation(request)
# Allocation adjusted based on provider reputation
```

### 7. Testing Harness (`axiom.testing`)

Chaos injection and tamper-evident auditing:

```python
from axiom.testing import IntegrityAuditLog, ChaosInjector, isolated_test_env

# Tamper-evident audit log
audit_log = IntegrityAuditLog("audit.json")
audit_log.append("write", {"file": "data.json", "size": 1024})
verification = audit_log.verify()  # Check HMAC signatures

# Chaos injection for testing
chaos = ChaosInjector(failure_rate=0.1, latency_ms_range=(10, 50))

if chaos.maybe_inject_failure("db_write"):
    raise RuntimeError("Chaos: Simulated failure")

chaos.maybe_inject_latency("api_call")

# Isolated test environment
with isolated_test_env("my_test") as test_dir:
    # test_dir is auto-cleaned up
    (test_dir / "test.txt").write_text("test")
```

## Installation

### Requirements

```bash
pip install -r requirements-dev.txt
```

**Development Dependencies:**
- pytest >= 7.0.0
- hypothesis >= 6.0.0
- typing_extensions >= 4.0.0
- pytest-asyncio >= 0.21.0
- pytest-cov >= 4.0.0

### Environment Setup

Set `PYTHONPATH` to include `src/`:

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "$PWD\src"
```

**Linux/macOS:**
```bash
export PYTHONPATH="$PWD/src"
```

### Security Configuration

Set HMAC key for audit logs:

```powershell
$env:AXIOM_AUDIT_KEY = "your-secure-key-here"
```

**⚠️ Important:** Use a strong random key in production, not the default `dev_not_secure`.

## Testing

### Run All Tests

```bash
python run_tests.py
```

Or directly with pytest:

```bash
pytest tests/ -v
```

### Test Coverage

- `tests/test_transactional_io.py` - Cross-platform I/O
- `tests/test_runner_integration.py` - Resource envelopes & circuit breakers
- `tests/test_coordination_autosave_compression.py` - Storage coordination
- `tests/test_integrity_harness.py` - Audit logs & chaos injection
- `tests/test_capacity_system.py` - Proof-of-capacity & JIT verification

### Test Isolation

All tests use temporary directories and clean up automatically:

```python
def test_example():
    with isolated_test_env("my_test") as test_dir:
        # Test code here
        pass
    # test_dir cleaned up automatically
```

## VS Code Configuration

### Recommended Settings

Add to `.vscode/settings.json`:

```json
{
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 120000,
  "python.analysis.extraPaths": ["src"],
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"]
}
```

### Avoid Cloud Sync

**Important:** Place `output_dir` and telemetry directories **outside** OneDrive/cloud sync folders to prevent conflicts:

```python
compressor = SnapshotCompressor(
    source_dir="data",
    output_dir="C:/local/snapshots",  # Local path, not synced
    coordinator=coordinator
)
```

## Architecture Notes

### Same-Volume Atomic Rename

`TransactionalWriter` creates temp files in the **same directory** as the target:

```python
def _write_temp_file(self, content: bytes, target_dir: Path) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(
        suffix='.tmp',
        prefix='axiomx_',
        dir=str(target_dir)  # Same volume as target
    )
```

This ensures `os.replace()` is atomic (no cross-filesystem issues).

### Intent Lock Conflicts

Conflict matrix:

| Intent Type | Conflicts With |
|-------------|---------------|
| READ        | *(none)* |
| WRITE       | COMPRESS, BACKUP |
| COMPRESS    | WRITE, BACKUP |
| BACKUP      | WRITE, COMPRESS |

### Degradation Levels

Resource utilization triggers:

| Level | Threshold | Behavior |
|-------|-----------|----------|
| OPTIMAL | < 70% | Full capacity |
| REDUCED | 70-85% | Reduce workload |
| MINIMAL | 85-95% | Critical operations only |
| EMERGENCY | >= 95% | Halt non-essential operations |

### Reputation Levels

Capacity provider reputation:

| Level | Requirements | Degradation Factor |
|-------|-------------|-------------------|
| UNTRUSTED | < 10 proofs | 0.5 (50% capacity) |
| PROBATION | 10+ proofs, 80%+ success | 0.7 |
| TRUSTED | 50+ proofs, 95%+ success | 0.9 |
| VERIFIED | 100+ proofs, 99%+ success | 1.0 (full capacity) |

## Migration from LOG³

LOG⁴ is a **patch-only upgrade** - existing LOG³ code continues to work:

### Before (LOG³)

```python
from src.integrity.transactional_writer import TransactionalWriter
writer = TransactionalWriter()
```

### After (LOG⁴)

```python
from axiom.core import TransactionalWriter
writer = TransactionalWriter()  # Same API, enhanced internals
```

### Key Changes

1. **Import paths:** `src.integrity.*` → `axiom.core.*`
2. **Error types:** `IntegrityError` → `TransactionError` (base), `IntegrityError` (subclass)
3. **Locking:** Automatic (no code changes needed)
4. **Same-volume constraint:** Temp files now in target directory (was in system temp)

## Performance Considerations

### Proof-of-Work Difficulty

Default `difficulty_target=4` means ~16 attempts on average. Adjust based on hardware:

- **Testing:** `difficulty_target=2` (fast)
- **Development:** `difficulty_target=4` (balanced)
- **Production:** `difficulty_target=6` (secure)

### Compression Size Limits

Default `max_archive_size=1GB`. For laptops/testing, use smaller limits:

```python
compressor = SnapshotCompressor(
    source_dir="data",
    output_dir="snapshots",
    max_archive_size=100 * 1024 * 1024  # 100MB
)
```

### Autosave Intervals

Default `interval_sec=120` (2 minutes). Adjust based on workload:

- **Fast iteration:** 60s
- **Production:** 300s (5 minutes)
- **Low-priority:** 600s (10 minutes)

## Troubleshooting

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'axiom'`

**Solution:** Set `PYTHONPATH`:

```powershell
$env:PYTHONPATH = "$PWD\src"
```

### Lock Timeout

**Error:** `Circuit breaker 'io_operations' is open`

**Solution:** Increase timeout or reduce concurrent operations:

```python
runner.register_circuit_breaker(
    "io_operations",
    failure_threshold=10,  # Increase threshold
    timeout_sec=120.0      # Longer timeout
)
```

### Compression Fails

**Error:** `CompressionError: Cannot acquire compression lock - conflicting operations`

**Solution:** Release write intents before compression:

```python
coordinator.release_intent(write_intent_id)
time.sleep(0.1)  # Brief pause
compressor.compress()
```

### Audit Log Tampering

**Error:** `verification['valid'] == False`

**Solution:** Check `AXIOM_AUDIT_KEY` environment variable and regenerate log:

```python
import os
os.environ["AXIOM_AUDIT_KEY"] = "new-secure-key"
audit_log = IntegrityAuditLog("audit_new.json")
```

## Contributing

### Adding New Modules

1. Create module in appropriate `src/axiom/` subdirectory
2. Add to `__init__.py` exports
3. Create tests in `tests/test_<module>.py`
4. Update this README with examples
5. Run full test suite: `python run_tests.py`

### Code Style

- **Docstrings:** Google-style with Args/Returns/Raises
- **Type hints:** Use `typing` module annotations
- **Error handling:** Raise specific exceptions (e.g., `TransactionError`)
- **Logging:** Use `telemetry` dicts, not print statements

## License

Part of AXIOM-X project. See main repository for license.

## Version History

- **v8.1.0-log4** (2025-10-21): Initial LOG⁴ release with cross-platform support
- **v8.1.0-log3** (2025-10-20): LOG³ structural-antifragility baseline
- **v8.0.0** (2025-10): Core v8 features (mode mapping, W2 scheduler, budgets)

---

**Note:** This is a **patch-only** upgrade. No breaking changes to existing LOG³ code.
