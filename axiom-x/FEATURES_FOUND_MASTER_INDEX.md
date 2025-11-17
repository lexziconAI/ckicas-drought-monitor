# 🌀 CONSTITUTIONAL MARKET HARMONICS - COMPLETE FEATURE MASTER INDEX

**Fractal Analysis Discovery Session | November 7, 2025**

---

## 📊 DUMMY INTERNATIONAL STOCK PORTFOLIO

**Location:** `INTERNATIONAL_PORTFOLIO_FOUND.md` + Backend API

### Portfolio Composition (19 Total Holdings):
- **US Positions**: 6 holdings = $225,879.11 (59.28%)
- **International Positions**: 13 holdings = $155,154.49 (40.72%)
- **Total Portfolio Value**: $381,033.60

### International Holdings by Region:

#### 🇪🇺 EUROPE ($90,744.73 | 58.5% of International)
1. **🇳🇱 ASML.AS** (Netherlands) - $49,602.78 - Semiconductor equipment - **32% of international**
2. **🇩🇪 SAP.DE** (Germany) - $20,012.40 - Enterprise software
3. **🇬🇧 AZN.L** (UK) - $14,706.60 - AstraZeneca (Pharma)
4. **🇬🇧 ULVR.L** (UK) - $5,353.05 - Unilever (Consumer goods)
5. **🇬🇧 HSBA.L** (UK) - $869.95 - HSBC (Banking)
6. **🇫🇷 OR.PA** (France) - TBD - L'Oréal (Luxury/Consumer)

#### 🌏 ASIA PACIFIC ($62,813.51 | 40.5% of International)
1. **🇨🇳 000001.SS** (China) - $44,800.00 - Ping An (Insurance/Banking) - **29% of international**
2. **🇯🇵 8058.T** (Japan) - Mitsubishi (Conglomerate)
3. **🇮🇳 INFY** (India) - Infosys (IT Services)
4. **🇰🇷 005930.KS** (South Korea) - Samsung (Electronics)
5. **🇸🇬 C6L.SG** (Singapore) - DBS Group (Banking)
6. **🇹🇭 ADVANC.BK** (Thailand) - Advanced (Telecom)
7. **🇻🇳 VNM** (Vietnam) - Vinamilk (Consumer Goods)

#### 🌎 NORTH AMERICA OTHER ($1,788.50 | 1.15% of International)
1. **🇨🇦 TOX.TO** (Canada) - Toromont (Industrial equipment)

### API Endpoints for Portfolio:
```bash
GET /api/international-portfolio        # Full international breakdown
GET /api/starting-balances              # Initial positions with international data
GET /api/portfolio                      # All positions (US + International)
```

### Backend Data Files:
- `server.ts` (Lines 270-450) - `/api/international-portfolio` endpoint
- `server.ts` (Lines 449-524) - Enhanced `/api/starting-balances` endpoint
- `INTERNATIONAL_PORTFOLIO_FOUND.md` - Complete discovery document

---

## 📈 CHART & GRAPH COMPONENTS

**Technology:** Chart.js + React-ChartJS-2  
**Location:** `dashboard/components/` + `app/page.tsx` (25 components)

### Core Chart Types:

#### 1. **Performance Chart** (Line Chart)
- Historical ROI over time
- Sharpe ratio tracking
- Constitutional alignment over time
- **Component:** `ResilientPerformancePanel`
- **Data:** `/api/performance` endpoint

#### 2. **Portfolio Holdings Chart** (Pie/Doughnut)
- Holdings allocation by weight %
- Constitutional score per position
- Value per holding
- **Component:** `ResilientPortfolioPanel`
- **Data:** `/api/portfolio` endpoint

#### 3. **Constitutional Radar Chart** (5-axis)
- Yama Principles alignment:
  - Ahimsa (Non-violence)
  - Satya (Truth)
  - Asteya (Non-stealing)
  - Brahmacharya (Moderation)
  - Aparigraha (Non-attachment)
- **Component:** `ResilientConstitutionalRadar`

#### 4. **Market Sentiment Chart**
- Fear/Greed gauge (0-100 scale)
- Trending indicators
- Sector rotation signals
- **Component:** `ResilientMarketSentiment`

