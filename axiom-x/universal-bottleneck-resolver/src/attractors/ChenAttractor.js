/**
 * Chen Attractor Implementation
 * 3D chaotic system discovered by Guanrong Chen and Tetsushi Ueta
 * Known for its complex structure and higher-dimensional behavior
 */

const BaseAttractor = require('./BaseAttractor');

class ChenAttractor extends BaseAttractor {
  constructor(a = 5, b = -10, c = -0.38) {
    super(3); // Chen is 3D
    this.a = a;
    this.b = b;
    this.c = c;
  }

  /**
   * Calculate derivatives for Chen system
   * dx/dt = a * (y - x)
   * dy/dt = (c - a) * x - x * z + c * y
   * dz/dt = x * y - b * z
   */
  calculateDerivatives(state) {
    const [x, y, z] = state;

    return [
      this.a * (y - x),                        // dx/dt
      (this.c - this.a) * x - x * z + this.c * y, // dy/dt
      x * y - this.b * z                       // dz/dt
    ];
  }

  /**
   * Get Chen-specific parameters
   */
  getParameters() {
    return {
      a: this.a,
      b: this.b,
      c: this.c
    };
  }

  /**
   * Set parameters with validation
   */
  setParameters(a, b, c) {
    // Chen system requires specific parameter ranges for chaos
    if (a <= 0) {
      throw new Error('Parameter a must be positive');
    }
    if (b >= 0) {
      throw new Error('Parameter b must be negative');
    }
    if (c >= 0) {
      throw new Error('Parameter c must be negative');
    }

    this.a = a;
    this.b = b;
    this.c = c;
  }

  /**
   * Get standard Chen parameters for chaotic behavior
   */
  static getStandardParameters() {
    return {
      a: 5,
      b: -10,
      c: -0.38
    };
  }

  /**
   * Get parameter sets for different dynamical behaviors
   */
  static getParameterSets() {
    return {
      standard: { a: 5, b: -10, c: -0.38 },
      highChaos: { a: 36, b: -3, c: -16 },
      moderateChaos: { a: 40, b: -3, c: -28 },
      lowChaos: { a: 5, b: -10, c: -0.1 }
    };
  }

  /**
   * Check if parameters are in the chaotic regime
   * Chen system is chaotic for a > 0, b < 0, c < 0
   */
  isChaotic() {
    return this.a > 0 && this.b < 0 && this.c < 0;
  }

  /**
   * Calculate the equilibrium points of the Chen system
   */
  getEquilibriumPoints() {
    const equilibria = [];

    // Equilibrium point 1: (0, 0, 0)
    equilibria.push([0, 0, 0]);

    // Equilibrium point 2: Solve for non-trivial points
    // This requires solving a cubic equation, simplified approximation
    if (this.isChaotic()) {
      // Approximate non-trivial equilibrium
      const x_eq = Math.sqrt(-this.b * this.c / this.a);
      const y_eq = x_eq;
      const z_eq = x_eq * y_eq / this.b;

      if (isFinite(x_eq) && isFinite(y_eq) && isFinite(z_eq)) {
        equilibria.push([x_eq, y_eq, z_eq]);
        equilibria.push([-x_eq, -y_eq, z_eq]);
      }
    }

    return equilibria;
  }

  /**
   * Calculate the Lyapunov spectrum for Chen system
   * Returns array of three Lyapunov exponents
   */
  calculateLyapunovSpectrum(trajectory = null) {
    const traj = trajectory || this.trajectory;
    if (traj.length < 1000) return [0, 0, 0];

    try {
      // Simplified Lyapunov spectrum calculation
      // In practice, this requires solving the variational equations
      const exponents = [];

      // First exponent (largest) - similar to base calculation
      exponents.push(this.calculateLyapunovExponent(traj));

      // Second exponent - approximate using trajectory divergence
      let divergence2 = 0;
      let count2 = 0;

      for (let i = 10; i < Math.min(traj.length, 1000); i += 10) {
        const localDivergence = Math.sqrt(
          traj[i].slice(0, 2).reduce((sum, val, k) =>
            sum + Math.pow(val - traj[i-1][k], 2), 0
          )
        );
        if (localDivergence > 1e-8) {
          divergence2 += Math.log(localDivergence);
          count2++;
        }
      }

      exponents.push(count2 > 0 ? divergence2 / count2 : 0);

      // Third exponent - constrained by volume preservation
      // For continuous systems, sum of exponents should be negative
      const sumFirstTwo = exponents[0] + exponents[1];
      exponents.push(-sumFirstTwo);

      return exponents;
    } catch (error) {
      console.warn('Lyapunov spectrum calculation failed:', error.message);
      return [0, 0, 0];
    }
  }

