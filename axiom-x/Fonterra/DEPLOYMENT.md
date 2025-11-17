# 🚢 Deployment Guide: NZ Drought Early Warning Dashboard

**Constitutional AI deployment to Render with CKICAS platform foundation**

## 📋 Prerequisites

- [GitHub Account](https://github.com) with repository access
- [Render Account](https://render.com) (free tier available)
- NIWA DataHub API access (contact Dr. Jochen Schmidt)
- OpenWeatherMap API key (free tier)
- Regional Council API access (most are public)

## 🏗️ Architecture Overview

### Production Stack
- **Frontend**: React 18 + Vite → Static hosting on Render
- **Backend**: FastAPI + SQLAlchemy → Web service on Render
- **Database**: PostgreSQL on Render (free tier: 256MB → $7/mo: 1GB)
- **Jobs**: Background cron jobs for data refresh
- **CI/CD**: GitHub Actions with constitutional compliance checks

### CKICAS Platform Foundation
This deployment establishes the **modular architecture** for the broader CKICAS (Community Kinetic Intelligent Complex Adaptive System) platform:

```
CKICAS Platform (Future)
├── 📊 Drought Module (Phase 1 - This deployment)
├── 🦠 Pandemic Early Warning (Phase 2)
├── 🌪️ Climate Event Tracking (Phase 3)
└── 🏭 Supply Chain Resilience (Phase 4)
```

## 🚀 Quick Deploy

### 1. Fork & Clone Repository
```bash
git clone https://github.com/lexziconAI/constitutional-market-harmonics.git
cd constitutional-market-harmonics/Fonterra
```

### 2. Set Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Deploy to Render

#### Option A: One-Click Deploy (Recommended)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

#### Option B: Manual Setup
1. Connect GitHub repository to Render
2. Create PostgreSQL database instance
3. Create web service using `render.yaml`
4. Set environment variables in Render dashboard

### 4. Configure Environment Variables
In Render dashboard, set these secrets:

```bash
# Database (auto-configured by render.yaml)
DATABASE_URL=postgresql://...

# NIWA APIs
NIWA_API_KEY=your_niwa_api_key
NIWA_DATAHUB_EMAIL=your.email@domain.com

# Weather API
OPENWEATHER_API_KEY=your_openweather_api_key

# Application
ENVIRONMENT=production
LOG_LEVEL=INFO
CACHE_TTL_HOURS=12
RATE_LIMIT_PER_DAY=1000
```

## 🔧 Configuration Details

### Render Services

#### Web Service (`nz-drought-dashboard`)
- **Type**: Web Service
- **Environment**: Python 3.9
- **Build Command**: See `render.yaml`
- **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check**: `/health`
- **Instance**: Free tier (750 hours/month) → Starter ($7/mo) for production

#### Database (`drought-db`)
- **Type**: PostgreSQL
- **Plan**: Free (256MB) → Starter ($7/mo, 1GB) for production
- **Version**: Latest stable

#### Cron Jobs
- **Daily NIWA Fetch**: `0 18 * * *` (6am NZ time)
- **Hourly Council Data**: `0 * * * *`

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | ✅ | Auto | PostgreSQL connection string |
| `NIWA_API_KEY` | ✅ | - | NIWA CliFlo API key |
| `NIWA_DATAHUB_EMAIL` | ✅ | - | NIWA DataHub account email |
| `OPENWEATHER_API_KEY` | ✅ | - | OpenWeatherMap API key |
| `ENVIRONMENT` | ❌ | development | Runtime environment |
| `LOG_LEVEL` | ❌ | INFO | Logging verbosity |
| `CACHE_TTL_HOURS` | ❌ | 12 | Brahmacharya cache expiry |
| `RATE_LIMIT_PER_DAY` | ❌ | 1000 | Aparigraha public API limit |

## 🧪 Testing & Validation

### Pre-Deployment Tests
```bash
# Constitutional compliance tests
cd backend
pytest tests/test_constitutional.py -v

# API integration tests
pytest tests/test_api.py -v

# Agent functionality tests
pytest tests/test_agents.py -v
```

### Post-Deployment Validation
```bash
# Health check
curl https://your-app.render.com/health

# Test public API
curl "https://your-app.render.com/api/public/drought-risk?lat=-37.7&lon=175.2&forecast_days=14"
```

## 📊 Monitoring & Maintenance

### Health Endpoints
- **System Health**: `GET /health` - Comprehensive status with metrics
- **API Docs**: `GET /docs` - Interactive FastAPI documentation

### Brahmacharya Efficiency Monitoring
The `/health` endpoint provides:
- Cache hit rate (target: >80%)
- API calls saved through caching
- Response time metrics
- Constitutional compliance status

### Alerting
Set up Render alerts for:
- Service downtime
- Database connection issues
- High error rates
- Cache efficiency drops below 70%

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
Located in `.github/workflows/deploy.yml`:

1. **Test Stage**:
   - Run constitutional compliance tests
   - Execute API integration tests
   - Build frontend assets

2. **Deploy Stage** (main branch only):
   - Deploy to Render
   - Health check validation
   - Slack/email notifications

### Constitutional CI/CD Checks
- **Ahimsa**: No untested code paths that could cause false alarms
- **Satya**: Confidence calibration validation
- **Asteya**: Data attribution completeness
- **Brahmacharya**: Cache efficiency monitoring
- **Aparigraha**: Public API accessibility

## 🚨 Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check Render database status
# Verify DATABASE_URL environment variable
# Ensure PostgreSQL instance is running
```

#### API Keys Invalid
```bash
# Verify NIWA credentials with test API call
# Check OpenWeatherMap API key validity
# Confirm regional council endpoints accessible
```

#### Build Failures
```bash
# Check Python/Node.js versions in render.yaml
# Verify requirements.txt dependencies
# Confirm frontend build process
```

#### Cache Efficiency Low
- Monitor `/health` endpoint Brahmacharya metrics
- Adjust `CACHE_TTL_HOURS` if needed
- Check for API rate limiting issues

### Rollback Procedure
1. Revert GitHub commit
2. GitHub Actions will auto-deploy previous version
3. Monitor health endpoint for recovery
4. Notify stakeholders of rollback

## 📈 Scaling Considerations

### Free Tier Limits
- **Web Service**: 750 hours/month
- **Database**: 256MB storage
- **Cron Jobs**: Limited execution time

### Production Scaling
- **Web Service**: Upgrade to Starter ($7/mo) or Standard ($25/mo)
- **Database**: Upgrade to 1GB ($7/mo) or larger
- **CDN**: Consider Cloudflare for global performance

### Performance Optimization
- **Frontend**: Code splitting by route
- **Backend**: Async database connections
- **Caching**: Brahmacharya intelligent cache management
- **APIs**: Rate limiting and request batching

## 🔗 CKICAS Platform Extension

### Modular Architecture
This deployment creates the foundation for CKICAS modules:

```python
# Future module registration
ckicas_modules = {
    "drought": DroughtModule(),
    "pandemic": PandemicModule(),
    "climate": ClimateModule(),
    "supply_chain": SupplyChainModule()
}
```

### Adding New Modules
1. Create module directory under `backend/app/modules/`
2. Implement constitutional agent pattern
3. Add to orchestrator configuration
4. Update frontend dashboard
5. Extend health monitoring

## 📞 Support & Contact

### Academic Context
- **Institution**: University of Auckland, Information Systems
- **Research**: CKICAS framework for community resilience
- **Supervisor**: Associate Professor [Name]

### Technical Support
- **Issues**: GitHub Issues in this repository
- **Documentation**: Update this guide as needed
- **Constitutional Questions**: Refer to Yama principles in README

### Community Validation
- **Farmers**: Waikato/Taranaki dairy farmers
- **Agri-Organizations**: DairyNZ, Federated Farmers
- **Government**: Regional Councils, MPI

---

## ✅ Success Criteria

**Short-term (2 weeks):**
- [ ] Deployed to Render with HTTPS, <2s page load
- [ ] NIWA DataHub integration pathway ready
- [ ] CI/CD pipeline running, all tests passing
- [ ] Health monitoring active, alerts configured

**Medium-term (1-2 months):**
- [ ] VCSN data integrated when access granted
- [ ] 10+ farmers validating tool in Waikato/Taranaki
- [ ] Zero false alarms logged (Ahimsa compliance validated)
- [ ] Modular architecture designed for next CKICAS modules

**Long-term (6 months):**
- [ ] CKICAS manuscript submitted to CAIS journal
- [ ] Second resilience module deployed (TBD based on community needs)
- [ ] Open source repository public with documentation
- [ ] DairyNZ or Federated Farmers promotion secured

**Built with ❤️ for New Zealand farmers by Constitutional AI** 🇳🇿🌾