#### 5. **Forex Panel Chart**
- Currency pair data
- 4+ currency pairs with live rates
- Allocation visualization
- **Component:** `ResilientForexPanel`

#### 6. **News Carousel Cards**
- Interactive swipeable interface
- Constitutional scoring of news
- Source attribution + timestamps
- **Component:** `ResilientNewsCarousel`

#### 7. **Global Markets Data**
- 8+ exchange monitoring
- Multi-currency support
- Real-time pricing
- **Component:** `ResilientGlobalMarkets`

---

## 🌀 FRACTAL ANALYSIS & CHAOS THEORY VISUALIZATION

**Technology:** 3D Canvas/SVG rendering + Interactive Controls  
**Location:** `dashboard/components/` + Chaos Theory Attractors

### 3D Strange Attractors:

#### 1. **Lorenz Attractor**
- Classic chaos system
- 3D butterfly-shaped trajectory
- Signal strength visualization
- **Component:** `ResilientChaosVisualizer`
- **Tab:** Chaos Tab

#### 2. **Chen Attractor**
- Modified chaotic system
- Different scroll dynamics
- Market pattern correlation
- **Component:** Same (Switchable)

#### 3. **Rössler Attractor**
- Simplified chaos system
- Spiral trajectory patterns
- Risk metric correlation
- **Component:** Same (Switchable)

### Visualization Features:
- ✅ Interactive 3D rotation
- ✅ Hardware-accelerated rendering
- ✅ Real-time signal updates
- ✅ Projections between attractors
- ✅ Detailed mode for deep analysis

### API Endpoint:
```bash
GET /api/chaos  # Chaos signals for visualization
```

---

## 💬 FLOATING CLAUDE CHAT INTERFACE

**Technology:** Claude Sonnet 4.5 API + Context Awareness  
**Location:** `dashboard/page.tsx` + `server.ts` + `/api/chat`

### Features:

#### Chat Capabilities:
1. ✅ **Portfolio Context Aware**
   - Knows your holdings
   - References your positions
   - Provides portfolio-specific advice

2. ✅ **Multi-Tab Availability**
   - Floating button on ALL 8 tabs
   - Bottom-right corner persistent
   - Always accessible

3. ✅ **Conversation Memory**
   - Maintains conversation history
   - Understands follow-up questions
   - Context preservation across messages

4. ✅ **Advanced Features**
   - Extended thinking (if enabled)
   - Message export/save
   - Error handling with retry logic
   - Graceful degradation if backend fails

5. ✅ **Message Categories**
   - Portfolio analysis questions
   - Market analysis questions
   - Constitutional AI scoring questions
   - System status queries
   - Trade recommendations

### API Endpoints:
```bash
GET  /api/chat                 # Chat history/context
POST /api/chat                 # Send message to Claude
```

### UI/UX:
- **Position:** Bottom-right floating button
- **Animation:** Slide-in from right on click
- **Styling:** Dark theme with accent colors
- **Responsive:** Works on all screen sizes

---

## 🧠 NEURAL NETWORK & AI COMPONENTS

**Location:** `dashboard/page.tsx` (25 components)

### Neural Analysis Components:

#### 1. **ResilientConstitutionalNeuralNetwork**
- **Purpose:** Separate AI analysis engine
- **Shows:** Predictions, pattern detection, anomalies
- **Metrics:** Learning progress, accuracy rates
- **Tab:** Neural Tab (dedicated full-screen)
- **Output:** Investment recommendations + warnings

#### 2. **ResilientFractalOptimizationPanel**
- **Purpose:** Fractal analysis recommendations
- **Shows:** 3+ optimization suggestions
- **Metrics:** Scaling effects modeling
- **Tab:** Performance Tab
- **Output:** Rebalancing advice + alternatives

#### 3. **ResilientAdvancedAnalyticsPanel**
- **Purpose:** Statistical correlation analysis
- **Shows:** Correlation matrices + volatility metrics
- **Metrics:** Risk decomposition details
- **Tab:** Markets Tab
- **Output:** Quantitative insights

