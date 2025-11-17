/**
 * Rossler Attractor Implementation
 * 3D chaotic system discovered by Otto Rossler
 * Known for its simple equations yet complex spiral structure
 */

const BaseAttractor = require('./BaseAttractor');

class RosslerAttractor extends BaseAttractor {
  constructor(a = 0.2, b = 0.2, c = 5.7) {
    super(3); // Rossler is 3D
    this.a = a;
    this.b = b;
    this.c = c;
  }

  /**
   * Calculate derivatives for Rossler system
   * dx/dt = -y - z
   * dy/dt = x + a * y
   * dz/dt = b + z * (x - c)
   */
  calculateDerivatives(state) {
    const [x, y, z] = state;

    return [
      -y - z,                    // dx/dt
      x + this.a * y,           // dy/dt
      this.b + z * (x - this.c) // dz/dt
    ];
  }

  /**
   * Get Rossler-specific parameters
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
    // Rossler system parameters should be in reasonable ranges
    if (a < 0 || a > 1) {
      throw new Error('Parameter a should be between 0 and 1');
    }
    if (b < 0 || b > 1) {
      throw new Error('Parameter b should be between 0 and 1');
    }
    if (c < 0 || c > 10) {
      throw new Error('Parameter c should be between 0 and 10');
    }

    this.a = a;
    this.b = b;
    this.c = c;
  }

  /**
   * Get standard Rossler parameters for chaotic behavior
   */
  static getStandardParameters() {
    return {
      a: 0.2,
      b: 0.2,
      c: 5.7
    };
  }

  /**
   * Get parameter sets for different dynamical behaviors
   */
  static getParameterSets() {
    return {
      standard: { a: 0.2, b: 0.2, c: 5.7 },
      highChaos: { a: 0.1, b: 0.1, c: 14 },
      periodic: { a: 0.2, b: 0.2, c: 2.5 },
      quasiperiodic: { a: 0.15, b: 0.2, c: 8.5 }
    };
  }

  /**
   * Check if parameters are in the chaotic regime
   * Rossler system shows chaos for c > ~4
   */
  isChaotic() {
    return this.c > 4;
  }

  /**
   * Calculate the period of the Rossler attractor
   * Approximate formula for the main period
   */
  getApproximatePeriod() {
    if (!this.isChaotic()) {
      // For periodic behavior, estimate period
      return 2 * Math.PI / Math.sqrt(this.c - this.b);
    } else {
      // For chaotic behavior, return average lobe return time
      return 2 * Math.PI * Math.sqrt(this.c) / this.a;
    }
  }

  /**
   * Calculate the folding point (where trajectory folds back)
   */
  getFoldingPoint() {
    // The folding occurs approximately at x = c
    return this.c;
  }

  /**
   * Generate Poincare section at z = 0
   */
  generatePoincareSection(steps = 10000) {
    const poincarePoints = [];
    this.setState([0.1, 0.1, 0.1]);
    this.clearTrajectory();

    let lastZ = this.state[2];

    for (let i = 0; i < steps; i++) {
      this.evolve();

      // Check for crossing z = 0 plane
      if ((lastZ <= 0 && this.state[2] > 0) || (lastZ >= 0 && this.state[2] < 0)) {
        // Linear interpolation to find exact crossing point
        const t = -lastZ / (this.state[2] - lastZ);
        const crossingX = this.trajectory[this.trajectory.length - 2][0] +
                          t * (this.state[0] - this.trajectory[this.trajectory.length - 2][0]);
        const crossingY = this.trajectory[this.trajectory.length - 2][1] +
                          t * (this.state[1] - this.trajectory[this.trajectory.length - 2][1]);

        poincarePoints.push([crossingX, crossingY]);
      }

      lastZ = this.state[2];
    }

    return poincarePoints;
  }

  /**
   * Calculate the rotation number (winding number around the main loop)
   */
  calculateRotationNumber(poincarePoints = null) {
    const points = poincarePoints || this.generatePoincareSection();

    if (points.length < 10) return 0;

    try {
      // Calculate angle changes around the center
      const centerX = points.reduce((sum, p) => sum + p[0], 0) / points.length;
      const centerY = points.reduce((sum, p) => sum + p[1], 0) / points.length;

      let totalAngleChange = 0;
      let lastAngle = Math.atan2(points[0][1] - centerY, points[0][0] - centerX);

      for (let i = 1; i < points.length; i++) {
        const angle = Math.atan2(points[i][1] - centerY, points[i][0] - centerX);
        let angleDiff = angle - lastAngle;

        // Handle angle wrapping
        while (angleDiff > Math.PI) angleDiff -= 2 * Math.PI;
        while (angleDiff < -Math.PI) angleDiff += 2 * Math.PI;

        totalAngleChange += angleDiff;
        lastAngle = angle;
      }

      return totalAngleChange / (2 * Math.PI);
    } catch (error) {
      console.warn('Rotation number calculation failed:', error.message);
      return 0;
    }
  }

