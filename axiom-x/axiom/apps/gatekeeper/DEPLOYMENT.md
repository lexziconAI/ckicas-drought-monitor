---
author: "Regan William DUFF"
company: "AXIOM INTELLIGENCE LIMITED"
company_number: "9287393"
date: "October 26, 2025"
cryptographic_signature: "e368e457794a2be7283831a073a9dc2e15dc537035dc8af08a0d5bde13e866e8"
constitutional_compliance: "Satya, Asteya, Ahimsa"
provenance_hash: "53ee22ff68d9cddb96806fbaa5c8d78584adb311ffb6858ac22a2dc2956757fc"
---

# 🚀 GATEKEEPER - Quick Deployment Guide

**From zero to qualified leads in 5 minutes**

---

## ✅ Prerequisites

- Python 3.9+ installed
- Internet connection (for AI model, optional)

---

## 📦 Step 1: Install Dependencies (30 seconds)

```bash
pip install fastapi uvicorn pydantic
```

**Optional** (for AI responses):
```bash
pip install openai anthropic
```

---

## 🎯 Step 2: Deploy (One Command)

```bash
cd axiom-x
python -m axiom.apps.gatekeeper.cli deploy
```

**Expected Output:**
```
================================================================================
GATEKEEPER - Starting Web Server
================================================================================
Server: http://localhost:8765
API Docs: http://localhost:8765/docs
Health: http://localhost:8765/health
================================================================================
INFO:     Uvicorn running on http://0.0.0.0:8765
```

---

## 🌐 Step 3: Test It

### Option A: Web Browser
1. Open: http://localhost:8765
2. Type: "How does this work?"
3. Request: "Show me a receipt for SENTINEL"
4. Qualify: "I'm the CTO, budget is $150K, need it ASAP"

### Option B: API Test
```bash
# Health check
curl http://localhost:8765/health

# Create conversation
curl -X POST http://localhost:8765/api/conversations/new

# Send message
curl -X POST http://localhost:8765/api/conversations/message \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "YOUR_CONV_ID",
    "message": "Show me a receipt for SENTINEL"
  }'
```

---

## 📊 Step 4: Monitor Analytics

```bash
# CLI
python -m axiom.apps.gatekeeper.cli analytics

# Or API
curl http://localhost:8765/api/analytics/dashboard
```

**Shows:**
- Total conversations
- Qualification rate
- Common questions
- Time to qualification

---

## 🔧 Optional: Enable AI Responses

**For GPT-4:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**For Claude:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Then restart server. Without keys, mock mode works fine for testing!

---

## 📧 Optional: Enable Email Notifications

```bash
export NOTIFICATION_EMAIL="you@email.com"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PASSWORD="your-app-password"
```

**Get Gmail App Password:**
1. Go to: https://myaccount.google.com/apppasswords
2. Create app password for "Mail"
3. Use that password (not your Gmail password)

---

## 🚢 Production Deployment

### Railway.app (Recommended)

1. Create `Procfile`:
```
web: python -m axiom.apps.gatekeeper.cli deploy --port $PORT --host 0.0.0.0
```

2. Deploy:
```bash
railway login
railway init
railway up
```

3. Set environment variables in Railway dashboard

### Render.com

1. Connect GitHub repo
2. Set start command:
```
python -m axiom.apps.gatekeeper.cli deploy --port $PORT --host 0.0.0.0
```
3. Set environment variables in Render dashboard

### Fly.io

1. Create `fly.toml`:
```toml
app = "gatekeeper"

[http_service]
  internal_port = 8765
  force_https = true
```

2. Deploy:
```bash
fly launch
fly deploy
```

---

## 🧪 Testing

### Run All Tests
```bash
python -m axiom.apps.gatekeeper.cli test
```

### Test Individual Components
```bash
# Privacy guard (prevents code leakage)
python -m axiom.apps.gatekeeper.privacy

# Qualification (BANT scoring)
python -m axiom.apps.gatekeeper.qualification

# Receipts (cryptographic proof)
python -m axiom.apps.gatekeeper.receipts

# Fractal sharding (optimization)
python -m axiom.apps.gatekeeper.cli explore
```

---

## 📈 Success Metrics (Week 1)

Track these in analytics dashboard:

