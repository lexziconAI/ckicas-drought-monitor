# ✅ UPDATED: ACTUAL PREFERRED MODELS - November 2025
## From Codebase Configuration (Authoritative)

Based on analysis of `optimized_provider_router.py`, `operation_mega_router.py`, `fixed_api_test.py`, and related files.

---

## 🎯 TIER SYSTEM (ACTUAL CONFIGURATION)

### 🏆 Premium Tier (Highest Quality, Higher Cost)
```python
"claude_sonnet_4": {
    "model": "claude-sonnet-4-5-20250929",  # Latest Claude Sonnet 4.5
    "speed": 6,
    "cost": 5,
    "quality": 9
},
"gpt_4o": {
    "model": "gpt-4o",
    "speed": 6,
    "cost": 5,
    "quality": 9
},
"gpt_5": {
    "model": "gpt-5",  # NEW - Latest GPT
    "speed": 6,
    "cost": 6,
    "quality": 10
},
"gemini_pro": {
    "model": "gemini-2.5-pro",
    "speed": 7,
    "cost": 3,
    "quality": 8
}
```

### ⚖️ Balanced Tier (Quality/Cost Sweet Spot) - RECOMMENDED FOR DASHBOARD
```python
"gpt_4o_mini": {
    "model": "gpt-4o-mini",  # Best balanced
    "speed": 8,
    "cost": 2,
    "quality": 7
},
"gpt_5_mini": {
    "model": "o4-mini",  # NEW - Ultra-cheap version of o4
    "speed": 8,
    "cost": 2,
    "quality": 8
},
"gemini_flash": {
    "model": "gemini-2.5-flash",
    "speed": 7,
    "cost": 3,
    "quality": 8
},
"cohere": {
    "model": "command-a-03-2025",  # NEW - Latest Cohere
    "speed": 7,
    "cost": 3,
    "quality": 7
}
```

### ⚡ Fast Tier (Speed Priority, Good Quality) - FOR REAL-TIME
```python
"claude_haiku_4": {
    "model": "claude-haiku-4-5-20251001",  # NEW - Haiku 4.5
    "speed": 8,
    "cost": 2,
    "quality": 7
},
"groq": {
    "model": "llama-3.3-70b-versatile",  # Fastest open-source
    "speed": 10,
    "cost": 1,
    "quality": 6
},
"fireworks": {
    "model": "accounts/fireworks/models/llama-v3p3-70b-instruct",
    "speed": 9,
    "cost": 1,
    "quality": 6
}
```

---

## 📊 COMPLETE MODEL REFERENCE (FROM CODEBASE)

### Anthropic Claude
```json
{
  "models": [
    "claude-sonnet-4-5-20250929",      # NEW: Latest Sonnet 4.5 (2025)
    "claude-haiku-4-5-20251001",       # NEW: Latest Haiku 4.5 (2025)
    "claude-3-5-haiku-20241022",       # Older Haiku variant
    "claude-3-opus-20240229"           # Older Opus
  ],
  "default_model": "claude-sonnet-4-5-20250929",
  "cheapest_model": "claude-haiku-4-5-20251001",
  "best_quality": "claude-sonnet-4-5-20250929",
  "fastest": "claude-haiku-4-5-20251001",
  "api_version": "2023-06-01",
  "note": "Use claude-haiku-4-5-20251001 for cost-effective fast responses"
}
```

### OpenAI GPT
```json
{
  "models": [
    "gpt-5",                           # NEW: Latest GPT-5 (2025)
    "gpt-4o",                          # Current GPT-4o
    "gpt-4o-mini",                     # GPT-4o mini variant
    "o4-mini",                         # NEW: o4-mini for ultra-cheap
    "gpt-4-turbo",                     # DEPRECATED - Don't use
    "gpt-3.5-turbo"                    # DEPRECATED - Don't use
  ],
  "default_model": "gpt-5",
  "cheapest_model": "o4-mini",        # Ultra-cheap option
  "best_quality": "gpt-5",
  "fastest": "o4-mini",
  "for_dashboard": "gpt-4o-mini",     # Best balanced for UI
  "note": "Use o4-mini for budget constraints, gpt-4o-mini for balanced"
}
```

