/**
 * Database Manager for Universal Bottleneck Resolver
 * Handles SQLite database operations with proper error handling and transactions
 */

const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');

class DatabaseManager {
  constructor(databasePath = './bottlenecks.db') {
    this.databasePath = databasePath;
    this.db = null;
    this.initialized = false;
  }

  /**
   * Initialize database connection and schema
   */
  async initialize() {
    if (this.initialized) return;

    return new Promise((resolve, reject) => {
      // Ensure database directory exists
      const dbDir = path.dirname(this.databasePath);
      if (!fs.existsSync(dbDir)) {
        fs.mkdirSync(dbDir, { recursive: true });
      }

      this.db = new sqlite3.Database(this.databasePath, (err) => {
        if (err) {
          reject(new Error(`Failed to connect to database: ${err.message}`));
          return;
        }

        console.log(`Connected to SQLite database: ${this.databasePath}`);
        this._initializeSchema()
          .then(() => {
            this.initialized = true;
            resolve();
          })
          .catch(reject);
      });
    });
  }

  /**
   * Initialize database schema
   */
  async _initializeSchema() {
    const schemaPath = path.join(__dirname, 'schema.sql');
    const schema = fs.readFileSync(schemaPath, 'utf8');

    return this.runTransaction(async () => {
      // Split schema into individual statements
      // Remove comments first, then split by semicolons
      const cleanSchema = schema
        .split('\n')
        .filter(line => !line.trim().startsWith('--'))
        .join('\n')
        .replace(/\/\*[\s\S]*?\*\//g, '') // Remove multi-line comments
        .trim();

      const statements = cleanSchema
        .split(';')
        .map(stmt => stmt.trim())
        .filter(stmt => stmt.length > 0);

      console.log(`Processing ${statements.length} SQL statements`);

      // Execute all statements in order
      for (const statement of statements) {
        if (statement.trim()) {
          await this.run(statement + ';');
        }
      }

      console.log('Database schema initialized successfully');
    });
  }

  /**
   * Run database transaction
   */
  async runTransaction(callback) {
    return new Promise((resolve, reject) => {
      this.db.run('BEGIN TRANSACTION', (err) => {
        if (err) {
          reject(new Error(`Failed to begin transaction: ${err.message}`));
          return;
        }

        Promise.resolve(callback())
          .then(() => {
            this.db.run('COMMIT', (commitErr) => {
              if (commitErr) {
                reject(new Error(`Failed to commit transaction: ${commitErr.message}`));
              } else {
                resolve();
              }
            });
          })
          .catch((error) => {
            this.db.run('ROLLBACK', (rollbackErr) => {
              if (rollbackErr) {
                console.error('Failed to rollback transaction:', rollbackErr);
              }
              reject(error);
            });
          });
      });
    });
  }

  /**
   * Run a single SQL statement
   */
  async run(sql, params = []) {
    return new Promise((resolve, reject) => {
      this.db.run(sql, params, function(err) {
        if (err) {
          reject(new Error(`SQL execution failed: ${err.message}\nSQL: ${sql}`));
        } else {
          resolve({ lastID: this.lastID, changes: this.changes });
        }
      });
    });
  }

  /**
   * Run a SELECT query and return all results
   */
  async getAll(sql, params = []) {
    return new Promise((resolve, reject) => {
      this.db.all(sql, params, (err, rows) => {
        if (err) {
          reject(new Error(`Query failed: ${err.message}\nSQL: ${sql}`));
        } else {
          resolve(rows);
        }
      });
    });
  }

  /**
   * Run a SELECT query and return first result
   */
  async get(sql, params = []) {
    return new Promise((resolve, reject) => {
      this.db.get(sql, params, (err, row) => {
        if (err) {
          reject(new Error(`Query failed: ${err.message}\nSQL: ${sql}`));
        } else {
          resolve(row);
        }
      });
    });
  }

  // ===== BOTTLENECK OPERATIONS =====

  /**
   * Save a bottleneck definition
   */
  async saveBottleneck(bottleneck) {
    const sql = `
      INSERT INTO bottlenecks (domain, name, description, dimensions, bottleneck_type, optimization_target)
      VALUES (?, ?, ?, ?, ?, ?)
    `;

    const result = await this.run(sql, [
      bottleneck.domain,
      bottleneck.name,
      bottleneck.description,
      bottleneck.dimensions,
      bottleneck.bottleneck_type,
      bottleneck.optimization_target
    ]);

    const bottleneckId = result.lastID;

    // Save components
    if (bottleneck.components) {
      for (const component of bottleneck.components) {
        await this.saveComponent(bottleneckId, component);
      }
    }

    // Save constraints
    if (bottleneck.constraints) {
      for (const constraint of bottleneck.constraints) {
        await this.saveConstraint(bottleneckId, constraint);
      }
    }

    return bottleneckId;
  }

  /**
   * Get bottleneck by ID
   */
  async getBottleneck(id) {
    const sql = 'SELECT * FROM bottlenecks WHERE id = ?';
    const bottleneck = await this.get(sql, [id]);

    if (!bottleneck) return null;

    // Load components and constraints
    bottleneck.components = await this.getComponents(id);
    bottleneck.constraints = await this.getConstraints(id);

    return bottleneck;
  }

  /**
   * Save a component
   */
  async saveComponent(bottleneckId, component) {
    const sql = `
      INSERT INTO components (bottleneck_id, name, type, properties)
      VALUES (?, ?, ?, ?)
    `;

    return await this.run(sql, [
      bottleneckId,
      component.name,
      component.type,
      JSON.stringify(component.properties || {})
    ]);
  }

  /**
   * Get components for a bottleneck
   */
  async getComponents(bottleneckId) {
    const sql = 'SELECT * FROM components WHERE bottleneck_id = ?';
    const components = await this.getAll(sql, [bottleneckId]);

    return components.map(comp => ({
      ...comp,
      properties: JSON.parse(comp.properties || '{}')
    }));
  }

  /**
   * Save a constraint
   */
  async saveConstraint(bottleneckId, constraint) {
    const sql = `
      INSERT INTO constraints (bottleneck_id, name, type, definition)
      VALUES (?, ?, ?, ?)
    `;

    return await this.run(sql, [
      bottleneckId,
      constraint.name,
      constraint.type,
      JSON.stringify(constraint.definition || {})
    ]);
  }

  /**
   * Get constraints for a bottleneck
   */
  async getConstraints(bottleneckId) {
    const sql = 'SELECT * FROM constraints WHERE bottleneck_id = ?';
    const constraints = await this.getAll(sql, [bottleneckId]);

    return constraints.map(constraint => ({
      ...constraint,
      definition: JSON.parse(constraint.definition || '{}')
    }));
  }

  // ===== EXPLORATION OPERATIONS =====

  /**
   * Create exploration run
   */
  async createExplorationRun(runData) {
    const sql = `
      INSERT INTO exploration_runs (bottleneck_id, attractor_type, iterations, started_at)
      VALUES (?, ?, ?, ?)
    `;

    return await this.run(sql, [
      runData.bottleneck_id,
      runData.attractor_type,
      runData.iterations,
      new Date().toISOString()
    ]);
  }

  /**
   * Complete exploration run
   */
  async completeExplorationRun(runId, results) {
    const sql = `
      UPDATE exploration_runs
      SET final_state = ?, final_fitness = ?, lyapunov_exponent = ?,
          fractal_dimension = ?, completed_at = ?
      WHERE id = ?
    `;

    return await this.run(sql, [
      JSON.stringify(results.final_state || []),
      results.final_fitness || 0,
      results.lyapunov_exponent || 0,
      results.fractal_dimension || 0,
      new Date().toISOString(),
      runId
    ]);
  }

  /**
   * Save exploration checkpoint
   */
  async saveCheckpoint(checkpointData) {
    const sql = `
      INSERT INTO exploration_checkpoints (run_id, iteration, state, fitness, lyapunov, fractal_dim)
      VALUES (?, ?, ?, ?, ?, ?)
    `;

    return await this.run(sql, [
      checkpointData.run_id,
      checkpointData.iteration,
      JSON.stringify(checkpointData.state || []),
      checkpointData.fitness || 0,
      checkpointData.lyapunov || 0,
      checkpointData.fractal_dim || 0
    ]);
  }

  // ===== SOLUTION OPERATIONS =====

  /**
   * Save solution
   */
  async saveSolution(solutionData) {
    const sql = `
      INSERT INTO solutions (bottleneck_id, run_id, configuration, fitness, stability_score,
                            improvement_factor, estimated_economic_impact, validation_status)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `;

    const result = await this.run(sql, [
      solutionData.bottleneck_id,
      solutionData.run_id,
      JSON.stringify(solutionData.configuration || {}),
      solutionData.fitness || 0,
      solutionData.stability_score || 0,
      solutionData.improvement_factor || 1,
      solutionData.estimated_economic_impact || 0,
      solutionData.validation_status || 'pending'
    ]);

    return result.lastID;
  }

  /**
   * Get solution by ID
   */
  async getSolution(id) {
    const sql = 'SELECT * FROM solutions WHERE id = ?';
    const solution = await this.get(sql, [id]);

    if (!solution) return null;

    // Parse JSON fields
    solution.configuration = JSON.parse(solution.configuration || '{}');

    return solution;
  }

  // ===== DEPLOYMENT OPERATIONS =====

  /**
   * Save deployment plan
   */
  async saveDeploymentPlan(planData) {
    const sql = `
      INSERT INTO deployment_plans (solution_id, plan_steps, estimated_timeline,
                                  estimated_cost, risk_assessment, status)
      VALUES (?, ?, ?, ?, ?, ?)
    `;

    const result = await this.run(sql, [
      planData.solution_id,
      JSON.stringify(planData.plan_steps || []),
      planData.estimated_timeline || '',
      planData.estimated_cost || 0,
      JSON.stringify(planData.risk_assessment || {}),
      planData.status || 'draft'
    ]);

    return result.lastID;
  }

  // ===== TEMPLATE OPERATIONS =====

  /**
   * Save domain template
   */
  async saveDomainTemplate(template) {
    const sql = `
      INSERT OR REPLACE INTO domain_templates (domain, template_definition, typical_dimensions,
                                             common_constraints, success_metrics, example_applications)
      VALUES (?, ?, ?, ?, ?, ?)
    `;

    return await this.run(sql, [
      template.domain,
      JSON.stringify(template.template_definition || {}),
      template.typical_dimensions || 0,
      JSON.stringify(template.common_constraints || []),
      JSON.stringify(template.success_metrics || {}),
      template.example_applications || ''
    ]);
  }

  /**
   * Get domain templates
   */
  async getDomainTemplates() {
    const sql = 'SELECT * FROM domain_templates';
    const templates = await this.getAll(sql);

    return templates.map(template => ({
      ...template,
      template_definition: JSON.parse(template.template_definition || '{}'),
      common_constraints: JSON.parse(template.common_constraints || '[]'),
      success_metrics: JSON.parse(template.success_metrics || '{}')
    }));
  }

  /**
   * Get domain template by domain
   */
  async getDomainTemplate(domain) {
    const sql = 'SELECT * FROM domain_templates WHERE domain = ?';
    const template = await this.get(sql, [domain]);

    if (!template) return null;

    return {
      ...template,
      template_definition: JSON.parse(template.template_definition || '{}'),
      common_constraints: JSON.parse(template.common_constraints || '[]'),
      success_metrics: JSON.parse(template.success_metrics || '{}')
    };
  }

  // ===== ECONOMIC IMPACT OPERATIONS =====

  /**
   * Save economic impact
   */
  async saveEconomicImpact(impactData) {
    const sql = `
      INSERT INTO economic_impacts (solution_id, domain, market_size, estimated_value_creation,
                                   actual_value_creation, beneficiaries, deployment_locations)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `;

    return await this.run(sql, [
      impactData.solution_id,
      impactData.domain,
      impactData.market_size || 0,
      impactData.estimated_value_creation || 0,
      impactData.actual_value_creation || 0,
      impactData.beneficiaries || 0,
      impactData.deployment_locations || ''
    ]);
  }

  /**
   * Close database connection
   */
  close() {
    if (this.db) {
      this.db.close((err) => {
        if (err) {
          console.error('Error closing database:', err);
        } else {
          console.log('Database connection closed');
        }
      });
    }
  }
}

module.exports = DatabaseManager;