  /**
   * Get attractor properties with Chen-specific metrics
   */
  getProperties() {
    const baseProps = super.getProperties();
    const lyapunovSpectrum = this.calculateLyapunovSpectrum();

    return {
      ...baseProps,
      isChaotic: this.isChaotic(),
      equilibriumPoints: this.getEquilibriumPoints(),
      lyapunovSpectrum: lyapunovSpectrum,
      kaplanYorkeDimension: this.calculateKaplanYorkeDimension(lyapunovSpectrum)
    };
  }

  /**
   * Calculate Kaplan-Yorke dimension from Lyapunov spectrum
   * D_KY = j + (sum_{i=1}^j λ_i) / |λ_{j+1}|
   */
  calculateKaplanYorkeDimension(lyapunovSpectrum) {
    if (!lyapunovSpectrum || lyapunovSpectrum.length < 3) return 0;

    try {
      const sortedExponents = [...lyapunovSpectrum].sort((a, b) => b - a);
      let cumulativeSum = 0;
      let dimension = 0;

      for (let j = 0; j < sortedExponents.length - 1; j++) {
        cumulativeSum += sortedExponents[j];
        if (cumulativeSum > 0 && sortedExponents[j + 1] < 0) {
          dimension = j + cumulativeSum / Math.abs(sortedExponents[j + 1]);
          break;
        }
      }

      return dimension;
    } catch (error) {
      console.warn('Kaplan-Yorke dimension calculation failed:', error.message);
      return 0;
    }
  }

  /**
   * Generate bifurcation diagram by varying parameter c
   */
  generateBifurcationDiagram(cRange = { min: -2, max: 0, steps: 100 }) {
    const bifurcationData = [];
    const originalC = this.c;

    for (let i = 0; i < cRange.steps; i++) {
      const c = cRange.min + (cRange.max - cRange.min) * (i / (cRange.steps - 1));
      this.c = c;

      // Generate trajectory with this parameter
      this.setState([0.1, 0.1, 0.1]);
      this.clearTrajectory();

      // Let system settle
      for (let j = 0; j < 1000; j++) {
        this.evolve();
      }

      // Sample points for bifurcation
      const samples = [];
      for (let j = 0; j < 100; j++) {
        this.evolve();
        samples.push(this.state[0]); // Sample x coordinate
      }

      bifurcationData.push({
        parameter: c,
        samples: samples,
        lyapunovExponent: this.calculateLyapunovExponent()
      });
    }

    // Restore original parameter
    this.c = originalC;

    return bifurcationData;
  }

  /**
   * Calculate the basin of attraction stability
   */
  calculateBasinStability(initialConditions, tolerance = 0.1) {
    const stabilityData = [];

    initialConditions.forEach(ic => {
      this.setState(ic);
      this.clearTrajectory();

      // Evolve for sufficient time
      for (let i = 0; i < 5000; i++) {
        this.evolve();
      }

      const trajectory = this.getTrajectory();
      const finalState = trajectory[trajectory.length - 1];

      // Check if trajectory stays bounded
      const isBounded = trajectory.slice(-100).every(state =>
        state.every(coord => Math.abs(coord) < 100)
      );

      // Calculate trajectory variance as stability measure
      const variances = [0, 1, 2].map(dim => {
        const values = trajectory.slice(-1000).map(state => state[dim]);
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        return values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
      });

      stabilityData.push({
        initialCondition: ic,
        finalState: finalState,
        isBounded: isBounded,
        trajectoryVariance: variances,
        maxVariance: Math.max(...variances)
      });
    });

    return stabilityData;
  }
}

module.exports = ChenAttractor;