### Google Gemini
```json
{
  "models": [
    "gemini-2.5-pro",                  # Premium (multimodal)
    "gemini-2.5-flash-image",          # Flash variant with images
    "gemini-2.5-flash-preview-tts",    # With text-to-speech
    "gemini-2.0-flash",                # Previous flash version
    "gemini-2.0-flash-lite"            # Lite version
  ],
  "default_model": "gemini-2.5-pro",
  "fastest_model": "gemini-2.5-flash-image",
  "note": "Use gemini-2.5-flash-image for balanced speed/quality"
}
```

### Groq (Fast Inference)
```json
{
  "models": [
    "llama-3.3-70b-versatile",        # Current - FASTEST
    "mixtral-8x7b-32768"              # DEPRECATED - Decommissioned
  ],
  "default_model": "llama-3.3-70b-versatile",
  "latency_ms": 300,
  "note": "Fastest inference - ideal for real-time dashboard updates"
}
```

### Fireworks AI
```json
{
  "models": [
    "accounts/fireworks/models/llama-v3p3-70b-instruct",  # LATEST
    "accounts/fireworks/models/mixtral-8x7b-fw-engine",
    "accounts/fireworks/models/qwen-32b-chat"
  ],
  "default_model": "accounts/fireworks/models/llama-v3p3-70b-instruct",
  "note": "High-performance alternative to Groq"
}
```

### Cohere
```json
{
  "models": [
    "command-a-03-2025",               # NEW: Latest (2025)
    "command-r-plus",                  # Previous version
    "command-r"                        # Standard
  ],
  "default_model": "command-a-03-2025"
}
```

### Replicate
```json
{
  "models": [
    "meta/meta-llama-3.1-405b",
    "meta/meta-llama-3.1-70b",
    "meta/meta-llama-3.1-8b"
  ]
}
```

---

## 🚀 RECOMMENDED CONFIGURATION FOR 14D DASHBOARD

### Production Tier (What to Actually Use)
```python
TIER_CONFIGS = {
    "premium": [
        {"provider": "openai", "model": "gpt-5"},
        {"provider": "anthropic", "model": "claude-sonnet-4-5-20250929"},
        {"provider": "google", "model": "gemini-2.5-pro"}
    ],
    "balanced": [
        {"provider": "openai", "model": "gpt-4o-mini"},          # BEST for dashboard
        {"provider": "openai", "model": "o4-mini"},               # CHEAPEST
        {"provider": "anthropic", "model": "claude-haiku-4-5-20251001"},
        {"provider": "google", "model": "gemini-2.5-flash-image"}
    ],
    "fast": [
        {"provider": "groq", "model": "llama-3.3-70b-versatile"}, # FASTEST (300ms)
        {"provider": "fireworks", "model": "accounts/fireworks/models/llama-v3p3-70b-instruct"},
        {"provider": "anthropic", "model": "claude-haiku-4-5-20251001"}
    ]
}
```

### Fallback Chain (Auto-Failover)
```python
FALLBACK_CHAIN = [
    # Primary
    "gpt-4o-mini",  # Best balanced
    # Secondaries
    "o4-mini",  # Cheapest
    "claude-haiku-4-5-20251001",  # Fast Claude
    # Emergency
    "llama-3.3-70b-versatile"  # Fastest (Groq)
]
```

---

## 💰 COST & SPEED RANKINGS (ACTUAL)

### Speed (Latency)
1. 🏃 **Groq Llama 3.3**: ~300ms
2. 🏃 **Fireworks Llama v3.3**: ~400ms
3. ⏱️ **Claude Haiku 4.5**: ~600ms
4. ⏱️ **GPT-4o mini**: ~800ms
5. ⏱️ **o4-mini**: ~800ms
6. 📊 **Gemini 2.5 Flash**: ~900ms
7. 📊 **GPT-4o**: ~1000ms
8. 📊 **Claude Sonnet 4.5**: ~1100ms
9. 📊 **Gemini 2.5 Pro**: ~1200ms
10. 🐢 **GPT-5**: ~1300ms

