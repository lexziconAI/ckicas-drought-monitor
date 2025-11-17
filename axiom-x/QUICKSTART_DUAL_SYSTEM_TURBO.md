# AXIOM-X DUAL-SYSTEM TURBO MODE - QUICKSTART

**Launch Time:** < 5 minutes  
**Complexity:** Moderate  
**Requirements:** 16+ cores, 24GB+ RAM, API keys

---

## 🚀 ULTRA-QUICK START (3 Commands)

```bash
# Terminal 1: Infrastructure Workers
python spawn_infrastructure_workers.py

# Terminal 2: Phase 2 Validation
python phase2_swarm_coordinator.py

# Terminal 3: Monitor
python dual_system_monitor.py
```

**Expected Result:** 2,894 agents running, 4.5 minute completion

---

## 📋 PREREQUISITES

### 1. API Keys (`.env` file)
```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-proj-...
GOOGLE_API_KEY=AIza...
GROQ_API_KEY=gsk_...
COHERE_API_KEY=...
FIREWORKS_API_KEY=...
```

### 2. System Check
```bash
# Verify hardware
python -c "import psutil; print(f'Cores: {psutil.cpu_count()}, RAM: {psutil.virtual_memory().total / 1024**3:.1f}GB')"

# Should show: Cores: 16+ , RAM: 24GB+
```

---

## 🎯 CONFIGURATION PROFILES

### Profile 1: MAXIMUM SPEED (Default)
```python
# phase2_swarm_coordinator.py
BATCH_SIZE = 400
MAX_CONCURRENT = 400

# spawn_infrastructure_workers.py
MAX_INFRASTRUCTURE_WORKERS = 100
```

**Best for:** Fastest completion, max CPU usage (80-95%)

---

### Profile 2: CONSERVATIVE (Lower Resource Usage)
```python
# phase2_swarm_coordinator.py
BATCH_SIZE = 200
MAX_CONCURRENT = 200

# spawn_infrastructure_workers.py
MAX_INFRASTRUCTURE_WORKERS = 50
```

**Best for:** Running alongside other applications, 50-70% CPU

---

### Profile 3: EXTREME (Experimental - 32+ cores only)
```python
# phase2_swarm_coordinator.py
BATCH_SIZE = 600
MAX_CONCURRENT = 600

# spawn_infrastructure_workers.py
MAX_INFRASTRUCTURE_WORKERS = 150
```

**Best for:** High-end workstations, 95%+ CPU, <3 min completion

---

## 📊 EXPECTED OUTPUTS

**Phase 2 (4-5 minutes):**
- ✅ `canonical_files_map.yaml` - Master system brain
- ✅ `redundant_files_list.json` - Safe deletion plan
- ✅ `performance_timeline.json` - Breakthrough history

**Infrastructure (Continuous):**
- ✅ 60-100 new feature files
- ✅ Architecture designs
- ✅ Test suites

---

## ⚠️ TROUBLESHOOTING

### Problem: CPU at 100%, system lagging

**Solution:** Reduce batch sizes
```python
BATCH_SIZE = 200  # Down from 400
MAX_INFRASTRUCTURE_WORKERS = 50  # Down from 100
```

### Problem: Out of memory

**Solution:** Close other applications, reduce workers
```python
MAX_INFRASTRUCTURE_WORKERS = 50
```

### Problem: Provider rate limits

**Solution:** Already handled! 2-second delays built-in. Just wait.

---

## 📈 VALIDATION

**Check it's working:**
```bash
# Watch progress
tail -f phase2_output.log

# Monitor resources
python dual_system_monitor.py
```

**Good signs:**
- ✅ CPU 70-90%
- ✅ "Completed batch X" every 60-90 seconds
- ✅ Task counts increasing

---

## 📚 LEARN MORE

- Full documentation: `AXIOM_X_TURBO_MODE_SNAPSHOT_2024_11_09.md`
- Architecture details: `canonical_files_map.yaml` (after completion)
- Research context: University of Auckland PhD dissertation (in progress)

---

END QUICKSTART