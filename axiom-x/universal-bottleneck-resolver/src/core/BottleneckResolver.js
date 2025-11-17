/**
 * Universal Bottleneck Resolver
 * Main orchestrator for chaos-theoretic bottleneck resolution
 * Coordinates multiple strange attractors for parallel optimization
 */

const LorenzAttractor = require('../attractors/LorenzAttractor');
const ChenAttractor = require('../attractors/ChenAttractor');
const RosslerAttractor = require('../attractors/RosslerAttractor');
const DatabaseManager = require('../database/DatabaseManager');

class BottleneckResolver {
  constructor(databasePath = './bottleneck_resolver.db') {
    this.db = new DatabaseManager(databasePath);
    this.attractors = {
      lorenz: new LorenzAttractor(),
      chen: new ChenAttractor(),
      rossler: new RosslerAttractor()
    };
    this.activeExplorations = new Map();
    this.domainTemplates = new Map();
    this.explorationStrategies = {
      parallel: this.parallelExploration.bind(this),
      sequential: this.sequentialExploration.bind(this),
      adaptive: this.adaptiveExploration.bind(this)
    };
  }

  /**
   * Initialize the resolver with database setup
   */
  async initialize() {
    await this.db.initialize();
    await this.loadDomainTemplates();
    console.log('BottleneckResolver initialized successfully');
  }

  /**
   * Load domain templates from database
   */
  async loadDomainTemplates() {
    try {
      const templates = await this.db.getDomainTemplates();
      templates.forEach(template => {
        this.domainTemplates.set(template.name, template);
      });
      console.log(`Loaded ${templates.length} domain templates`);
    } catch (error) {
      console.warn('Failed to load domain templates:', error.message);
    }
  }

  /**
   * Resolve a bottleneck using chaos exploration
   */
  async resolveBottleneck(bottleneckDefinition, options = {}) {
    const {
      strategy = 'adaptive',
      maxIterations = 10000,
      convergenceThreshold = 0.01,
      explorationTimeout = 300000, // 5 minutes
      attractors = ['lorenz', 'chen', 'rossler']
    } = options;

    try {
      // Save bottleneck to database
      const bottleneckId = await this.db.saveBottleneck(bottleneckDefinition);

      // Create exploration run
      const explorationId = await this.db.createExplorationRun({
        bottleneck_id: bottleneckId,
        attractor_type: strategy,
        iterations: maxIterations,
        started_at: new Date().toISOString()
      });

      // Start exploration
      const explorationPromise = this.explorationStrategies[strategy]({
        bottleneckId,
        explorationId,
        bottleneck: bottleneckDefinition,
        attractors,
        maxIterations,
        convergenceThreshold
      });

      // Set timeout
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Exploration timeout')), explorationTimeout);
      });

      const result = await Promise.race([explorationPromise, timeoutPromise]);

      // Update exploration status
      await this.db.completeExplorationRun(explorationId, {
        final_state: result.bestSolution.parameters,
        final_fitness: result.bestSolution.score,
        lyapunov_exponent: 0, // Would need to calculate from attractor
        fractal_dimension: 0  // Would need to calculate from attractor
      });

