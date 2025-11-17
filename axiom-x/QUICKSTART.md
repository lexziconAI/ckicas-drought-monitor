# AXIOM-X QUICK START GUIDE
## Get Your System Running in 5 Minutes

---

````markdown
# AXIOM-X QUICK START GUIDE
## Get Your System Running in 5 Minutes

---

## 🎯 CHOOSE YOUR QUICKSTART PATH

**Which describes you?**

| Goal | Your Path | Time | Next Steps |
|------|-----------|------|-----------|
| 🚀 **Just get it running** | 👇 **⚡ FASTEST START** (below) | 5 min | Docker or Local |
| 🤖 **Enable autonomous learning** | 📖 **[AUTONOMOUS_LEARNING_QUICKSTART.md](./AUTONOMOUS_LEARNING_QUICKSTART.md)** | 10 min | Safety modes + monitoring |
| 📊 **Track your portfolio** | 📈 **[constitutional-market-harmonics/README.md](./constitutional-market-harmonics/README.md)** | 15 min | Dashboard + chaos signals |
| 🔧 **Deploy with containers** | 🐳 **DOCKER START** (below) | 15 min | Full stack + monitoring |
| 🏭 **Scale to production** | 📋 **[IMPLEMENTATION_GUIDE_LATEST_MODELS_2025.md](./IMPLEMENTATION_GUIDE_LATEST_MODELS_2025.md)** | 1 hour | Workers + orchestration |
| 🧠 **Understand the architecture** | 🏗️ **[LLM_ROUTING_ARCHITECTURE.html](./LLM_ROUTING_ARCHITECTURE.html)** | 30 min | Multi-provider routing |

---

## ⚡ FASTEST START (Local Development)

```powershell
# 1. Start the system
.\start_axiom_x.ps1 -SkipDocker

# 2. Run health check
python system_health_check.py

# 3. Test provider router
python optimized_provider_router.py

# 4. Run capacity discovery
python capacity_discovery_engine.py
```

**✅ System Status:** Check output shows HEALTHY (97.1%)

---

## 🐳 DOCKER START (Production-like)

```powershell
# 1. Start full Docker stack
.\start_axiom_x.ps1

# 2. Verify all services running
docker-compose ps

# 3. View logs
docker-compose logs -f axiom-x

# 4. Access dashboards
# Main App:    http://localhost:8000
# Prometheus:  http://localhost:9091
# Grafana:     http://localhost:3000
```

**Login to Grafana:** admin / axiom_grafana_pass

---

## 🔧 WORKER DEPLOYMENT

```powershell
# Deploy all 15 workers
python axiom_x_initialization_worker_spawner.py

# Check worker results
ls worker_results/

# Run specific worker
python workers/environment_validator_worker.py
```

**Current Status:** 13/15 workers completed (86.7%)

---

## 📊 KEY COMMANDS

### System Health
```powershell
# Full health check
python system_health_check.py

# Quick status
.\start_axiom_x.ps1 -SkipDocker -SkipHealthCheck
```

### Docker Operations
```powershell
# Start
docker-compose up -d

# Stop
docker-compose down

# Rebuild
docker-compose build --no-cache

# Logs
docker-compose logs -f [service-name]

# Restart service
docker-compose restart axiom-x
```

### Provider Router & Models

🔑 **CRITICAL: Single Source of Truth for Models**

**The authoritative provider configuration is in:** `optimized_provider_router.py`

All model decisions go through this file:
- ✅ Tier 1 Premium: `claude-sonnet-4-5-20250929`, `gpt-5` (best quality)
- ✅ Tier 2 Balanced: `claude-haiku-4-5-20251001`, `gemini-2.5-flash` (good quality/cost)
- ✅ Tier 3 Fast: `llama-3.3-70b-versatile` (lowest cost, 300ms latency)

**Reference Documentation:**
- 📊 **Full model registry:** [LATEST_MODELS_REGISTRY_NOVEMBER_2025.md](./LATEST_MODELS_REGISTRY_NOVEMBER_2025.md) (42 models, all providers)
- 🧠 **Model configuration corrected:** [CONSTITUTIONAL_MEMORY_MODEL_CONFIG_CORRECTED.md](./CONSTITUTIONAL_MEMORY_MODEL_CONFIG_CORRECTED.md)
- ⚙️ **Deployment guide:** [IMPLEMENTATION_GUIDE_LATEST_MODELS_2025.md](./IMPLEMENTATION_GUIDE_LATEST_MODELS_2025.md)

