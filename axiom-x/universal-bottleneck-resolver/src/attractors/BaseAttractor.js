/**
 * Base Attractor Class
 * Abstract base class for all strange attractors used in chaos exploration
 */

const math = require('mathjs');

class BaseAttractor {
  constructor(dimensions) {
    this.dimensions = Math.max(dimensions, 3); // Minimum 3D for basic attractors
    this.state = this.initializeState();
    this.dt = 0.01; // Time step for integration
    this.trajectory = [];
    this.maxTrajectoryLength = 10000; // Prevent memory issues
  }

  /**
   * Initialize random state vector
   */
  initializeState() {
    // Initialize with small random values to avoid numerical instability
    return Array.from({ length: this.dimensions }, () =>
      (Math.random() - 0.5) * 0.1
    );
  }

  /**
   * Set initial state
   */
  setState(state) {
    if (state.length !== this.dimensions) {
      throw new Error(`State vector must have ${this.dimensions} dimensions`);
    }
    this.state = [...state];
    this.trajectory = [this.state];
  }

  /**
   * Evolve state by one time step
   */
  evolve(state = null, dt = null) {
    const currentState = state || this.state;
    const timeStep = dt || this.dt;

    // Calculate derivatives (to be implemented by subclasses)
    const derivatives = this.calculateDerivatives(currentState);

    // Euler integration
    const newState = currentState.map((x, i) =>
      x + derivatives[i] * timeStep
    );

    // Apply bounds to prevent numerical explosion
    const boundedState = this.applyBounds(newState);

    // Update trajectory
    this.trajectory.push(boundedState);
    if (this.trajectory.length > this.maxTrajectoryLength) {
      this.trajectory.shift(); // Remove oldest point
    }

    this.state = boundedState;
    return boundedState;
  }

  /**
   * Calculate derivatives (to be implemented by subclasses)
   */
  calculateDerivatives(state) {
    throw new Error('calculateDerivatives must be implemented by subclass');
  }

  /**
   * Apply bounds to prevent numerical instability
   */
  applyBounds(state) {
    const bound = 100; // Reasonable bound for most attractors
    return state.map(x => Math.max(-bound, Math.min(bound, x)));
  }

  /**
   * Calculate Lyapunov exponent (measure of chaos/sensitivity)
   * Positive values indicate chaotic behavior
   */
  calculateLyapunovExponent(trajectory = null) {
    const traj = trajectory || this.trajectory;
    if (traj.length < 100) return 0; // Need sufficient data

    try {
      // Simplified Lyapunov calculation using divergence rate
      let totalDivergence = 0;
      let count = 0;

      for (let i = 1; i < Math.min(traj.length, 1000); i++) {
        const divergence = math.norm(
          math.subtract(traj[i], traj[i-1])
        );
        if (divergence > 1e-10) { // Avoid log(0)
          totalDivergence += Math.log(divergence);
          count++;
        }
      }

      return count > 0 ? totalDivergence / count : 0;
    } catch (error) {
      console.warn('Lyapunov calculation failed:', error.message);
      return 0;
    }
  }

  /**
   * Calculate fractal dimension using box-counting method
   */
  calculateFractalDimension(trajectory = null) {
    const traj = trajectory || this.trajectory;
    if (traj.length < 100) return 0;

    try {
      // Simplified box-counting dimension
      const boxes = new Set();
      const boxSize = 0.1; // Fixed box size for simplicity

      traj.forEach(point => {
        const boxCoords = point.map(coord =>
          Math.floor(coord / boxSize)
        );
        boxes.add(boxCoords.join(','));
      });

      const boxCount = boxes.size;
      const totalPoints = traj.length;

      // Estimate dimension using log-log relationship
      if (boxCount > 0 && totalPoints > 0) {
        return Math.log(boxCount) / Math.log(1 / boxSize);
      }

      return 0;
    } catch (error) {
      console.warn('Fractal dimension calculation failed:', error.message);
      return 0;
    }
  }

  /**
   * Get current trajectory
   */
  getTrajectory() {
    return [...this.trajectory];
  }

  /**
   * Clear trajectory
   */
  clearTrajectory() {
    this.trajectory = [this.state];
  }

  /**
   * Get attractor properties
   */
  getProperties() {
    return {
      name: this.constructor.name,
      dimensions: this.dimensions,
      parameters: this.getParameters(),
      lyapunovExponent: this.calculateLyapunovExponent(),
      fractalDimension: this.calculateFractalDimension(),
      trajectoryLength: this.trajectory.length
    };
  }

  /**
   * Get attractor-specific parameters (to be implemented by subclasses)
   */
  getParameters() {
    return {};
  }

  /**
   * Validate state vector
   */
  validateState(state) {
    if (!Array.isArray(state)) return false;
    if (state.length !== this.dimensions) return false;
    if (state.some(x => !isFinite(x))) return false;
    return true;
  }
}

module.exports = BaseAttractor;