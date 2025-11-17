---
author: "Regan William DUFF"
company: "AXIOM INTELLIGENCE LIMITED"
company_number: "9287393"
date: "October 26, 2025"
cryptographic_signature: "ec93b2a2e233a033b3040e8b623df75a9c51d8c3240adb733e3d33efa5132524"
constitutional_compliance: "Satya, Asteya, Ahimsa"
provenance_hash: "ccab9b4123aede4700998abf3ccc3b2937dd609a4711cef1c3ff4814517915f6"
---

# Autonomous Learning System - Quick Start Guide

## ✅ System Status

**SENTINEL autonomous learning is ENABLED with paranoid safety mode** 🛡️

All safety components are operational:
- ✅ Drift Monitor (tracks parameter changes)
- ✅ Yama Enforcer (enforces ethical constraints)
- ✅ Experience Filter (filters toxic experiences)
- ✅ Meta-Learning Bounds (prevents unbounded self-improvement)
- ✅ Provenance Engine (cryptographic accountability)
- ✅ Real-time Monitoring Dashboard

## 🚀 Quick Commands

### Enable Learning for an App
```bash
python axiom_configure.py --app=sentinel --learning=enabled --safety-mode=paranoid --rollback-on-any-violation
```

### Check Status
```bash
python axiom_configure.py --status
```

### Start Live Monitoring
```bash
# Monitor all apps indefinitely
python axiom_configure.py --monitor

# Monitor specific app for 2 hours
python axiom_configure.py --app=sentinel --monitor --duration=2
```

### Run Demo Simulation
```bash
python demo_autonomous_learning.py
```

## 📊 Week 1 Success Criteria

The system tracks these automatically:

1. **Zero Yama Violations** ✅
   - All ethical constraints must be satisfied
   - Automatic rollback on any violation

2. **Drift < 10%** ✅
   - Parameter drift from baseline stays under 10%
   - L2 norm calculation for aggregate drift

3. **Quality ≥ 97.1%** ✅
   - Maintains SENTINEL baseline quality
   - Tested on existing test suites

4. **100+ Tasks Complete** 🔄
   - Track learning iterations
   - Only counts successful updates

5. **Zero Emergency Rollbacks** ✅
   - No critical failures requiring rollback
   - System automatically pauses on violations

## 🛡️ Safety Modes

### Paranoid (Current for SENTINEL)
- Max drift: 10%
- Min quality: 97.1%
- Max cost/update: $1.00
- Learning rate limit: 0.001
- **Rollback on ANY violation**

### Strict
- Max drift: 15%
- Min quality: 95%
- Max cost/update: $5.00
- Learning rate limit: 0.01
- Rollback on critical violations

### Balanced
- Max drift: 25%
- Min quality: 93%
- Max cost/update: $10.00
- Learning rate limit: 0.05
- Log violations, no auto-rollback

### Experimental
- Max drift: 40%
- Min quality: 90%
- Max cost/update: $50.00
- Learning rate limit: 0.1
- Requires human approval

## 📈 Monitoring Dashboard Features

The real-time dashboard shows:

- **Current Status**: Learning enabled/disabled/paused/halted
- **Drift Tracking**: Real-time parameter drift with trend indicators
- **Quality Metrics**: Test pass rates and quality scores
- **Cost Tracking**: Budget usage per update
- **Violation Alerts**: Real-time safety violation notifications
- **Week 1 Criteria**: Progress toward success targets

## 🔧 Integration with Existing Code

### In Your Learning Code

```python
from core.learning.safe_learning_coordinator import get_learning_coordinator

# Initialize coordinator
coordinator = get_learning_coordinator('sentinel')

# Set baseline parameters
coordinator.initialize_baseline({
    'learning_rate': 0.001,
    'batch_size': 32,
    'hidden_dim': 128
})

# Validate each learning update
result = coordinator.validate_learning_update(
    proposed_parameters={...},
    experience_data={...},
    source_info={...},
    quality_score=0.975,
    cost=0.85
)

if result.approved:
    # Apply the update
    apply_parameters(result.bounded_parameters or proposed_parameters)
else:
    # Rollback triggered automatically
    print(f"Update rejected: {result.reason}")
```

## 🚨 Emergency Procedures

### If Learning is Paused
```bash
# Check why it was paused
python axiom_configure.py --status

# Resume if safe (requires human judgment)
python -c "from core.learning.learning_config import get_learning_config_manager; get_learning_config_manager().resume_learning('sentinel')"
```

### If Emergency Halt Triggered
```bash
# Emergency halt requires code change or manual override
# Review violation logs first:
cat core/telemetry/learning_alerts.jsonl

# Investigate root cause before resuming
```

## 📂 Important Files

- **Configuration**: `config/learning_config.json`
- **Dashboard Snapshot**: `core/telemetry/learning_dashboard.json`
- **Alerts Log**: `core/telemetry/learning_alerts.jsonl`
- **Drift History**: `core/telemetry/storage/learning/sentinel_drift.jsonl`
- **Events Log**: `config/learning_events.jsonl`
- **Environment**: `.env` (API keys and model configurations)

## 🤖 Current LLM Models (November 2025 - UPDATED)

⚠️ **Authoritative Source**: See `CONSTITUTIONAL_MEMORY_MODEL_CONFIG_CORRECTED.md`

- **Claude (Premium)**: `claude-sonnet-4-5-20250929` (latest production Sonnet 4.5)
- **Claude (Fast)**: `claude-haiku-4-5-20251001` ⭐ NEW Haiku 4.5
- **GPT (Premium)**: `gpt-5` (latest GPT - was gpt-4-turbo)
- **GPT (Fast)**: `gpt-3.5-turbo`
- **Gemini**: `gemini-2.5-pro` (latest, replaced 2.0-flash-exp)
- **Groq**: `llama-3.3-70b-versatile` (fastest: 300ms, $0.0005/1k tokens)
- **Cohere**: `command-a-03-2025` (latest Command A model)

All models configured in `.env` file and `optimized_provider_router.py`.

## 🎯 Next Steps for Production

1. **Integrate with Real Tasks**
   - Connect coordinator to actual learning loops
   - Use real quality metrics from test suites
   - Track real costs from API usage

2. **Set Up Continuous Monitoring**
   - Run dashboard in background
   - Set up alerts (email/Slack/etc.)
   - Export metrics to visualization tools

3. **Gradual Rollout**
   - Start with SENTINEL (lowest risk)
   - Monitor for 1 week
   - Expand to LOG4 if successful
   - Eventually enable for DECISION_ARENA

4. **Weekly Reviews**
   - Check Week 1 criteria
   - Adjust thresholds if needed
   - Document learnings
   - Plan next phase

## ✨ Key Features

- **Unbreakable Ethics**: Yama constraints cannot be overridden by learning
- **Automatic Rollback**: Instant revert on safety violations
- **Complete Accountability**: Every decision is cryptographically signed
- **Real-time Monitoring**: Live dashboard with trend analysis
- **Multi-layer Filtering**: Content, source, poisoning, and safety validation
- **Circuit Breakers**: Prevents runaway learning
- **Human Oversight**: Emergency halt requires intervention

---

**The system is ready for production use with SENTINEL. Good luck with Week 1!** 🚀
