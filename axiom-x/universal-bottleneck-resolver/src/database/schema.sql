-- Universal Bottleneck Resolver Database Schema
-- SQLite 3.0+ compatible

-- Bottleneck definitions
CREATE TABLE IF NOT EXISTS bottlenecks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  domain TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  dimensions INTEGER NOT NULL,
  bottleneck_type TEXT NOT NULL,
  optimization_target TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Components (stakeholders, resources, agents)
CREATE TABLE IF NOT EXISTS components (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bottleneck_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  type TEXT NOT NULL, -- 'agent', 'resource', 'stakeholder'
  properties JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (bottleneck_id) REFERENCES bottlenecks(id) ON DELETE CASCADE
);

-- Constraints
CREATE TABLE IF NOT EXISTS constraints (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bottleneck_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  type TEXT NOT NULL, -- 'hard', 'soft', 'preference'
  definition JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (bottleneck_id) REFERENCES bottlenecks(id) ON DELETE CASCADE
);

-- Chaos exploration runs
CREATE TABLE IF NOT EXISTS exploration_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bottleneck_id INTEGER NOT NULL,
  attractor_type TEXT NOT NULL, -- 'lorenz', 'chen', 'rossler'
  iterations INTEGER NOT NULL,
  final_state JSON,
  final_fitness REAL,
  lyapunov_exponent REAL,
  fractal_dimension REAL,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (bottleneck_id) REFERENCES bottlenecks(id) ON DELETE CASCADE
);

-- Exploration history (checkpoints every N iterations)
CREATE TABLE IF NOT EXISTS exploration_checkpoints (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id INTEGER NOT NULL,
  iteration INTEGER NOT NULL,
  state JSON,
  fitness REAL,
  lyapunov REAL,
  fractal_dim REAL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (run_id) REFERENCES exploration_runs(id) ON DELETE CASCADE
);

-- Solutions (best configurations found)
CREATE TABLE IF NOT EXISTS solutions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bottleneck_id INTEGER NOT NULL,
  run_id INTEGER NOT NULL,
  configuration JSON,
  fitness REAL,
  stability_score REAL,
  improvement_factor REAL,
  estimated_economic_impact REAL,
  validation_status TEXT DEFAULT 'pending', -- 'pending', 'validated', 'failed'
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (bottleneck_id) REFERENCES bottlenecks(id) ON DELETE CASCADE,
  FOREIGN KEY (run_id) REFERENCES exploration_runs(id) ON DELETE CASCADE
);

-- Deployment plans
CREATE TABLE IF NOT EXISTS deployment_plans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  solution_id INTEGER NOT NULL,
  plan_steps JSON,
  estimated_timeline TEXT,
  estimated_cost REAL,
  risk_assessment JSON,
  status TEXT DEFAULT 'draft', -- 'draft', 'approved', 'deployed', 'validated'
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (solution_id) REFERENCES solutions(id) ON DELETE CASCADE
);

-- Validation results (after deployment)
CREATE TABLE IF NOT EXISTS validation_results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  solution_id INTEGER NOT NULL,
  deployment_plan_id INTEGER,
  actual_improvement REAL,
  actual_economic_impact REAL,
  sustained_performance JSON, -- time series
  degradation_percentage REAL,
  lessons_learned TEXT,
  validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (solution_id) REFERENCES solutions(id) ON DELETE CASCADE,
  FOREIGN KEY (deployment_plan_id) REFERENCES deployment_plans(id) ON DELETE CASCADE
);

-- Domain templates (predefined mappings for common domains)
CREATE TABLE IF NOT EXISTS domain_templates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  domain TEXT UNIQUE NOT NULL,
  template_definition JSON,
  typical_dimensions INTEGER,
  common_constraints JSON,
  success_metrics JSON,
  example_applications TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Economic impact tracking
CREATE TABLE IF NOT EXISTS economic_impacts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  solution_id INTEGER NOT NULL,
  domain TEXT NOT NULL,
  market_size REAL,
  estimated_value_creation REAL,
  actual_value_creation REAL,
  beneficiaries INTEGER,
  deployment_locations TEXT,
  measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (solution_id) REFERENCES solutions(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_bottlenecks_domain ON bottlenecks(domain);
CREATE INDEX IF NOT EXISTS idx_bottlenecks_created ON bottlenecks(created_at);
CREATE INDEX IF NOT EXISTS idx_exploration_runs_bottleneck ON exploration_runs(bottleneck_id);
CREATE INDEX IF NOT EXISTS idx_exploration_runs_attractor ON exploration_runs(attractor_type);
CREATE INDEX IF NOT EXISTS idx_solutions_bottleneck ON solutions(bottleneck_id);
CREATE INDEX IF NOT EXISTS idx_solutions_fitness ON solutions(fitness DESC);
CREATE INDEX IF NOT EXISTS idx_checkpoints_run ON exploration_checkpoints(run_id);
CREATE INDEX IF NOT EXISTS idx_checkpoints_iteration ON exploration_checkpoints(iteration);