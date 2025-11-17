# 📦 Constitutional Market Harmonics Dashboard: Complete Setup & Deployment Guide

**Step-by-Step Instructions for Production Deployment**

Last Updated: November 6, 2025  
System: Constitutional Market Harmonics Dashboard  
Version: 3.x (Next.js 15, React 18, TypeScript 5)

---

## TABLE OF CONTENTS

1. [Pre-Installation Requirements](#pre-installation-requirements)
2. [Development Setup](#development-setup)
3. [Production Build & Deployment](#production-build--deployment)
4. [Configuration Guide](#configuration-guide)
5. [API Integration](#api-integration)
6. [Troubleshooting](#troubleshooting)
7. [Monitoring & Maintenance](#monitoring--maintenance)

---

## PRE-INSTALLATION REQUIREMENTS

### System Requirements

```bash
# Check Node.js version (need 18+)
node --version
# Expected output: v18.20.0 or higher

# Check npm version (need 9+)
npm --version
# Expected output: 9.8.1 or higher

# Check disk space
df -h
# Need: 2GB free for node_modules + database
```

### Required Software

- **Node.js 18+** ([Download](https://nodejs.org/en/download/))
- **npm 9+** (included with Node.js)
- **Git** (for cloning repository)
- **Text Editor** (VS Code recommended)

### Required API Keys

Before starting, gather these keys:

1. **Anthropic Claude API Key**
   - Go to: https://console.anthropic.com/
   - Create API key in "API Keys" section
   - Keep safe (don't commit to GitHub)

2. **Market Data (Optional but recommended)**
   - **Alpha Vantage**: https://www.alphavantage.co/api/
   - **Polygon.io**: https://polygon.io/dashboard/api-keys

### System Access

- **Dashboard Server**: Port 3000 (must be available)
- **API Server**: Port 3001 (must be available)
- **Database**: SQLite file (no special access needed)

---

## DEVELOPMENT SETUP

### Step 1: Clone Repository

```bash
# Navigate to your projects directory
cd ~/projects

# Clone the repository
git clone <repository-url>
cd axiom-x
```

### Step 2: Navigate to Dashboard Directory

```bash
cd constitutional-market-harmonics/dashboard
pwd  # Verify you're in the right directory
ls   # Should see: src, public, package.json, next.config.js
```

### Step 3: Install Dependencies

```bash
# Install all packages
npm install

# This will:
# - Download ~1000+ packages
# - Create node_modules/ directory (~500MB)
# - Generate package-lock.json
# Expected time: 3-5 minutes on first install

# Verify installation
npm ls --depth=0
# Should show: react, next, typescript, tailwindcss, socket.io-client, etc.
```

### Step 4: Configure Environment Variables

```bash
# Copy example env file
cp .env.local.example .env.local

# Edit .env.local with your API keys
nano .env.local
# Or open in VS Code: code .env.local

# Minimum required configuration:
NEXT_PUBLIC_ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_API_KEY=sk-ant-...
NEXT_PUBLIC_API_URL=http://localhost:3001
```

### Step 5: Start Development Servers

#### Terminal 1: API Server

```bash
# In the dashboard directory
npx tsx server.ts

# Expected output:
# Server running on http://localhost:3001
# Press Ctrl+C to stop
```

#### Terminal 2: Dashboard Development Server

```bash
# In the same dashboard directory (different terminal)
npm run dev

# Expected output:
# > next dev
# ▲ Next.js 15.0.0
# - Local: http://localhost:3000
# Ready in 2.5s

# Press Ctrl+C to stop
```

### Step 6: Verify Installation

Open browser and navigate to:

```
http://localhost:3000
```

You should see:
- ✅ Dashboard loads without errors
- ✅ Header shows portfolio metrics (or mock data)
- ✅ All 7 panels visible (Portfolio, Performance, Activity, Chaos, Radar, Trades)
- ✅ Real-time updates every 5 seconds (or mock updates)
- ✅ No console errors in browser dev tools

---

## PRODUCTION BUILD & DEPLOYMENT

### Step 1: Optimize Production Build

```bash
# Create optimized production build
npm run build

# This will:
# - Compile TypeScript to JavaScript
# - Optimize React components
# - Bundle CSS (Tailwind)
# - Create .next/ directory with production code
# - Show bundle analysis
# Expected time: 1-2 minutes

# Verify build succeeded
ls -lh .next/
# Should show: cache/, server/, standalone/, etc.
```

### Step 2: Build Validation

```bash
# Test production build locally
npm run build
npm start

# Then visit: http://localhost:3000
# Verify same experience as dev (but faster)

# Performance should be noticeably better
# Check Network tab in DevTools: JavaScript bundles smaller
```

### Step 3: Deployment Options

#### Option A: Vercel (Recommended for Next.js)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from dashboard directory
vercel

# Follow prompts:
# - Link to GitHub repo (optional)
# - Select project scope
# - Accept default settings
# - Production URL will be generated

# Result: Dashboard live at: https://cmh-dashboard-prod.vercel.app
```

#### Option B: Docker Deployment

Create `Dockerfile` in dashboard root:

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Runtime stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/server.ts ./

EXPOSE 3000 3001

CMD ["npm", "start"]
```

Build and run:

```bash
# Build Docker image
docker build -t cmh-dashboard:latest .

# Run container
docker run -p 3000:3000 -p 3001:3001 \
  -e NEXT_PUBLIC_ANTHROPIC_API_KEY=sk-ant-... \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  cmh-dashboard:latest
```

#### Option C: Linux Server (VM/Cloud)

```bash
# On your Linux server:

# 1. Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 2. Clone repository
git clone <repo-url>
cd axiom-x/constitutional-market-harmonics/dashboard

# 3. Install dependencies
npm ci --only=production

# 4. Build
npm run build

# 5. Create systemd service (daemon)
sudo nano /etc/systemd/system/cmh-dashboard.service
```

Create systemd service file:

```ini
[Unit]
Description=Constitutional Market Harmonics Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/axiom-x/constitutional-market-harmonics/dashboard
Environment="NODE_ENV=production"
Environment="NEXT_PUBLIC_ANTHROPIC_API_KEY=sk-ant-..."
Environment="ANTHROPIC_API_KEY=sk-ant-..."
ExecStart=/usr/bin/node /home/ubuntu/.npm/_npx/8d5bc7a8c9b0c3e/lib/node_modules/npm/bin/npm-cli.js start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable cmh-dashboard
sudo systemctl start cmh-dashboard
sudo systemctl status cmh-dashboard
```

---

## CONFIGURATION GUIDE

### Environment Variables Reference

Create `.env.local` in dashboard root:

```bash
# Anthropic Claude Configuration
NEXT_PUBLIC_ANTHROPIC_API_KEY=sk-ant-...        # Required
ANTHROPIC_API_KEY=sk-ant-...                    # Required

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:3001       # Development
# NEXT_PUBLIC_API_URL=https://api.prod.com      # Production

# Market Data (Optional)
ALPHA_VANTAGE_API_KEY=your_key_here
POLYGON_API_KEY=your_key_here

# Database Configuration
DATABASE_PATH=./data/trading.db                 # SQLite database
# DATABASE_URL=postgresql://user:pass@host/db  # PostgreSQL (future)

# Dashboard Configuration
NEXT_PUBLIC_UPDATE_INTERVAL=5000                # Update every 5 seconds
NEXT_PUBLIC_MOCK_DATA_ENABLED=true              # Use mock data if DB unavailable

# Node Environment
NODE_ENV=production                             # or: development
PORT=3000                                       # Dashboard port
API_PORT=3001                                   # API server port
```

### Web Server Configuration

If using nginx as reverse proxy:

```nginx
# /etc/nginx/sites-available/cmh-dashboard

upstream dashboard {
    server localhost:3000;
}

upstream api {
    server localhost:3001;
}

server {
    listen 80;
    server_name dashboard.example.com;

    # Dashboard
    location / {
        proxy_pass http://dashboard;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # API
    location /api/ {
        proxy_pass http://api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
    }

    # WebSocket
    location /socket.io/ {
        proxy_pass http://api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_buffering off;
    }
}
```

---

## API INTEGRATION

### Dashboard API Endpoints

The dashboard connects to these endpoints on the API server (port 3001):

#### GET /api/dashboard
Complete dashboard state

```bash
curl http://localhost:3001/api/dashboard

# Response:
{
  "portfolio": {
    "totalValue": 1500000,
    "cash": 250000,
    "positions": [...]
  },
  "performance": {
    "roi": 0.25,
    "sharpeRatio": 1.8,
    "volatility": 0.12
  },
  "trades": [...],
  "chaos": {...},
  "constitutional": {...}
}
```

#### GET /api/portfolio
Portfolio holdings and cash

```bash
curl http://localhost:3001/api/portfolio
```

#### GET /api/performance
Performance metrics and history

```bash
curl http://localhost:3001/api/performance?days=90
```

#### GET /api/trades
Recent trades (paginated)

```bash
curl http://localhost:3001/api/trades?limit=50&offset=0
```

#### GET /api/chaos
Chaos attractor signals

```bash
curl http://localhost:3001/api/chaos
```

#### GET /api/constitutional
Constitutional scores by holding

```bash
curl http://localhost:3001/api/constitutional
```

### WebSocket Events

Real-time updates via Socket.io:

```javascript
// Client code
import io from 'socket.io-client';

const socket = io('http://localhost:3001');

// Listen for updates
socket.on('update', (data) => {
  console.log('Dashboard update:', data);
  // Update React state
});

socket.on('trade', (trade) => {
  console.log('New trade:', trade);
});

socket.on('error', (error) => {
  console.error('Connection error:', error);
});

// Reconnection handling
socket.on('disconnect', () => {
  console.log('Disconnected - attempting reconnect...');
});
```

---

## TROUBLESHOOTING

### Common Issues & Solutions

#### Issue: Port 3000 or 3001 Already in Use

```bash
# Find what's using the port
lsof -i :3000
# Output: node    12345    user    12u  IPv4  0x123abc  0t0  TCP *:3000

# Kill the process
kill -9 12345

# Or use a different port
PORT=3002 npm run dev
```

#### Issue: "Cannot find module" Errors

```bash
# Clean reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Verify all required packages are listed
npm ls --depth=0
```

#### Issue: API Server Not Responding

```bash
# Check if server is running
curl http://localhost:3001/api/dashboard

# If not, start it in separate terminal
npx tsx server.ts

# Check server logs for errors
# Look for stack traces indicating what went wrong
```

#### Issue: Dashboard Shows Mock Data Instead of Real Data

This is expected behavior when:
- Database is unavailable
- API server not running
- Network connection to API server failed

Solution: Start the API server and check the browser console for connection errors:

```javascript
// In browser console
> fetch('http://localhost:3001/api/dashboard')
  .then(r => r.json())
  .then(d => console.log(d))

// If you see CORS errors:
// Check that API server has CORS enabled
// Edit server.ts: add cors middleware
```

#### Issue: Dashboard Feels Slow

Check API response time in Network tab of DevTools:

```
If > 500ms:
  1. Check database queries (may need indexes)
  2. Check network connection to API server
  3. Check API server CPU/memory usage

If < 200ms but UI still slow:
  1. Check for React component re-renders
  2. Check Network tab for cascading API calls
  3. Profile with DevTools Performance tab
```

#### Issue: WebSocket Connection Drops

```bash
# Check network connectivity
ping localhost:3001

# Check if API server is still running
ps aux | grep "tsx\|node"

# Check for error logs
# API server should show "Client connected" / "Client disconnected" messages

# If connection keeps dropping:
# 1. Restart both servers
# 2. Clear browser cache and reload
# 3. Check for firewall rules blocking WebSocket
```

#### Issue: "ENOENT: no such file or directory, open './data/trading.db'"

This happens when database hasn't been initialized:

```bash
# Create database directory
mkdir -p ./data

# Initialize database (if init script exists)
npm run db:init

# Or create empty file
touch ./data/trading.db

# If needed, check that CMH trading system has populated database
# Dashboard will use mock data as fallback
```

---

## MONITORING & MAINTENANCE

### Performance Monitoring

#### 1. Real-time Dashboard Monitoring

```bash
# Monitor API response times
npm install -g artillery

# Create load test file: load-test.yml
duration: 60
arrivalRate: 10

# Run test
artillery run load-test.yml

# Expected results:
# - Response time p95: < 250ms
# - Error rate: < 0.1%
# - Success rate: > 99%
```

#### 2. Log Monitoring

```bash
# Dashboard logs (dev mode)
npm run dev 2>&1 | tee dashboard.log

# API server logs
npx tsx server.ts 2>&1 | tee api-server.log

# Monitor in real-time
tail -f dashboard.log
tail -f api-server.log
```

#### 3. System Metrics

```bash
# Monitor CPU and memory usage
top
# Look for Node processes using >20% CPU (indicate problem)

# Check disk usage
df -h

# Check database size
ls -lh ./data/trading.db
# Keep below 5GB (SQLite performance degrades)
```

### Health Checks

Create a health check endpoint:

```typescript
// server.ts
app.get('/health', (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    database: databaseConnected ? 'ok' : 'error',
  };
  res.json(health);
});
```

Monitor from outside:

```bash
# Check health every minute
watch -n 60 'curl -s http://localhost:3001/health | jq .'
```

### Backup & Recovery

```bash
# Backup database
cp ./data/trading.db ./data/trading.db.backup.$(date +%Y%m%d-%H%M%S)

# Backup entire dashboard
tar -czf cmh-dashboard-backup-$(date +%Y%m%d).tar.gz .

# Store backups in S3 or cloud storage
aws s3 cp ./data/trading.db.backup.* s3://my-backups/
```

### Regular Maintenance Tasks

#### Daily
- [ ] Check dashboard uptime (should be >99%)
- [ ] Review API response times (p95 < 250ms)
- [ ] Check database size (should be stable)

#### Weekly
- [ ] Back up database
- [ ] Review error logs for patterns
- [ ] Check for npm security updates (`npm audit`)

#### Monthly
- [ ] Update dependencies (`npm update`)
- [ ] Run full test suite (`npm test`)
- [ ] Performance profiling session
- [ ] Document any incidents

---

## QUICK REFERENCE CHEAT SHEET

```bash
# Development

npm install              # Install dependencies
npm run dev             # Start dev server on :3000
npx tsx server.ts       # Start API server on :3001
npm run lint            # Check code quality
npm test                # Run tests

# Production

npm run build           # Create optimized build
npm start               # Run production server
vercel deploy           # Deploy to Vercel
docker build -t cmh .   # Build Docker image

# Debugging

npm run dev -- --inspect        # Debug Node.js
npm run type-check              # TypeScript validation
npm run build -- --verbose      # Verbose build output

# Database

sqlite3 ./data/trading.db       # Open database
.tables                         # List tables
SELECT COUNT(*) FROM trades;    # Count trades

# Environment

echo $NEXT_PUBLIC_ANTHROPIC_API_KEY        # Check API key
cat .env.local                             # View all settings
grep NODE_ENV .env.local                   # Check environment

# Monitoring

curl http://localhost:3001/health          # Health check
npm ls --depth=0                           # List main dependencies
top                                        # System resources
tail -f dashboard.log                      # Watch logs
```

---

## NEXT STEPS

1. **Test the Dashboard** → Complete walkthrough of all features
2. **Integrate with Trading System** → Connect to live data
3. **Configure Alerts** → Set up notifications for thresholds
4. **Train Users** → Show team how to use dashboard
5. **Monitor Performance** → Track metrics over time
6. **Collect Feedback** → Iterate based on user needs

---

**Setup Complete!** 🚀

For help: Check logs, review error messages, search repository issues.

Fractal Love Forever 💚