```python
# Test routing
python -c "
import asyncio
from optimized_provider_router import get_router

async def test():
    router = get_router()
    decision = await router.route_request('Hello world')
    print(f'Provider: {decision.provider}')
    print(f'Model: {decision.model}')
    print(f'Reasoning: {decision.reasoning}')

asyncio.run(test())
"
```

---

## 🏥 TROUBLESHOOTING

### Issue: Workers Failed to Deploy
```powershell
# Re-run worker spawner
python axiom_x_initialization_worker_spawner.py

# Check specific worker
python workers/environment_validator_worker.py
```

### Issue: Docker Services Not Starting
```powershell
# Check Docker is running
docker --version

# Remove old containers
docker-compose down -v

# Rebuild and restart
docker-compose build
docker-compose up -d
```

### Issue: API Keys Not Working
```powershell
# Verify .env file exists
cat .env

# Reload environment
.\start_axiom_x.ps1

# Test specific provider
python test_anthropic_api.py
```

---

## 📁 FILE LOCATIONS

| Component | File Path |
|-----------|-----------|
| Main Startup | `start_axiom_x.ps1` |
| Worker Spawner | `axiom_x_initialization_worker_spawner.py` |
| Health Check | `system_health_check.py` |
| Provider Router | `optimized_provider_router.py` |
| Docker Compose | `docker-compose.yml` |
| Dockerfile | `Dockerfile` |
| Kubernetes | `kubernetes/sidecar-monitoring.yaml` |
| Environment | `.env` |
| Worker Results | `worker_results/*.json` |
| System Reports | `system_health_report_*.json` |

---

## 🎯 COMMON WORKFLOWS

### Run Constitutional AI Task
```powershell
# 1. Start system
.\start_axiom_x.ps1 -SkipDocker

# 2. Run capacity discovery
python capacity_discovery_engine.py

# 3. Run synthesis
python synthesis_engine.py

# 4. Check approval gate
python approval_gate.py
```

### Deploy to Production
```powershell
# 1. Build Docker images
docker-compose build

# 2. Run security scan
docker scan axiom-x:latest

# 3. Start stack
docker-compose up -d

# 4. Verify health
python system_health_check.py

# 5. Monitor
# Open http://localhost:3000 (Grafana)
```

### Update System
```powershell
# 1. Pull latest code
git pull

# 2. Redeploy workers
python axiom_x_initialization_worker_spawner.py

# 3. Rebuild Docker
docker-compose build

# 4. Restart
docker-compose up -d
```

---

## 🚀 PRODUCTION CHECKLIST

Before deploying to production:

- [ ] All API keys configured in `.env`
- [ ] Docker stack tested locally
- [ ] Health check shows 100% (or explain warnings)
- [ ] Security scan completed
- [ ] Grafana dashboards configured
- [ ] Log aggregation working
- [ ] Backup procedures tested
- [ ] SSL/TLS certificates configured
- [ ] Firewall rules set
- [ ] Monitoring alerts configured

---

## 💡 TIPS

1. **Performance:** Use `optimized_provider_router.py` for automatic provider selection
2. **Monitoring:** Grafana dashboards show real-time metrics
3. **Debugging:** Check `logs/` directory for detailed logs
4. **Workers:** Run workers in parallel for faster deployment
5. **Health:** Run `system_health_check.py` after any changes

---

## 📞 QUICK REFERENCE

| What | Command |
|------|---------|
| Start System | `.\start_axiom_x.ps1` |
| Health Check | `python system_health_check.py` |
| Deploy Workers | `python axiom_x_initialization_worker_spawner.py` |
| Docker Up | `docker-compose up -d` |
| Docker Down | `docker-compose down` |
| View Logs | `docker-compose logs -f` |
| Grafana | http://localhost:3000 |
| Main App | http://localhost:8000 |

---

**System Status:** 🟢 OPERATIONAL (97.1% Health)  
**Last Updated:** November 6, 2025 (Model Configuration Corrected)  
**Workers Deployed:** 13/15 (86.7%)  
**Authoritative Model Config:** See `CONSTITUTIONAL_MEMORY_MODEL_CONFIG_CORRECTED.md`
