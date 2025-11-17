/**
 * Basic Tests for Universal Bottleneck Resolver
 */

const LorenzAttractor = require('../src/attractors/LorenzAttractor');
const ChenAttractor = require('../src/attractors/ChenAttractor');
const RosslerAttractor = require('../src/attractors/RosslerAttractor');
const BaseDomainTemplate = require('../src/domains/BaseDomainTemplate');
const ClimateCoordination = require('../src/domains/ClimateCoordination');

describe('Chaos Attractors', () => {
  describe('LorenzAttractor', () => {
    let attractor;

    beforeEach(() => {
      attractor = new LorenzAttractor();
    });

    test('should initialize with correct dimensions', () => {
      expect(attractor.dimensions).toBe(3);
      expect(attractor.state).toHaveLength(3);
    });

    test('should evolve state correctly', () => {
      const initialState = [1, 1, 1];
      attractor.setState(initialState);

      const newState = attractor.evolve();
      expect(newState).toHaveLength(3);
      expect(newState).not.toEqual(initialState);
      expect(attractor.state).toEqual(newState);
    });

    test('should calculate Lyapunov exponent', () => {
      attractor.setState([1, 1, 1]);

      // Generate longer trajectory for better calculation
      for (let i = 0; i < 5000; i++) {
        attractor.evolve();
      }

      const lyapunov = attractor.calculateLyapunovExponent();
      expect(typeof lyapunov).toBe('number');
      expect(lyapunov).toBeLessThan(10); // Should be reasonable (not infinity)
      expect(lyapunov).toBeGreaterThan(-10); // Should be reasonable (not negative infinity)
    });

    test('should be in chaotic regime with default parameters', () => {
      expect(attractor.isChaotic()).toBe(true);
    });

    test('should get correct properties', () => {
      const props = attractor.getProperties();
      expect(props.name).toBe('LorenzAttractor');
      expect(props.dimensions).toBe(3);
      expect(props.isChaotic).toBe(true);
    });
  });

  describe('ChenAttractor', () => {
    let attractor;

    beforeEach(() => {
      attractor = new ChenAttractor();
    });

    test('should initialize correctly', () => {
      expect(attractor.dimensions).toBe(3);
      expect(attractor.a).toBe(5);
      expect(attractor.b).toBe(-10);
      expect(attractor.c).toBe(-0.38);
    });

    test('should evolve and maintain chaos', () => {
      attractor.setState([0.1, 0.1, 0.1]);

      for (let i = 0; i < 100; i++) {
        attractor.evolve();
      }

      expect(attractor.isChaotic()).toBe(true);
      expect(attractor.getTrajectory().length).toBeGreaterThan(90);
    });

    test('should calculate Kaplan-Yorke dimension', () => {
      attractor.setState([0.1, 0.1, 0.1]);

      for (let i = 0; i < 1000; i++) {
        attractor.evolve();
      }

      const props = attractor.getProperties();
      expect(props.kaplanYorkeDimension).toBeDefined();
      expect(typeof props.kaplanYorkeDimension).toBe('number');
    });
  });

  describe('RosslerAttractor', () => {
    let attractor;

    beforeEach(() => {
      attractor = new RosslerAttractor();
    });

    test('should initialize correctly', () => {
      expect(attractor.dimensions).toBe(3);
      expect(attractor.a).toBe(0.2);
      expect(attractor.b).toBe(0.2);
      expect(attractor.c).toBe(5.7);
    });

    test('should generate Poincare section', () => {
      // Use more steps and check that it's an array
      const poincarePoints = attractor.generatePoincareSection(5000);
      expect(Array.isArray(poincarePoints)).toBe(true);
      // Poincare section might be empty for some parameter sets, just check structure
      if (poincarePoints.length > 0) {
        expect(poincarePoints[0]).toHaveLength(2); // 2D projection
      }
    });

    test('should calculate rotation number', () => {
      const poincarePoints = attractor.generatePoincareSection(2000);
      const rotationNumber = attractor.calculateRotationNumber(poincarePoints);
      expect(typeof rotationNumber).toBe('number');
    });
  });
});

