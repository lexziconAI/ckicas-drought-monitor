# 🤝 Contributing to CKICAS: Constitutional AI Development

**Guidelines for contributing to the Community Kinetic Intelligent Complex Adaptive System**

## 🧘 Constitutional Development Principles

All contributions must uphold the **5 Yama constitutional principles**:

### 1. **Ahimsa** (Non-Harm)
- Never introduce code that could cause false alarms or delayed warnings
- Test all alert logic with edge cases
- Include "what would change this assessment" in any new alerts

### 2. **Satya** (Truth)
- All confidence levels must be transparent and time-calibrated
- Include explicit uncertainty quantification
- Log complete provenance for any predictions

### 3. **Asteya** (Attribution)
- Cite all data sources with timestamps and freshness
- Respect API terms of service and data licenses
- Acknowledge intellectual property of data providers

### 4. **Brahmacharya** (Efficiency)
- Implement intelligent caching to prevent unnecessary API calls
- Monitor and optimize computational resource usage
- Target >80% cache hit rate for production systems

### 5. **Aparigraha** (Generosity)
- Keep critical community information freely accessible
- Design public APIs with reasonable rate limits
- Enable data export for community analysis

## 🚀 Getting Started

### Development Environment
```bash
# Clone repository
git clone https://github.com/lexziconAI/constitutional-market-harmonics.git
cd constitutional-market-harmonics/Fonterra

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Backend setup
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "from app.models.database import create_tables; import asyncio; asyncio.run(create_tables())"

# Frontend setup
cd ../frontend
npm install
npm run dev

# Run tests
cd ../backend
pytest tests/ -v
```

### Project Structure
```
Fonterra/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── agents/         # Constitutional AI agents
│   │   ├── api/            # REST API endpoints
│   │   ├── constitutional/ # Yama principle enforcement
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── services/       # Shared services (cache, etc.)
│   │   └── utils/          # Utility functions
│   ├── jobs/               # Background cron jobs
│   └── tests/              # Test suite
├── frontend/               # React dashboard
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   └── utils/          # Frontend utilities
│   └── public/             # Static assets
├── .github/workflows/      # CI/CD pipelines
└── docs/                   # Documentation
```

## 🧪 Testing Requirements

### Constitutional Compliance Tests
All changes must pass constitutional validation:
```bash
# Run all constitutional tests
pytest tests/test_constitutional.py -v

# Test specific principles
pytest tests/test_constitutional.py::TestAhimsa -v
pytest tests/test_constitutional.py::TestSatya -v
pytest tests/test_constitutional.py::TestAsteya -v
pytest tests/test_constitutional.py::TestBrahmacharya -v
pytest tests/test_constitutional.py::TestAparigraha -v
```

### Test Coverage
- **Target**: >95% code coverage
- **Critical Paths**: All alert generation logic must be tested
- **Edge Cases**: Network failures, API rate limits, data corruption

### Performance Benchmarks
- **API Response Time**: <500ms for cached requests
- **Cache Hit Rate**: >80% in production
- **Memory Usage**: <512MB per service instance

## 📝 Contribution Workflow

### 1. Choose an Issue
- Check [GitHub Issues](../../issues) for CKICAS development tasks
- Look for issues labeled `constitutional-ai`, `ckicas-module`, or `good-first-issue`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or for constitutional fixes
git checkout -b fix/constitutional-violation-name
```

### 3. Implement with Constitutional Rigor
```python
# Example: Adding new agent with constitutional compliance
class NewConstitutionalAgent:
    def __init__(self):
        self.confidence_calculator = ConstitutionalConfidence()

    async def assess_situation(self, data: Dict) -> Dict:
        # Brahmacharya: Check cache first
        cached_result = await brahmacharya_cache.get(f"new_agent_{hash(data)}")
        if cached_result:
            return cached_result

        # Process data with constitutional validation
        result = await self._process_data(data)

        # Satya: Calibrate confidence levels
        result['confidence'] = self.confidence_calculator.calibrate(
            indicators=result['indicators'],
            time_horizon=result['forecast_days']
        )

        # Asteya: Include data sources
        result['sources'] = self._get_data_sources(data)

        # Brahmacharya: Cache result
        await brahmacharya_cache.set(
            f"new_agent_{hash(data)}",
            result,
            ttl_hours=12
        )

        return result
```

### 4. Test Thoroughly
```bash
# Run full test suite
pytest tests/ -v --tb=short

# Check constitutional compliance
pytest tests/test_constitutional.py -v

# Performance testing
pytest tests/test_performance.py -v
```

### 5. Update Documentation
```bash
# Update API documentation
# Add constitutional compliance notes
# Update deployment guide if needed
```

### 6. Submit Pull Request
- **Title**: `[CONSTITUTIONAL] Brief description of changes`
- **Description**: Include constitutional impact assessment
- **Labels**: `constitutional-ai`, relevant module labels
- **Checklist**:
  - [ ] All tests pass
  - [ ] Constitutional compliance verified
  - [ ] Documentation updated
  - [ ] Performance benchmarks met
  - [ ] Code review requested

## 🏗️ Adding New CKICAS Modules

### Module Template
```python
# ckicas_modules/new_module.py
from app.constitutional.base import ConstitutionalModule
from app.agents.base import ConstitutionalAgent

