/**
 * Base Domain Template
 * Abstract base class for domain-specific bottleneck templates
 */

class BaseDomainTemplate {
  constructor(domainName) {
    this.domain = domainName;
    this.variables = [];
    this.constraints = [];
    this.objective = null;
  }

  /**
   * Get domain name
   */
  getDomainName() {
    return this.domain;
  }

  /**
   * Get variables for this domain
   */
  getVariables() {
    return this.variables;
  }

  /**
   * Get constraints for this domain
   */
  getConstraints() {
    return this.constraints;
  }

  /**
   * Get objective function
   */
  getObjective() {
    return this.objective;
  }

  /**
   * Validate a solution against domain constraints
   */
  validateSolution(solution) {
    const violations = [];

    this.constraints.forEach(constraint => {
      const value = solution[constraint.variable];

      if (value === undefined) {
        violations.push(`Missing required variable: ${constraint.variable}`);
        return;
      }

      switch (constraint.type) {
        case 'range':
          if (value < constraint.min || value > constraint.max) {
            violations.push(`${constraint.variable} must be between ${constraint.min} and ${constraint.max}`);
          }
          break;

        case 'equality':
          if (Math.abs(value - constraint.value) > (constraint.tolerance || 0)) {
            violations.push(`${constraint.variable} must equal ${constraint.value} ± ${constraint.tolerance || 0}`);
          }
          break;

        case 'minimum':
          if (value < constraint.min) {
            violations.push(`${constraint.variable} must be at least ${constraint.min}`);
          }
          break;

        case 'maximum':
          if (value > constraint.max) {
            violations.push(`${constraint.variable} must be at most ${constraint.max}`);
          }
          break;
      }
    });

    return violations;
  }

  /**
   * Generate initial conditions for exploration
   */
  generateInitialConditions(numConditions = 5) {
    const conditions = [];

    for (let i = 0; i < numConditions; i++) {
      const condition = [];

      this.variables.forEach(variable => {
        let value;

        if (variable.type === 'continuous') {
          value = variable.min + Math.random() * (variable.max - variable.min);
        } else if (variable.type === 'discrete') {
          const options = variable.options || [];
          value = options[Math.floor(Math.random() * options.length)];
        } else if (variable.type === 'binary') {
          value = Math.random() > 0.5 ? 1 : 0;
        }

        condition.push(value);
      });

      conditions.push(condition);
    }

    return conditions;
  }

  /**
   * Map attractor state to domain solution
   */
  mapAttractorToSolution(attractorState) {
    const solution = {};

    this.variables.forEach((variable, index) => {
      if (index < attractorState.length) {
        const attractorValue = attractorState[index];
        solution[variable.name] = this.scaleAttractorValue(attractorValue, variable);
      }
    });

    return solution;
  }

  /**
   * Scale attractor value to variable bounds
   */
  scaleAttractorValue(attractorValue, variable) {
    if (variable.type === 'continuous') {
      // Attractor values are typically in range [-bound, bound]
      // Scale to variable [min, max]
      const attractorRange = 100; // From BaseAttractor bounds
      const normalized = (attractorValue + attractorRange) / (2 * attractorRange);
      return variable.min + normalized * (variable.max - variable.min);
    } else if (variable.type === 'binary') {
      return attractorValue > 0 ? 1 : 0;
    } else if (variable.type === 'discrete') {
      const options = variable.options || [];
      const index = Math.floor((attractorValue + 50) / 100 * options.length);
      return options[Math.max(0, Math.min(options.length - 1, index))];
    }

    return attractorValue;
  }

  /**
   * Evaluate solution quality
   */
  evaluateSolution(solution) {
    if (!this.objective) return 0;

    const objectiveValue = this.objective.function(solution);

    // Apply constraint penalties
    const violations = this.validateSolution(solution);
    const penalty = violations.length * 100; // Heavy penalty per violation

    if (this.objective.type === 'maximize') {
      return objectiveValue - penalty;
    } else {
      return -objectiveValue - penalty; // Convert minimize to maximize
    }
  }

  /**
   * Get domain metadata
   */
  getMetadata() {
    return {
      name: this.domain,
      description: `Domain template for ${this.domain} optimization`,
      variables: this.variables.length,
      constraints: this.constraints.length,
      complexity: this.variables.length > 5 ? 'high' : 'medium'
    };
  }

  /**
   * Calculate domain-specific impact
   */
  calculateImpact(solution) {
    // Default implementation - should be overridden by subclasses
    return {
      primary: this.evaluateSolution(solution),
      secondary: 0,
      total: this.evaluateSolution(solution)
    };
  }

  /**
   * Generate deployment roadmap
   */
  generateDeploymentRoadmap(solution) {
    // Default implementation - should be overridden by subclasses
    return {
      phases: [
        {
          name: 'Planning',
          actions: ['Analyze solution', 'Plan implementation'],
          duration: '1 month'
        },
        {
          name: 'Implementation',
          actions: ['Deploy solution', 'Monitor progress'],
          duration: '3 months'
        },
        {
          name: 'Optimization',
          actions: ['Fine-tune parameters', 'Scale up'],
          duration: '6 months'
        }
      ]
    };
  }

  /**
   * Get attractor preferences for this domain
   */
  getAttractorPreferences() {
    return {
      lorenz: { weight: 0.33, reason: 'General purpose optimization' },
      chen: { weight: 0.33, reason: 'Complex system modeling' },
      rossler: { weight: 0.34, reason: 'Dynamic system analysis' }
    };
  }

  /**
   * Export domain template as bottleneck definition
   */
  toBottleneckDefinition() {
    return {
      domain: this.domain,
      variables: this.variables,
      constraints: this.constraints,
      objective: this.objective,
      metadata: this.getMetadata(),
      attractorPreferences: this.getAttractorPreferences()
    };
  }
}

module.exports = BaseDomainTemplate;