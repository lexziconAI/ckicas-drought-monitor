-- Constitutional Market Harmonics Database Schema
-- SQLite 3.0+ compatible

-- Constitutional company scores
CREATE TABLE IF NOT EXISTS constitutional_scores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticker TEXT UNIQUE NOT NULL,
  company_name TEXT,
  overall_score REAL NOT NULL, -- 0.0 to 1.0
  ahimsa_score REAL NOT NULL, -- Non-harm principle
  satya_score REAL NOT NULL, -- Truthfulness principle
  asteya_score REAL NOT NULL, -- Non-stealing principle
  brahmacharya_score REAL NOT NULL, -- Self-discipline principle
  aparigraha_score REAL NOT NULL, -- Non-hoarding principle
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  data_sources TEXT, -- JSON array of data sources
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Portfolio positions (paper trading)
CREATE TABLE IF NOT EXISTS portfolio_positions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticker TEXT NOT NULL,
  shares REAL NOT NULL,
  average_cost REAL NOT NULL,
  current_value REAL NOT NULL,
  entry_date TIMESTAMP NOT NULL,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(ticker)
);

-- Trading history
CREATE TABLE IF NOT EXISTS trades (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticker TEXT NOT NULL,
  action TEXT NOT NULL, -- 'buy', 'sell'
  shares REAL NOT NULL,
  price REAL NOT NULL,
  amount REAL NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  strategy TEXT, -- Which attractor strategy triggered this
  constitutional_score REAL, -- Constitutional score at time of trade
  notes TEXT
);

-- Market data cache
CREATE TABLE IF NOT EXISTS market_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticker TEXT NOT NULL,
  date DATE NOT NULL,
  open REAL,
  high REAL,
  low REAL,
  close REAL NOT NULL,
  volume INTEGER,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(ticker, date)
);

-- Performance tracking
CREATE TABLE IF NOT EXISTS performance_metrics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATE NOT NULL,
  portfolio_value REAL NOT NULL,
  cash_balance REAL NOT NULL,
  roi REAL NOT NULL,
  sharpe_ratio REAL,
  max_drawdown REAL,
  win_rate REAL,
  total_trades INTEGER DEFAULT 0,
  constitutional_alignment REAL, -- Portfolio-wide alignment score
  downstream_value REAL, -- Estimated downstream impact
  combined_score REAL, -- ROI × Constitutional Impact
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(date)
);

-- Trading signals (for analysis)
CREATE TABLE IF NOT EXISTS trading_signals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  strategy TEXT NOT NULL, -- 'lorenz', 'chen', 'rossler', 'ensemble'
  ticker TEXT NOT NULL,
  signal_type TEXT NOT NULL, -- 'buy', 'sell', 'hold'
  strength REAL NOT NULL, -- 0.0 to 1.0
  market_state TEXT, -- JSON of market conditions
  constitutional_score REAL,
  executed BOOLEAN DEFAULT FALSE,
  execution_price REAL,
  execution_timestamp TIMESTAMP
);

-- Chaos attractor states (for analysis)
CREATE TABLE IF NOT EXISTS attractor_states (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  attractor_type TEXT NOT NULL, -- 'lorenz', 'chen', 'rossler'
  state_vector TEXT NOT NULL, -- JSON array of state values
  lyapunov_exponent REAL,
  fractal_dimension REAL,
  market_context TEXT -- JSON of market conditions
);

-- Counterfactual impact calculations
CREATE TABLE IF NOT EXISTS counterfactual_impacts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticker TEXT NOT NULL,
  position_size REAL NOT NULL, -- Hypothetical position size
  scale_factor REAL NOT NULL, -- How much larger than actual
  direct_impact REAL, -- Price impact
  downstream_impact REAL, -- Network effects
  constitutional_signal REAL, -- Ethical signaling value
  calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System configuration
CREATE TABLE IF NOT EXISTS system_config (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_constitutional_scores_ticker ON constitutional_scores(ticker);
CREATE INDEX IF NOT EXISTS idx_portfolio_positions_ticker ON portfolio_positions(ticker);
CREATE INDEX IF NOT EXISTS idx_trades_ticker ON trades(ticker);
CREATE INDEX IF NOT EXISTS idx_trades_timestamp ON trades(timestamp);
CREATE INDEX IF NOT EXISTS idx_market_data_ticker_date ON market_data(ticker, date);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_date ON performance_metrics(date);
CREATE INDEX IF NOT EXISTS idx_trading_signals_timestamp ON trading_signals(timestamp);
CREATE INDEX IF NOT EXISTS idx_attractor_states_timestamp ON attractor_states(timestamp);