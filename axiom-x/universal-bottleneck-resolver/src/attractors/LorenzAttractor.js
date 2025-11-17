/**
 * Lorenz Attractor Implementation
 * Classic 3D chaotic system discovered by Edward Lorenz
 * Used for weather modeling and chaos theory demonstrations
 */

const BaseAttractor = require('./BaseAttractor');

class LorenzAttractor extends BaseAttractor {
  constructor(sigma = 10, rho = 28, beta = 8/3) {
    super(3); // Lorenz is 3D
    this.sigma = sigma;
    this.rho = rho;
    this.beta = beta;
  }

  /**
   * Calculate derivatives for Lorenz system
   * dx/dt = sigma * (y - x)
   * dy/dt = x * (rho - z) - y
   * dz/dt = x * y - beta * z
   */
  calculateDerivatives(state) {
    const [x, y, z] = state;

    return [
      this.sigma * (y - x),                    // dx/dt
      x * (this.rho - z) - y,                  // dy/dt
      x * y - this.beta * z                    // dz/dt
    ];
  }

  /**
   * Get Lorenz-specific parameters
   */
  getParameters() {
    return {
      sigma: this.sigma,
      rho: this.rho,
      beta: this.beta
    };
  }

  /**
   * Set parameters with validation
   */
  setParameters(sigma, rho, beta) {
    if (sigma <= 0 || rho <= 0 || beta <= 0) {
      throw new Error('All Lorenz parameters must be positive');
    }

    this.sigma = sigma;
    this.rho = rho;
    this.beta = beta;
  }

  /**
   * Get optimal parameters for chaos exploration
   * Classic values: sigma=10, rho=28, beta=8/3
   */
  static getClassicParameters() {
    return {
      sigma: 10,
      rho: 28,
      beta: 8/3
    };
  }

  /**
   * Get parameters for different chaotic regimes
   */
  static getParameterSets() {
    return {
      classic: { sigma: 10, rho: 28, beta: 8/3 },
      highChaos: { sigma: 16, rho: 45.92, beta: 4 },
      lowChaos: { sigma: 10, rho: 24.74, beta: 8/3 },
      periodic: { sigma: 10, rho: 13.926, beta: 8/3 }
    };
  }

  /**
   * Calculate the critical rho value where chaos begins
   * Approximately 24.74 for classic parameters
   */
  getCriticalRho() {
    return this.sigma * (this.sigma + this.beta + 3) / (this.sigma - this.beta - 1);
  }

  /**
   * Check if current parameters are in chaotic regime
   */
  isChaotic() {
    return this.rho > this.getCriticalRho();
  }

  /**
   * Get attractor properties with Lorenz-specific metrics
   */
  getProperties() {
    const baseProps = super.getProperties();
    return {
      ...baseProps,
      isChaotic: this.isChaotic(),
      criticalRho: this.getCriticalRho(),
      parameterRegime: this.getParameterRegime()
    };
  }

  /**
   * Determine the dynamical regime based on parameters
   */
  getParameterRegime() {
    const criticalRho = this.getCriticalRho();

    if (this.rho < 1) return 'stable_fixed_point';
    if (this.rho < criticalRho) return 'periodic';
    if (this.rho > criticalRho) return 'chaotic';
    return 'bifurcation_point';
  }

  /**
   * Generate multiple trajectories with different initial conditions
   * Useful for exploring the attractor basin
   */
  generateEnsemble(initialConditions, steps = 1000) {
    const trajectories = [];

    initialConditions.forEach(ic => {
      this.setState(ic);
      this.clearTrajectory();

      for (let i = 0; i < steps; i++) {
        this.evolve();
      }

      trajectories.push({
        initialCondition: ic,
        trajectory: this.getTrajectory(),
        lyapunovExponent: this.calculateLyapunovExponent(),
        fractalDimension: this.calculateFractalDimension()
      });
    });

    return trajectories;
  }

  /**
   * Calculate correlation dimension (more sophisticated than box-counting)
   */
  calculateCorrelationDimension(trajectory = null, maxRadius = 1.0, minRadius = 0.001) {
    const traj = trajectory || this.trajectory;
    if (traj.length < 100) return 0;

    try {
      const radii = [];
      const logR = [];
      const logC = [];

      // Generate logarithmically spaced radii
      for (let i = 0; i < 20; i++) {
        const r = minRadius * Math.pow(maxRadius / minRadius, i / 19);
        radii.push(r);
      }

      radii.forEach(r => {
        let correlationSum = 0;
        let pairCount = 0;

        // Calculate correlation sum for this radius
        for (let i = 0; i < traj.length; i++) {
          for (let j = i + 1; j < traj.length; j++) {
            const distance = Math.sqrt(
              traj[i].reduce((sum, val, k) => sum + Math.pow(val - traj[j][k], 2), 0)
            );

            if (distance < r) {
              correlationSum += 1;
            }
            pairCount++;
          }
        }

        const correlation = correlationSum / pairCount;

        if (correlation > 0) {
          logR.push(Math.log(r));
          logC.push(Math.log(correlation));
        }
      });

      // Calculate slope of log(C) vs log(r) for intermediate scaling region
      if (logR.length > 5) {
        const midStart = Math.floor(logR.length * 0.3);
        const midEnd = Math.floor(logR.length * 0.7);

        let slopeSum = 0;
        let count = 0;

        for (let i = midStart; i < midEnd - 1; i++) {
          const slope = (logC[i + 1] - logC[i]) / (logR[i + 1] - logR[i]);
          if (isFinite(slope)) {
            slopeSum += slope;
            count++;
          }
        }

        return count > 0 ? slopeSum / count : 0;
      }

      return 0;
    } catch (error) {
      console.warn('Correlation dimension calculation failed:', error.message);
      return 0;
    }
  }
}

module.exports = LorenzAttractor;