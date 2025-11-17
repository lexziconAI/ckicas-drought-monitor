# 📦 ARCHIVE: Outdated Documentation

This folder contains documentation that has been superseded by more accurate information.

## Files in This Archive

### 1. LATEST_MODELS_PROVIDER_STATUS_NOV2025.md
**Status**: ❌ OUTDATED - Referenced incorrect models  
**Reason for Archival**:
- Listed `gpt-4-turbo` (deprecated - should be `gpt-5`)
- Listed `claude-opus-4-1` (doesn't exist)
- Listed `claude-3.5-haiku` (wrong version - should be `claude-haiku-4-5-20251001`)

**Replaced by**:
- `CONSTITUTIONAL_MEMORY_MODEL_CONFIG_CORRECTED.md` - Authoritative model configuration

---

### 2. PROVIDER_SMOKE_TEST_RESULTS_14D.md
**Status**: ❌ OUTDATED - Based on incorrect model versions  
**Reason for Archival**:
- Referenced deprecated `gpt-4-turbo` in recommendations
- Did not include `claude-haiku-4-5-20251001` (the new preferred model)
- Based on incomplete provider testing

**Replaced by**:
- `optimized_provider_router.py` - Authoritative provider configuration with actual working models

---

## ✅ Authoritative Sources

Use these instead:

| Document | Purpose | Status |
|----------|---------|--------|
| `optimized_provider_router.py` | Provider model configuration | ✅ CURRENT |
| `CONSTITUTIONAL_MEMORY_MODEL_CONFIG_CORRECTED.md` | Model selection strategy | ✅ CURRENT |
| `multi_provider_integration_test_*.json` | Test results with actual APIs | ✅ CURRENT |
| `fixed_real_api_coordinator.py` | Working API integration | ✅ CURRENT |

---

## 🔍 What Changed

### Model Updates Applied
```
claude-3-5-haiku-20241022  ❌ OLD
claude-haiku-4-5-20251001  ✅ NEW - Haiku 4.5 (preferred)

gpt-4-turbo               ❌ OLD
gpt-5                     ✅ NEW - Latest GPT (primary)

claude-opus-4-1           ❌ DOESN'T EXIST
claude-sonnet-4-5-20250929 ✅ CURRENT - Sonnet 4.5
```

---

## 📝 Archive Date
November 6, 2025 14:30 UTC

## 🔄 Recovery
If you need these files for historical reference, they remain in this archive folder. Do NOT use them as source of truth.