  /**
   * Get attractor properties with Rossler-specific metrics
   */
  getProperties() {
    const baseProps = super.getProperties();
    const poincarePoints = this.generatePoincareSection();

    return {
      ...baseProps,
      isChaotic: this.isChaotic(),
      approximatePeriod: this.getApproximatePeriod(),
      foldingPoint: this.getFoldingPoint(),
      rotationNumber: this.calculateRotationNumber(poincarePoints),
      poincareSectionPoints: poincarePoints.length
    };
  }

  /**
   * Calculate the entropy of the Rossler system
   * Based on the Kolmogorov-Sinai entropy
   */
  calculateEntropy(trajectory = null) {
    const traj = trajectory || this.trajectory;
    if (traj.length < 1000) return 0;

    try {
      // Simplified entropy calculation using trajectory symbolization
      const symbols = [];
      const partitions = 8; // Number of partitions per dimension

      traj.forEach(state => {
        // Convert 3D state to symbol
        const symbol = state.map(coord => {
          const normalized = (coord + 50) / 100; // Normalize to [0,1]
          return Math.min(partitions - 1, Math.floor(normalized * partitions));
        });

        // Combine dimensions into single symbol
        const combinedSymbol = symbol[0] * partitions * partitions +
                              symbol[1] * partitions +
                              symbol[2];
        symbols.push(combinedSymbol);
      });

      // Calculate Shannon entropy
      const symbolCounts = {};
      symbols.forEach(symbol => {
        symbolCounts[symbol] = (symbolCounts[symbol] || 0) + 1;
      });

      let entropy = 0;
      const totalSymbols = symbols.length;

      Object.values(symbolCounts).forEach(count => {
        const probability = count / totalSymbols;
        entropy -= probability * Math.log2(probability);
      });

      return entropy;
    } catch (error) {
      console.warn('Entropy calculation failed:', error.message);
      return 0;
    }
  }

  /**
   * Generate bifurcation diagram by varying parameter c
   */
  generateBifurcationDiagram(cRange = { min: 2, max: 7, steps: 100 }) {
    const bifurcationData = [];
    const originalC = this.c;

    for (let i = 0; i < cRange.steps; i++) {
      const c = cRange.min + (cRange.max - cRange.min) * (i / (cRange.steps - 1));
      this.c = c;

      // Generate trajectory with this parameter
      this.setState([0.1, 0.1, 0.1]);
      this.clearTrajectory();

      // Let system settle
      for (let j = 0; j < 2000; j++) {
        this.evolve();
      }

      // Sample points for bifurcation
      const samples = [];
      for (let j = 0; j < 200; j++) {
        this.evolve();
        samples.push(this.state[0]); // Sample x coordinate
      }

      bifurcationData.push({
        parameter: c,
        samples: samples,
        lyapunovExponent: this.calculateLyapunovExponent(),
        entropy: this.calculateEntropy()
      });
    }

    // Restore original parameter
    this.c = originalC;

    return bifurcationData;
  }

  /**
   * Calculate the fractal dimension using sandbox method
   * More accurate for Rossler than simple box-counting
   */
  calculateSandboxDimension(trajectory = null, maxRadius = 10, minRadius = 0.01) {
    const traj = trajectory || this.trajectory;
    if (traj.length < 100) return 0;

    try {
      const radii = [];
      const mass = [];

      // Generate logarithmically spaced radii
      for (let i = 0; i < 15; i++) {
        const r = minRadius * Math.pow(maxRadius / minRadius, i / 14);
        radii.push(r);
      }

      radii.forEach(r => {
        let totalMass = 0;

        traj.forEach(point => {
          // Count points within radius r of this point
          let localMass = 0;
          traj.forEach(otherPoint => {
            const distance = Math.sqrt(
              point.reduce((sum, val, k) => sum + Math.pow(val - otherPoint[k], 2), 0)
            );
            if (distance <= r) {
              localMass += 1;
            }
          });
          totalMass += localMass;
        });

        mass.push(totalMass / traj.length);
      });

      // Calculate dimension from log-log plot
      if (radii.length > 5 && mass.length > 5) {
        const logR = radii.map(r => Math.log(1/r));
        const logM = mass.map(m => Math.log(m));

        // Use linear regression on intermediate scaling region
        const startIdx = Math.floor(logR.length * 0.2);
        const endIdx = Math.floor(logR.length * 0.8);

        let sumX = 0, sumY = 0, sumXY = 0, sumXX = 0;
        let n = 0;

        for (let i = startIdx; i < endIdx; i++) {
          if (isFinite(logR[i]) && isFinite(logM[i])) {
            sumX += logR[i];
            sumY += logM[i];
            sumXY += logR[i] * logM[i];
            sumXX += logR[i] * logR[i];
            n++;
          }
        }

        if (n > 1) {
          const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
          return slope;
        }
      }

      return 0;
    } catch (error) {
      console.warn('Sandbox dimension calculation failed:', error.message);
      return 0;
    }
  }
}

module.exports = RosslerAttractor;