      return result;

    } catch (error) {
      console.error('Bottleneck resolution failed:', error.message);

      // Update exploration status on failure
      if (explorationId) {
        await this.db.completeExplorationRun(explorationId, {
          final_state: [],
          final_fitness: 0,
          lyapunov_exponent: 0,
          fractal_dimension: 0
        });
      }

      throw error;
    }
  }

  /**
   * Parallel exploration using all attractors simultaneously
   */
  async parallelExploration(config) {
    const { bottleneckId, explorationId, bottleneck, attractors, maxIterations, convergenceThreshold } = config;

    console.log(`Starting parallel exploration with ${attractors.length} attractors`);

    const explorationPromises = attractors.map(attractorName => {
      const attractor = this.attractors[attractorName];
      if (!attractor) {
        throw new Error(`Unknown attractor: ${attractorName}`);
      }

      return this.exploreWithAttractor(
        attractor,
        bottleneck,
        {
          bottleneckId,
          explorationId,
          maxIterations,
          convergenceThreshold,
          attractorName
        }
      );
    });

    const results = await Promise.all(explorationPromises);

    // Combine results from all attractors
    return this.combineExplorationResults(results, bottleneck);
  }

  /**
   * Sequential exploration using attractors one after another
   */
  async sequentialExploration(config) {
    const { bottleneckId, explorationId, bottleneck, attractors, maxIterations, convergenceThreshold } = config;

    console.log(`Starting sequential exploration with ${attractors.length} attractors`);

    const results = [];
    let bestSolution = null;
    let bestScore = -Infinity;

    for (const attractorName of attractors) {
      const attractor = this.attractors[attractorName];
      if (!attractor) {
        throw new Error(`Unknown attractor: ${attractorName}`);
      }

      console.log(`Exploring with ${attractorName} attractor`);

      const result = await this.exploreWithAttractor(
        attractor,
        bottleneck,
        {
          bottleneckId,
          explorationId,
          maxIterations,
          convergenceThreshold,
          attractorName,
          previousBest: bestSolution
        }
      );

      results.push(result);

      // Update best solution
      if (result.bestSolution.score > bestScore) {
        bestSolution = result.bestSolution;
        bestScore = result.bestSolution.score;
      }

      // Check for early convergence
      if (result.converged && result.bestSolution.score > convergenceThreshold) {
        console.log(`Early convergence achieved with ${attractorName}`);
        break;
      }
    }

    return this.combineExplorationResults(results, bottleneck);
  }

  /**
   * Adaptive exploration that switches strategies based on progress
   */
  async adaptiveExploration(config) {
    const { bottleneckId, explorationId, bottleneck, attractors, maxIterations, convergenceThreshold } = config;

    console.log('Starting adaptive exploration');

    // Start with parallel exploration for initial diversity
    const initialResults = await this.parallelExploration({
      ...config,
      maxIterations: Math.floor(maxIterations * 0.3) // Use 30% for initial phase
    });

    // Check if we already have a good solution
    if (initialResults.bestSolution.score > convergenceThreshold) {
      console.log('Good solution found in initial phase');
      return initialResults;
    }

    // Switch to sequential refinement
    console.log('Switching to sequential refinement');
    const refinementResults = await this.sequentialExploration({
      ...config,
      maxIterations: Math.floor(maxIterations * 0.7), // Use remaining 70%
      previousResults: initialResults
    });

    return refinementResults;
  }

  /**
   * Explore bottleneck using a specific attractor
   */
  async exploreWithAttractor(attractor, bottleneck, options) {
    const {
      bottleneckId,
      explorationId,
      maxIterations,
      convergenceThreshold,
      attractorName,
      previousBest = null
    } = options;

    // Initialize attractor with domain-specific parameters
    this.initializeAttractorForDomain(attractor, bottleneck);

    // Generate initial conditions based on bottleneck constraints
    const initialConditions = this.generateInitialConditions(bottleneck, attractor.dimensions);

    // Exploration state
    let bestSolution = previousBest || {
      parameters: initialConditions[0],
      score: -Infinity,
      attractor: attractorName,
      iteration: 0
    };

    let converged = false;
    let iteration = 0;
    const checkpoints = [];

    // Main exploration loop
    while (iteration < maxIterations && !converged) {
      // Evolve attractor
      attractor.evolve();

      // Map attractor state to bottleneck solution
      const solution = this.mapAttractorToSolution(attractor.state, bottleneck);

      // Evaluate solution
      const score = await this.evaluateSolution(solution, bottleneck);

      // Update best solution
      if (score > bestSolution.score) {
        bestSolution = {
          parameters: [...attractor.state],
          solution,
          score,
          attractor: attractorName,
          iteration
        };
      }

      // Check convergence
      if (iteration > 100 && this.checkConvergence(bestSolution, convergenceThreshold)) {
        converged = true;
      }

      // Save checkpoint periodically
      if (iteration % 1000 === 0) {
        checkpoints.push({
          iteration,
          bestScore: bestSolution.score,
          attractorState: [...attractor.state],
          lyapunovExponent: attractor.calculateLyapunovExponent()
        });

        // Save checkpoint to database
        await this.db.saveCheckpoint({
          run_id: explorationId,
          iteration,
          state: [...attractor.state],
          fitness: bestSolution.score,
          lyapunov: attractor.calculateLyapunovExponent(),
          fractal_dim: attractor.calculateFractalDimension()
        });
      }

      iteration++;
    }

    // Save final solution
    const solutionId = await this.db.saveSolution({
      bottleneck_id: bottleneckId,
      run_id: explorationId,
      configuration: bestSolution.solution,
      fitness: bestSolution.score,
      stability_score: converged ? 1.0 : 0.5,
      improvement_factor: bestSolution.score > 0 ? bestSolution.score / 100 : 1.0,
      estimated_economic_impact: bestSolution.score * 1000000, // Rough estimate
      validation_status: 'pending'
    });

    return {
      attractor: attractorName,
      bestSolution,
      converged,
      iterations: iteration,
      checkpoints,
      solutionId,
      attractorProperties: attractor.getProperties()
    };
  }

  /**
   * Initialize attractor parameters based on domain
   */
  initializeAttractorForDomain(attractor, bottleneck) {
    const domain = bottleneck.domain || 'generic';

    // Use domain-specific parameter sets
    switch (attractor.constructor.name) {
      case 'LorenzAttractor':
        if (domain === 'climate') {
          attractor.setParameters(10, 28, 8/3); // Standard chaotic
        } else if (domain === 'finance') {
          attractor.setParameters(16, 45.92, 4); // High chaos
        }
        break;

      case 'ChenAttractor':
        if (domain === 'supply_chain') {
          attractor.setParameters(36, -3, -16); // High chaos
        } else if (domain === 'healthcare') {
          attractor.setParameters(40, -3, -28); // Moderate chaos
        }
        break;

      case 'RosslerAttractor':
        if (domain === 'communication') {
          attractor.setParameters(0.1, 0.1, 14); // High chaos
        } else if (domain === 'optimization') {
          attractor.setParameters(0.2, 0.2, 5.7); // Standard
        }
        break;
    }
  }

  /**
   * Generate initial conditions based on bottleneck constraints
   */
  generateInitialConditions(bottleneck, dimensions) {
    const conditions = [];
    const numConditions = Math.min(10, Math.max(3, bottleneck.constraints?.length || 3));

    for (let i = 0; i < numConditions; i++) {
      const condition = [];

      for (let d = 0; d < dimensions; d++) {
        // Generate initial conditions within reasonable bounds
        // Use bottleneck constraints if available
        if (bottleneck.constraints && bottleneck.constraints[d]) {
          const constraint = bottleneck.constraints[d];
          const range = constraint.max - constraint.min;
          condition.push(constraint.min + Math.random() * range);
        } else {
          // Default random initialization
          condition.push((Math.random() - 0.5) * 2);
        }
      }

      conditions.push(condition);
    }

    return conditions;
  }

  /**
   * Map attractor state to bottleneck solution
   */
  mapAttractorToSolution(attractorState, bottleneck) {
    const solution = {};

    // Map attractor dimensions to bottleneck variables
    if (bottleneck.variables) {
      bottleneck.variables.forEach((variable, index) => {
        if (index < attractorState.length) {
          // Scale attractor state to variable bounds
          const value = this.scaleAttractorValue(
            attractorState[index],
            variable.min || 0,
            variable.max || 1
          );
          solution[variable.name] = value;
        }
      });
    }

    // Add domain-specific mappings
    if (bottleneck.domain === 'climate') {
      solution.temperature = attractorState[0] * 10 + 20; // Scale to reasonable temp
      solution.emissions = Math.abs(attractorState[1]) * 100; // Positive emissions
      solution.adaptation = (attractorState[2] + 10) / 20; // 0-1 scale
    } else if (bottleneck.domain === 'supply_chain') {
      solution.inventory = Math.abs(attractorState[0]) * 1000;
      solution.transport = Math.abs(attractorState[1]) * 500;
      solution.warehousing = Math.abs(attractorState[2]) * 200;
    }

    return solution;
  }

  /**
   * Scale attractor value to target range
   */
  scaleAttractorValue(value, min, max) {
    // Attractor values are typically in range [-bound, bound]
    // Scale to [min, max]
    const attractorRange = 100; // From applyBounds in BaseAttractor
    const normalized = (value + attractorRange) / (2 * attractorRange);
    return min + normalized * (max - min);
  }

  /**
   * Evaluate solution quality
   */
  async evaluateSolution(solution, bottleneck) {
    // Simple evaluation based on constraints satisfaction
    let score = 0;

    if (bottleneck.objective) {
      // Evaluate objective function
      score = this.evaluateObjective(solution, bottleneck.objective);
    }

    // Add constraint penalties
    if (bottleneck.constraints) {
      const constraintPenalty = this.evaluateConstraints(solution, bottleneck.constraints);
      score -= constraintPenalty * 100; // Heavy penalty for violations
    }

    // Add domain-specific evaluation
    if (bottleneck.domain) {
      score += this.evaluateDomainSpecific(solution, bottleneck);
    }

    return score;
  }

  /**
   * Evaluate objective function
   */
  evaluateObjective(solution, objective) {
    // Simple linear objective for now
    // In practice, this would be much more sophisticated
    let value = 0;

    if (objective.type === 'maximize') {
      Object.values(solution).forEach(val => {
        if (typeof val === 'number') value += val;
      });
    } else if (objective.type === 'minimize') {
      Object.values(solution).forEach(val => {
        if (typeof val === 'number') value -= val;
      });
    }

    return value;
  }

  /**
   * Evaluate constraint satisfaction
   */
  evaluateConstraints(solution, constraints) {
    let violations = 0;

    constraints.forEach(constraint => {
      const value = solution[constraint.variable];

      if (value !== undefined) {
        if (constraint.type === 'range') {
          if (value < constraint.min || value > constraint.max) {
            violations++;
          }
        } else if (constraint.type === 'equality') {
          if (Math.abs(value - constraint.value) > constraint.tolerance) {
            violations++;
          }
        }
      }
    });

    return violations;
  }

  /**
   * Domain-specific evaluation
   */
  evaluateDomainSpecific(solution, bottleneck) {
    let bonus = 0;

    switch (bottleneck.domain) {
      case 'climate':
        // Reward balanced solutions
        const temp = solution.temperature || 0;
        const emissions = solution.emissions || 0;
        const adaptation = solution.adaptation || 0;

        if (temp > 15 && temp < 25) bonus += 10; // Comfortable temperature
        if (emissions < 50) bonus += 20; // Low emissions
        if (adaptation > 0.7) bonus += 15; // Good adaptation
        break;

      case 'supply_chain':
        // Reward efficient resource allocation
        const inventory = solution.inventory || 0;
        const transport = solution.transport || 0;
        const warehousing = solution.warehousing || 0;

        if (inventory > 100 && inventory < 800) bonus += 10;
        if (transport < 300) bonus += 15;
        if (warehousing < 150) bonus += 10;
        break;

      case 'healthcare':
        // Reward balanced healthcare allocation
        // This would be more sophisticated in practice
        bonus += 5;
        break;
    }

    return bonus;
  }

  /**
   * Check for convergence
   */
  checkConvergence(bestSolution, threshold) {
    // Simple convergence check
    return bestSolution.score > threshold;
  }

  /**
   * Combine results from multiple attractor explorations
   */
  combineExplorationResults(results, bottleneck) {
    // Find best overall solution
    let bestSolution = null;
    let bestScore = -Infinity;

    results.forEach(result => {
      if (result.bestSolution.score > bestScore) {
        bestSolution = result.bestSolution;
        bestScore = result.bestSolution.score;
      }
    });

    // Calculate ensemble statistics
    const scores = results.map(r => r.bestSolution.score);
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
    const maxScore = Math.max(...scores);
    const minScore = Math.min(...scores);

    // Check if any exploration converged
    const converged = results.some(r => r.converged);

    return {
      bestSolution,
      ensemble: {
        averageScore: avgScore,
        maxScore,
        minScore,
        converged,
        attractorResults: results.map(r => ({
          attractor: r.attractor,
          score: r.bestSolution.score,
          converged: r.converged,
          iterations: r.iterations
        }))
      },
      bottleneck,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Get exploration history
   */
  async getExplorationHistory(bottleneckId) {
    return await this.db.getExplorationRuns(bottleneckId);
  }

  /**
   * Get solution details
   */
  async getSolution(solutionId) {
    return await this.db.getSolution(solutionId);
  }

  /**
   * Export results for deployment
   */
  async exportForDeployment(explorationResult, deploymentOptions = {}) {
    const {
      format = 'json',
      includeMetadata = true,
      includeCheckpoints = false
    } = deploymentOptions;

    const deploymentPlan = {
      solution: explorationResult.bestSolution,
      ensemble: explorationResult.ensemble,
      bottleneck: explorationResult.bottleneck,
      timestamp: explorationResult.timestamp,
      deployment: {
        recommendedActions: this.generateDeploymentActions(explorationResult),
        riskAssessment: this.assessDeploymentRisks(explorationResult),
        scalingStrategy: this.generateScalingStrategy(explorationResult)
      }
    };

    if (includeMetadata) {
      deploymentPlan.metadata = {
        explorationId: explorationResult.explorationId,
        attractorsUsed: explorationResult.ensemble.attractorResults.map(r => r.attractor),
        totalIterations: explorationResult.ensemble.attractorResults.reduce((sum, r) => sum + r.iterations, 0)
      };
    }

    // Save deployment plan to database
    const deploymentId = await this.db.saveDeploymentPlan({
      explorationId: explorationResult.explorationId,
      plan: JSON.stringify(deploymentPlan),
      status: 'planned'
    });

    deploymentPlan.deploymentId = deploymentId;

    return deploymentPlan;
  }

  /**
   * Generate deployment actions
   */
  generateDeploymentActions(result) {
    const actions = [];
    const solution = result.bestSolution.solution;
    const domain = result.bottleneck.domain;

    // Domain-specific deployment actions
    switch (domain) {
      case 'climate':
        actions.push({
          type: 'policy',
          description: `Implement temperature target of ${solution.temperature?.toFixed(1)}°C`,
          priority: 'high'
        });
        actions.push({
          type: 'investment',
          description: `Reduce emissions by ${((solution.emissions || 0) * 0.1).toFixed(0)}% through technology investment`,
          priority: 'high'
        });
        break;

      case 'supply_chain':
        actions.push({
          type: 'optimization',
          description: `Optimize inventory levels to ${solution.inventory?.toFixed(0)} units`,
          priority: 'medium'
        });
        actions.push({
          type: 'logistics',
          description: `Redesign transport network for ${(solution.transport || 0).toFixed(0)} efficiency`,
          priority: 'medium'
        });
        break;

      default:
        actions.push({
          type: 'implementation',
          description: 'Deploy optimized solution parameters',
          priority: 'medium'
        });
    }

    return actions;
  }

  /**
   * Assess deployment risks
   */
  assessDeploymentRisks(result) {
    const risks = [];
    const ensemble = result.ensemble;

    // Risk based on solution stability
    if (ensemble.maxScore - ensemble.minScore > ensemble.averageScore * 0.5) {
      risks.push({
        level: 'high',
        description: 'High variance in solution quality across attractors',
        mitigation: 'Validate solution through additional testing'
      });
    }

    // Risk based on convergence
    if (!ensemble.converged) {
      risks.push({
        level: 'medium',
        description: 'Solution did not fully converge',
        mitigation: 'Monitor performance and be prepared to adjust'
      });
    }

    return risks;
  }

  /**
   * Generate scaling strategy
   */
  generateScalingStrategy(result) {
    return {
      phases: [
        {
          name: 'Pilot',
          scale: '10%',
          duration: '1 month',
          metrics: ['performance', 'stability']
        },
        {
          name: 'Scale',
          scale: '50%',
          duration: '3 months',
          metrics: ['efficiency', 'cost_savings']
        },
        {
          name: 'Full Deployment',
          scale: '100%',
          duration: '6 months',
          metrics: ['roi', 'impact']
        }
      ],
      successCriteria: [
        'Performance improvement > 10%',
        'Cost reduction > 5%',
        'No critical failures'
      ]
    };
  }

  /**
   * Close database connection
   */
  async close() {
    await this.db.close();
  }
}

module.exports = BottleneckResolver;