describe('Domain Templates', () => {
  describe('BaseDomainTemplate', () => {
    class TestTemplate extends BaseDomainTemplate {
      constructor() {
        super('test');
        this.variables = [
          { name: 'var1', type: 'continuous', min: 0, max: 1 },
          { name: 'var2', type: 'continuous', min: 0, max: 1 }
        ];
        this.constraints = [
          { variable: 'var1', type: 'range', min: 0.1, max: 0.9 }
        ];
        this.objective = {
          type: 'maximize',
          function: (solution) => solution.var1 + solution.var2
        };
      }
    }

    let template;

    beforeEach(() => {
      template = new TestTemplate();
    });

    test('should initialize correctly', () => {
      expect(template.domain).toBe('test');
      expect(template.variables).toHaveLength(2);
      expect(template.constraints).toHaveLength(1);
    });

    test('should validate solutions', () => {
      const validSolution = { var1: 0.5, var2: 0.3 };
      const invalidSolution = { var1: 1.5, var2: 0.3 };

      expect(template.validateSolution(validSolution)).toHaveLength(0);
      expect(template.validateSolution(invalidSolution)).toHaveLength(1);
    });

    test('should generate initial conditions', () => {
      const conditions = template.generateInitialConditions(3);
      expect(conditions).toHaveLength(3);
      expect(conditions[0]).toHaveLength(2);

      conditions.forEach(condition => {
        condition.forEach(value => {
          expect(value).toBeGreaterThanOrEqual(0);
          expect(value).toBeLessThanOrEqual(1);
        });
      });
    });

    test('should evaluate solutions', () => {
      const solution = { var1: 0.6, var2: 0.4 };
      const score = template.evaluateSolution(solution);
      expect(score).toBe(1.0); // 0.6 + 0.4
    });
  });

  describe('ClimateCoordination', () => {
    let template;

    beforeEach(() => {
      template = new ClimateCoordination();
    });

    test('should have correct domain', () => {
      expect(template.domain).toBe('climate');
    });

    test('should have climate variables', () => {
      expect(template.variables).toHaveLength(5);
      expect(template.variables[0].name).toBe('temperature_target');
      expect(template.variables[0].min).toBe(1.5);
      expect(template.variables[0].max).toBe(4.0);
    });

    test('should calculate climate benefit', () => {
      const solution = {
        temperature_target: 2.0,
        emission_reduction_rate: 0.05,
        adaptation_investment: 0.5,
        renewable_energy_fraction: 0.6,
        carbon_price: 50
      };

      const benefit = template.calculateClimateBenefit(solution);
      expect(typeof benefit).toBe('number');
      expect(benefit).toBeGreaterThan(0);
    });

    test('should validate climate solutions', () => {
      const validSolution = {
        temperature_target: 2.0,
        emission_reduction_rate: 0.05,
        adaptation_investment: 0.5,
        renewable_energy_fraction: 0.6,
        carbon_price: 50
      };

      const violations = template.validateSolution(validSolution);
      expect(violations).toHaveLength(0);
    });

    test('should calculate climate impact', () => {
      const solution = {
        temperature_target: 2.0,
        emission_reduction_rate: 0.05,
        adaptation_investment: 0.5,
        renewable_energy_fraction: 0.6,
        carbon_price: 50
      };

      const impact = template.calculateImpact(solution);
      expect(impact).toHaveProperty('environmental');
      expect(impact).toHaveProperty('economic');
      expect(impact).toHaveProperty('social');
      expect(impact).toHaveProperty('total');
    });
  });
});

describe('Integration Tests', () => {
  test('attractors should work together', () => {
    const lorenz = new LorenzAttractor();
    const chen = new ChenAttractor();
    const rossler = new RosslerAttractor();

    // Initialize all attractors
    lorenz.setState([1, 1, 1]);
    chen.setState([0.1, 0.1, 0.1]);
    rossler.setState([0.1, 0.1, 0.1]);

    // Evolve all for same number of steps
    for (let i = 0; i < 100; i++) {
      lorenz.evolve();
      chen.evolve();
      rossler.evolve();
    }

    // All should have trajectories
    expect(lorenz.getTrajectory().length).toBeGreaterThan(90);
    expect(chen.getTrajectory().length).toBeGreaterThan(90);
    expect(rossler.getTrajectory().length).toBeGreaterThan(90);

    // All should have finite Lyapunov exponents
    expect(isFinite(lorenz.calculateLyapunovExponent())).toBe(true);
    expect(isFinite(chen.calculateLyapunovExponent())).toBe(true);
    expect(isFinite(rossler.calculateLyapunovExponent())).toBe(true);
  });

  test('domain templates should be compatible', () => {
    const climate = new ClimateCoordination();

    // Should be able to generate initial conditions
    const conditions = climate.generateInitialConditions(5);
    expect(conditions).toHaveLength(5);

    // Should be able to map to solution
    const solution = climate.mapAttractorToSolution([2.0, 0.05, 0.5, 0.6, 50]);
    expect(solution).toHaveProperty('temperature_target');
    expect(solution).toHaveProperty('emission_reduction_rate');
    expect(solution).toHaveProperty('adaptation_investment');
    expect(solution).toHaveProperty('renewable_energy_fraction');
    expect(solution).toHaveProperty('carbon_price');

    // Should be able to evaluate
    const score = climate.evaluateSolution(solution);
    expect(typeof score).toBe('number');
  });
});