| Metric | Target | How to Achieve |
|--------|--------|----------------|
| Conversations | 20+ | Drive traffic to site |
| Avg Messages | 5+ | Engaging conversation flow |
| Qualification Rate | 10-20% | BANT scoring tuned right |
| False Positives | <20% | Red flag detection working |
| Time per Lead | <30 min | Automation saves time |

---

## 🛠️ Troubleshooting

### Server won't start

**Error**: Port already in use
```bash
# Use different port
python -m axiom.apps.gatekeeper.cli deploy --port 8766
```

**Error**: Dependencies missing
```bash
pip install fastapi uvicorn pydantic
```

### AI responses not working

**Mock mode** works without API keys! For production:
```bash
export OPENAI_API_KEY="sk-..."
```

Or edit `axiom/apps/gatekeeper/web.py`:
```python
conversation_engine = ConversationEngine(llm_provider="openai")  # or "anthropic"
```

### Email notifications not sending

Check configuration:
```bash
python -c "import os; print('Email:', os.getenv('NOTIFICATION_EMAIL')); print('SMTP:', os.getenv('SMTP_SERVER'))"
```

Notifications will print to console if email not configured.

### Privacy guard too strict

Adjust in `axiom/apps/gatekeeper/privacy.py`:
```python
self.privacy_guard = PrivacyGuard(strict_mode=False)  # Less strict
```

---

## 🎯 Example Conversation Flow

```
User: "Hi, what is this?"
Bot:  "👋 Hi! I showcase AI systems built 100-500x faster..."

User: "Show me proof"
Bot:  "I can generate a build receipt for SENTINEL, Decision Arena, or LOG⁴..."

User: "SENTINEL please"
Bot:  [Generates receipt with cryptographic signature]

User: "Impressive. I'm the CTO, we need this ASAP. Budget is $150K."
Bot:  "Perfect! Let me tell you more about SENTINEL..."

[System qualifies lead: Score 85/100]
[Email sent to you: "🎯 Qualified Lead Ready!"]
```

---

## 📞 What Happens Next?

1. **Qualified Lead** (70+ score) → You get email notification immediately
2. **Warm Lead** (50-69) → System continues nurturing
3. **Cold Lead** (<50) → Minimal engagement
4. **Disqualified** (red flags) → Politely declined, no notification

You only spend time on **qualified leads** (70+).

---

## 🔥 Rapid Iteration

### Tune Qualification Thresholds

Edit `reports/gatekeeper_exploration/qualification_optimal_weights.json`:
```json
{
  "threshold_qualified": 70,  // Lower = more leads, higher = stricter
  "threshold_warm": 50
}
```

### Add More Receipts

Edit `axiom/apps/gatekeeper/knowledge.py`:
```python
SYSTEM_DESCRIPTIONS = {
    "your_system": {
        "name": "Your System",
        "build_time": "X hours",
        "description": "...",
        "capabilities": [...]
    }
}
```

### Customize Conversation Style

Edit optimal config or re-run:
```bash
python -m axiom.apps.gatekeeper.cli explore
```

---

## 📚 Full Documentation

- **README.md** - Complete feature list
- **reports/gatekeeper_exploration/** - Fractal sharding results
- **API Docs** - http://localhost:8765/docs

---

## ✅ Deployment Checklist

- [ ] Dependencies installed (`pip install fastapi uvicorn pydantic`)
- [ ] Server starts (`python -m axiom.apps.gatekeeper.cli deploy`)
- [ ] Web interface loads (http://localhost:8765)
- [ ] Conversation works (send a message)
- [ ] Receipt generates (request SENTINEL receipt)
- [ ] Qualification works (test with "I'm the CTO, budget $150K")
- [ ] Analytics tracking (view dashboard)
- [ ] (Optional) AI responses enabled (set `OPENAI_API_KEY`)
- [ ] (Optional) Email notifications (set `NOTIFICATION_EMAIL`, `SMTP_*`)
- [ ] Production deployment (Railway/Render/Fly.io)

---

## 🎉 You're Live!

**Server is running at: http://localhost:8765**

**Next steps:**
1. Test with friends
2. Share link on social media
3. Monitor analytics daily
4. Respond to qualified leads within 4 hours
5. Iterate based on metrics

**Target: First qualified lead within 7 days!**

---

Built with LOG⁴ fractal sharding - 10M conversation strategies explored in 0.22 seconds.

**GATEKEEPER: Qualify leads faster than they can say "show me the code."** 🚀