#### 4. **ResilientRiskAssessmentPanel**
- **Purpose:** Risk quantification
- **Shows:** Volatility tracking + Maximum drawdown + VaR + Stress testing
- **Metrics:** Multi-dimensional risk view
- **Tab:** Performance Tab
- **Output:** Risk warnings + mitigation strategies

#### 5. **ResilientAntenarrativeLens**
- **Purpose:** Narrative analysis of market events
- **Shows:** Story identification + Sentiment scoring
- **Connects:** Chaos theory signals ↔ News stories
- **Tab:** Chaos/News Tab
- **Output:** Narrative-driven trading signals

---

## 🎨 ALL 25 DASHBOARD COMPONENTS

### TIER 1: Always Visible (5 components)
```typescript
1. ResilientHeader
   - Portfolio value display (real-time)
   - ROI % + Constitutional Score + Fractal Love Score
   - System health status indicator
   - Last update timestamp

2. ResilientPortfolioPanel
   - Holdings table (symbol, quantity, value, weight, constitutional score)
   - Cash position display
   - Detailed & simple view modes
   - Sorting & filtering by sector/type

3. ResilientPerformancePanel
   - Historical ROI chart (line graph)
   - Sharpe ratio tracking
   - Constitutional alignment over time
   - Detailed & simple view modes

4. ResilientActivityPanel
   - Chaos signals (Lorenz, Chen, Rössler)
   - Recent trades with reasoning
   - System health metrics
   - Error tracking

5. ResilientNewsTicker
   - Live market headlines
   - Constitutional scoring of news
   - Source attribution + timestamps
   - Auto-updating feed
```

### TIER 2: Tab-Specific (6 components)
```typescript
6. ResilientChaosVisualizer
   - 3D interactive strange attractors
   - Lorenz, Chen, Rössler projections
   - Signal strength visualization
   - Switchable between attractors
   - Tab: Chaos

7. ResilientGlobalMarkets
   - International market data
   - 8+ global exchanges
   - Real-time pricing
   - Multi-currency support
   - Tab: Markets

8. ResilientMarketSentiment
   - Sentiment analysis visualization
   - Fear/Greed indicators (0-100 scale)
   - Trending signals
   - Detailed mode available
   - Tab: Markets

9. ResilientConstitutionalRadar
   - 5-axis Yama principles chart
   - Ahimsa, Satya, Asteya, Brahmacharya, Aparigraha
   - Portfolio-wide alignment
   - Per-holding alignment available
   - Tab: Overview

10. ResilientNewsCarousel
    - Interactive card-based news display
    - Swipeable interface
    - Headlines clickable
    - Constitutional scoring per article
    - Tab: News

11. ResilientForexPanel
    - Currency pair data
    - 4+ currency pairs with rates
    - Allocation visualization
    - Tab: Markets
```

### TIER 3: Advanced Analysis (7 components)
```typescript
12. ResilientBalancesAndCashflow
    - Cash flow visualization
    - Allocation breakdown
    - Rebalancing recommendations

13. ResilientFractalOptimizationPanel
    - Fractal analysis results
    - 3+ optimization suggestions
    - Scaling effects modeling

14. ResilientAdvancedAnalyticsPanel
    - Statistical correlations
    - Correlation matrices
    - Risk decomposition

15. ResilientRiskAssessmentPanel
    - Volatility tracking
    - Maximum drawdown
    - Value-at-Risk (VaR)
    - Stress testing results

16. ResilientMarketIntelligencePanel
    - Cross-market analysis
    - Sector rotation signals
    - Macroeconomic indicators
    - Intelligence scoring

17. ResilientPanarchyCyclesGraph
    - Complexity cycles detection
    - Fractal scaling visualization
    - System resilience metrics
    - Adaptive capacity monitoring

18. ResilientAntenarrativeLens
    - Narrative analysis of events
    - Connects chaos signals ↔ news
    - Multi-input support
    - Credibility tiers + chaos stability
```

### TIER 4: Intelligence & AI (4 components)
```typescript
19. ResilientChatInterface
    - Floating Claude Sonnet 4.5 chat
    - Context-aware (knows your portfolio)
    - Available on ALL tabs
    - Conversation history + export

20. ResilientConstitutionalNeuralNetwork
    - Separate AI analysis engine
    - Predictions + pattern detection
    - Anomaly identification
    - Learning metrics

21. ConstitutionalRadar (5-axis Yama chart)
    - Ethical alignment monitoring
    - Per-position scoring

22. ConstitutionalScorer
    - Backend ethics calculation
    - Scores (0.0-1.0 range)
```