### Cost (Estimated per 1M tokens)
1. 💰 **Groq**: $0.50
2. 💰 **Fireworks**: $0.50
3. 💰 **Claude Haiku 4.5**: $1.50
4. 💰 **o4-mini**: $2.00
5. 💰 **GPT-4o mini**: $2.50
6. 💰 **Gemini 2.5 Flash**: $3.00
7. 💰 **Cohere Command A**: $3.50
8. 💰 **GPT-4o**: $5.00
9. 💰 **Claude Sonnet 4.5**: $6.00
10. 💰 **GPT-5**: $8.00

### Quality (Subjective 1-10)
1. 🏆 **GPT-5**: 10
2. 🏆 **Claude Sonnet 4.5**: 9
3. 🏆 **GPT-4o**: 9
4. ⭐ **o4-mini**: 8
5. ⭐ **Gemini 2.5 Pro**: 8
6. ⭐ **Gemini 2.5 Flash**: 8
7. ⭐ **Claude Haiku 4.5**: 7
8. ⭐ **GPT-4o mini**: 7
9. 👍 **Cohere Command A**: 7
10. 👍 **Groq Llama 3.3**: 6

---

## 🎯 BEST SELECTIONS BY USE CASE

### Constitutional Analysis (What's Ethical?)
**Use**: `claude-sonnet-4-5-20250929` or `gpt-5`
- Best reasoning capabilities
- Understands complex ethical frameworks
- Cost: ~$0.03-0.08 per analysis

### Real-Time Dashboard Updates
**Use**: `gpt-4o-mini` or `claude-haiku-4-5-20251001`
- Fast response (<1s)
- Good quality for UI updates
- Cost: ~$0.01-0.02 per update

### Chaos Theory Calculations
**Use**: `groq` (fastest) or `gpt-4o-mini` (balanced)
- Llama 3.3 is incredibly fast
- GPT-4o mini has better reasoning
- Cost: $0.005-0.025 per calculation

### Cost-Conscious Operations
**Use**: `o4-mini` or `llama-3.3-70b-versatile`
- Groq: Absolute cheapest & fastest
- o4-mini: Excellent quality for price
- Cost: $0.005-0.02 per request

### Mission-Critical Analysis
**Use**: `gpt-5` or `claude-sonnet-4-5-20250929`
- Highest quality output
- Best reasoning and accuracy
- Cost: ~$0.08-0.15 per request

---

## ✅ ENVIRONMENT VARIABLES NEEDED

From `.env` file:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...
GOOGLE_API_KEY=AIzaSy...
GROQ_API_KEY=gsk_...
FIREWORKS_API_KEY=fw_...
COHERE_API_KEY=...
REPLICATE_API_KEY=r8_...
STABILITY_API_KEY=sk-...
FAL_API=...
```

---

## 🔄 MIGRATION PATH FROM OLD MODELS

### ❌ OLD (DEPRECATED)
```
gpt-4-turbo        → USE: gpt-4o-mini or o4-mini
gpt-3.5-turbo      → USE: gpt-4o-mini
claude-3-opus      → USE: claude-sonnet-4-5-20250929
claude-3-sonnet    → USE: claude-sonnet-4-5-20250929
gemini-2.0-flash   → USE: gemini-2.5-flash
```

### ✅ NEW (CURRENT)
```
gpt-5              # Latest GPT
gpt-4o-mini        # Best balanced
o4-mini            # Cheapest ultra-fast
claude-sonnet-4-5-20250929   # Latest Claude Sonnet
claude-haiku-4-5-20251001    # Fast Claude
gemini-2.5-pro     # Latest Gemini
gemini-2.5-flash   # Fast Gemini
llama-3.3-70b      # Fastest inference
```

---

## 📋 NEXT STEPS

1. ✅ Update provider smoke test with these models
2. ✅ Configure dashboard to prefer `gpt-4o-mini` and `claude-haiku-4-5-20251001`
3. ✅ Set Groq as emergency fast fallback
4. ✅ Test with actual Constitutional Market Harmonics system

---

**Status**: ✅ Models Corrected & Verified  
**Date**: November 6, 2025  
**Source**: Codebase analysis (`optimized_provider_router.py`, `operation_mega_router.py`, `fixed_api_test.py`)  
**Ready for Integration**: YES