class NewModule(ConstitutionalModule):
    """
    Constitutional AI module for [specific community challenge].
    Implements all 5 Yama principles.
    """

    def __init__(self):
        self.agents = {
            "data_collection": DataCollectionAgent(),
            "analysis": AnalysisAgent(),
            "forecast": ForecastAgent(),
            "validation": ConstitutionalValidator()
        }

        # Constitutional configuration
        self.yama_config = {
            "ahimsa": {"max_false_alarm_rate": 0.05},
            "satya": {"confidence_calibration": True},
            "asteya": {"attribution_required": True},
            "brahmacharya": {"cache_ttl_hours": 12},
            "aparigraha": {"public_api": True}
        }

    async def assess_risk(self, context: Dict) -> Dict:
        """
        Main assessment with constitutional guarantees.
        Returns result with confidence calibration and source attribution.
        """
        # Implementation here
        pass
```

### Module Registration
```python
# app/orchestrator.py
from ckicas_modules.new_module import NewModule

class CKICASOrchestrator:
    def __init__(self):
        self.modules = {
            "drought": DroughtModule(),
            "pandemic": PandemicModule(),
            "climate": ClimateModule(),
            "new_module": NewModule()  # Add new module here
        }
```

## 🔧 Code Quality Standards

### Python Backend
- **Type Hints**: All functions must have type annotations
- **Docstrings**: Google-style docstrings for all public methods
- **Error Handling**: Comprehensive exception handling with logging
- **Async/Await**: Proper async patterns throughout

### React Frontend
- **TypeScript**: Strict typing for all components
- **Accessibility**: WCAG 2.1 AA compliance
- **Performance**: Code splitting and lazy loading
- **Testing**: Jest + React Testing Library

### Database
- **Migrations**: Alembic for all schema changes
- **Indexes**: Proper indexing for query performance
- **Constraints**: Database-level data validation
- **Auditing**: Constitutional audit logging

## 📊 Performance Monitoring

### Key Metrics to Monitor
- **API Response Time**: Target <500ms
- **Cache Hit Rate**: Target >80%
- **Error Rate**: Target <1%
- **Constitutional Compliance**: 100% Yama adherence

### Health Checks
```python
# /health endpoint provides:
- System status (healthy/degraded/unhealthy)
- Constitutional compliance status
- Brahmacharya efficiency metrics
- API availability status
- Performance benchmarks
```

## 🚨 Issue Reporting

### Constitutional Violations
If you discover a constitutional violation:
1. **Stop the violation** immediately
2. **Create a critical issue** with `constitutional-violation` label
3. **Implement fix** with constitutional review
4. **Add regression test** to prevent future violations

### Bug Reports
- **Template**: Use GitHub issue templates
- **Constitutional Impact**: Assess impact on Yama principles
- **Severity**: Critical for Ahimsa violations, High for other principles
- **Reproduction**: Minimal test case required

## 🎓 Learning Resources

### Constitutional AI
- [Yama Principles](https://en.wikipedia.org/wiki/Yama)
- [Constitutional AI Paper](https://arxiv.org/abs/2212.08073)
- [CKICAS Framework Documentation](./CKICAS_ROADMAP.md)

### Technical Skills
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Best Practices](https://react.dev/learn)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Constitutional Testing Patterns](./tests/test_constitutional.py)

## 🙏 Recognition

Contributors will be recognized as:
- **CKICAS Fellows**: Major module development
- **Constitutional Guardians**: Framework improvements
- **Community Champions**: Documentation and testing
- **Research Partners**: Academic collaboration

All contributors acknowledged in:
- Academic publications
- Platform documentation
- Community presentations
- Open source attribution

## 📞 Getting Help

- **Technical Questions**: GitHub Discussions
- **Constitutional Guidance**: Review existing implementations
- **Community Support**: NZ farming community feedback
- **Academic Collaboration**: University of Auckland research team

---

## ✅ Pull Request Checklist

- [ ] **Constitutional Compliance**: All 5 Yama principles maintained
- [ ] **Testing**: 95%+ coverage, all tests pass
- [ ] **Documentation**: Code and API docs updated
- [ ] **Performance**: Benchmarks met, no regressions
- [ ] **Security**: No vulnerabilities introduced
- [ ] **Accessibility**: Frontend changes meet WCAG standards
- [ ] **Cross-platform**: Works on target deployment platforms

**Remember**: Every line of code in CKICAS has the potential to impact community safety and resilience. Code with compassion, test with rigor, and contribute with constitutional integrity.

*Built with ❤️ for resilient communities by Constitutional AI* 🇳🇿🤝