### TIER 5: Support & Operations (3 components)
```typescript
23. ResilientTradesFeed
    - Live trade execution feed
    - Trade reasoning + timestamps
    - Execution price tracking

24. ErrorBoundary
    - Component-level error protection
    - Graceful degradation
    - User-friendly error messages

25. RootErrorBoundary
    - Global error handling
    - System-wide crash prevention
```

---

## 🗂️ NAVIGATION TABS (8 Total)

```
1. OVERVIEW Tab
   - Header + Portfolio Panel + Performance Panel
   - Activity Panel + News Ticker
   - Constitutional Radar + TradesFeed

2. PORTFOLIO Tab
   - Detailed portfolio positions
   - Cash balances + allocation %
   - Per-position constitutional scores

3. PERFORMANCE Tab
   - Historical ROI charts
   - Sharpe ratio + Constitutional alignment
   - Fractal Optimization Panel
   - Risk Assessment Panel
   - Balances & Cash Flow

4. CHAOS Tab
   - 3D interactive Lorenz/Chen/Rössler attractors
   - Signal strength visualization
   - Antenarrative Lens (chaos ↔ news correlation)

5. MARKETS Tab
   - Global Markets Panel (8+ exchanges)
   - Market Sentiment gauge
   - Forex Panel (4+ currency pairs)
   - Advanced Analytics Panel

6. NEWS Tab
   - News Carousel (interactive cards)
   - Constitutional scoring per article
   - Source attribution
   - Auto-updating headlines

7. CHAT Tab
   - Full-screen Claude Sonnet 4.5 interface
   - Extended conversation history
   - Export functionality

8. NEURAL Tab
   - Constitutional Neural Network visualization
   - AI predictions + patterns
   - Anomaly detection + learning metrics
   - System intelligence dashboard
```

---

## 📚 KEY DATA STRUCTURES

### Portfolio Position Object:
```typescript
{
  symbol: string;           // e.g., "ASML.AS"
  quantity: number;         // Shares held
  avgPrice: number;         // Entry price
  currentPrice: number;     // Last price
  value: number;            // Current position value
  weight: number;           // % of portfolio (0.0-1.0)
  constitutionalScore: number;  // Ethics alignment (0.0-1.0)
  exchange: string;         // e.g., "Amsterdam Stock Exchange"
  country: string;          // e.g., "Netherlands"
  region: string;           // e.g., "Europe"
  gain: number;             // Unrealized P&L
  gainPercent: number;      // Unrealized % return
}
```

### Dashboard Summary:
```typescript
{
  portfolio: {
    totalValue: number;
    cash: number;
    positions: Position[];
  },
  performance: {
    roi: number;              // Return on investment %
    sharpe: number;           // Sharpe ratio
    constitutionalScore: number;  // Overall ethics (0.0-1.0)
    fractalLoveScore: number; // Fractal harmony metric
    volatility: number;       // Annual volatility
  },
  sentiment: {
    score: number;            // 0-100 scale
    bullish: number;          // % bullish
    bearish: number;          // % bearish
  },
  chaos: {
    lorenz: number[];         // 3D coordinates
    chen: number[];           // 3D coordinates
    rossler: number[];        // 3D coordinates
  }
}
```

---

## 🔌 ALL API ENDPOINTS (20+)

**Base URL:** `http://localhost:3002/api/`

```bash
# Portfolio & Holdings
GET    /api/portfolio                          # Current positions
GET    /api/dashboard                          # Summary data
GET    /api/international-portfolio            # International breakdown
GET    /api/starting-balances                  # Initial positions

# Performance & Metrics
GET    /api/performance                        # Historical ROI
GET    /api/trades                             # Trade history
GET    /api/constitutional                     # Constitutional scores

# Market Data
GET    /api/global-sentiment                   # Market sentiment (0-100)
GET    /api/cross-market-correlations          # Asset correlations
GET    /api/chaos                              # Chaos attractor signals
GET    /api/live/quotes/:symbols               # Real-time prices
GET    /api/live/news/:symbol                  # Company news

# Intelligence & Analysis
GET    /api/chat                               # Chat history
POST   /api/chat                               # Send message to Claude
GET    /api/neural                             # NN predictions
GET    /api/optimization                       # Fractal optimization suggestions
GET    /api/risk-assessment                    # Risk metrics

# System Status
GET    /api/health                             # System health check
GET    /api/status                             # Component status
```

---

## 🎯 FILE LOCATIONS

### Core Components:
```
dashboard/
├── app/page.tsx               ← 25 components + 8 tabs (main dashboard)
├── app/layout.tsx             ← Root layout
├── app/api/
│   ├── dashboard/route.ts     ← Dashboard endpoint
│   ├── chat/route.ts          ← Chat endpoint
│   ├── portfolio/route.ts     ← Portfolio endpoint
│   ├── performance/route.ts   ← Performance endpoint
│   └── ... (5 more API routes)
├── server.js                  ← Express backend (RUNNING on 3002)
├── components/
│   └── ResilientComponents.tsx ← Backup complex components
└── public/                    ← Static assets
```

### Feature Documentation:
```
dashboard/
├── FEATURE_VALIDATION_TESTS.md              ← Test procedures
├── FEATURE_RESTORATION_COMPLETE.md          ← Feature status
├── DASHBOARD_COMPLETE_FEATURE_INVENTORY.md  ← Feature listing
├── QUICKSTART_ALL_FEATURES.md               ← Feature guide
├── LAUNCH_READY_REPORT.md                   ← Deployment status
└── README.md                                ← Overview
```

### Backend Core:
```
src/
├── core/ConstitutionalMarketHarmonics.js    ← Main trading system
├── database/DatabaseManager.js              ← Data persistence
├── analysis/ConstitutionalScorer.js         ← Ethics scoring
└── attractors/ChaosAttractors.js            ← Chaos calculations
```

---

## 🚀 HOW TO ACCESS FEATURES

### 1. **View Dashboard**
```bash
http://localhost:3000
```

### 2. **Check Backend Status**
```bash
# Test API
curl http://127.0.0.1:3002/api/dashboard

# View portfolio
curl http://127.0.0.1:3002/api/international-portfolio
```

### 3. **Access Each Feature**
- **Charts:** Click any tab → Charts auto-render
- **Fractal Chat:** Click 💬 button (bottom-right) on any tab
- **Chaos Visualization:** Click "Chaos" tab
- **Neural Analysis:** Click "Neural" tab
- **Global Markets:** Click "Markets" tab

### 4. **Live Data Integration**
- Backend already connected ✅
- Mock fallback active ✅
- Real API keys can be added to `.env.local`

---

## 📊 CURRENT SYSTEM STATUS

| Component | Status | Port | Notes |
|-----------|--------|------|-------|
| Frontend (Next.js) | ✅ Running | 3000 | http://localhost:3000 |
| Backend (Express) | ✅ Running | 3002 | http://127.0.0.1:3002 |
| Chat Interface | ✅ Ready | - | Floating on all tabs |
| Charts & Graphs | ✅ Rendering | - | Chart.js active |
| Chaos Visualizer | ✅ Ready | - | 3D Canvas loaded |
| Neural Component | ✅ Ready | - | Full-screen tab available |
| Mock Data | ✅ Active | - | Portfolio: $1.25M |
| WebSocket | ✅ Ready | 3002 | Real-time updates |

---

## 🎓 NEXT STEPS TO MAXIMIZE FEATURES

1. **✅ Already Done:** Backend + Frontend connected
2. **✅ Already Done:** 25 components deployed
3. **⏳ Optional:** Add real API keys to `.env.local`:
   - `ANTHROPIC_API_KEY` for Claude chat
   - `FINNHUB_API_KEY` for live stock data
   - `ALPHA_VANTAGE_API_KEY` for market data
4. **⏳ Optional:** Deploy to production (Vercel + Node.js server)
5. **⏳ Optional:** Add real trading via paper trading API

---

**🌀 Analysis Complete - All Features Located & Documented**
