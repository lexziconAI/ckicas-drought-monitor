#!/usr/bin/env node

/**
 * Universal Bottleneck Resolver - Example Usage
 * Demonstrates chaos-theoretic bottleneck resolution
 */

const BottleneckResolver = require('../src/core/BottleneckResolver');
const ClimateCoordination = require('../src/domains/ClimateCoordination');
const LorenzAttractor = require('../src/attractors/LorenzAttractor');

async function demonstrateClimateResolution() {
  console.log('🌀 Universal Bottleneck Resolver - Climate Coordination Demo');
  console.log('═'.repeat(60));

  try {
    // Initialize resolver
    const resolver = new BottleneckResolver('./example.db');
    await resolver.initialize();

    // Create climate bottleneck
    const climateTemplate = new ClimateCoordination();
    const templateData = climateTemplate.toBottleneckDefinition();

    // Create proper bottleneck definition for database
    const climateBottleneck = {
      domain: templateData.domain,
      name: 'Global Climate Change Mitigation',
      description: 'Optimize global climate action to limit warming to 1.5°C while maximizing economic benefits',
      dimensions: templateData.variables.length,
      bottleneck_type: 'multi-objective_optimization',
      optimization_target: 'maximize_climate_benefit',
      variables: templateData.variables,
      constraints: templateData.constraints.map((constraint, index) => ({
        name: constraint.variable || `constraint_${index}`,
        type: constraint.type,
        definition: {
          variable: constraint.variable,
          min: constraint.min,
          max: constraint.max,
          description: constraint.description
        }
      })),
      objective: templateData.objective
    };

    console.log('🌡️ Resolving Climate Coordination Bottleneck...');
    console.log(`Domain: ${climateBottleneck.domain}`);
    console.log(`Variables: ${climateBottleneck.variables.length}`);
    console.log(`Constraints: ${climateBottleneck.constraints.length}`);
    console.log();

    // Resolve bottleneck
    const startTime = Date.now();
    const result = await resolver.resolveBottleneck(climateBottleneck, {
      strategy: 'adaptive',
      maxIterations: 5000,
      convergenceThreshold: 0.01,
      explorationTimeout: 60000, // 1 minute
      attractors: ['lorenz', 'chen', 'rossler']
    });

    const duration = (Date.now() - startTime) / 1000;

    // Display results
    console.log('🎉 RESOLUTION COMPLETE');
    console.log('─'.repeat(40));
    console.log(`⏱️  Duration: ${duration.toFixed(1)}s`);
    console.log(`🎯 Best Score: ${result.bestSolution.score.toFixed(4)}`);
    console.log(`🏆 Attractor: ${result.bestSolution.attractor}`);
    console.log(`🔄 Total Iterations: ${result.ensemble.attractorResults.reduce((sum, r) => sum + r.iterations, 0)}`);

    console.log('\n📊 OPTIMAL SOLUTION');
    console.log('─'.repeat(40));
    const solution = result.bestSolution.solution;
    console.log(`Temperature Target: ${solution.temperature_target?.toFixed(2)}°C`);
    console.log(`Emission Reduction: ${(solution.emission_reduction_rate * 100)?.toFixed(1)}%/year`);
    console.log(`Adaptation Investment: ${(solution.adaptation_investment * 100)?.toFixed(1)}%`);
    console.log(`Renewable Energy: ${(solution.renewable_energy_fraction * 100)?.toFixed(1)}%`);
    console.log(`Carbon Price: $${solution.carbon_price?.toFixed(0)}/ton`);

    console.log('\n📈 ENSEMBLE PERFORMANCE');
    console.log('─'.repeat(40));
    result.ensemble.attractorResults.forEach(r => {
      const status = r.converged ? '✅' : '⏳';
      console.log(`${status} ${r.attractor}: ${r.score.toFixed(4)} (${r.iterations} iter)`);
    });

    // Calculate impact
    const impact = climateTemplate.calculateImpact(solution);
    console.log('\n💰 ECONOMIC IMPACT');
    console.log('─'.repeat(40));
    console.log(`Environmental: ${(impact.environmental * 100)?.toFixed(1)} points`);
    console.log(`Economic: ${(impact.economic * 100)?.toFixed(1)} points`);
    console.log(`Social: ${(impact.social * 100)?.toFixed(1)} points`);
    console.log(`Total Impact: ${(impact.total * 100)?.toFixed(1)} points`);

    // Cleanup
    await resolver.close();

  } catch (error) {
    console.error('❌ Demo failed:', error.message);
    process.exit(1);
  }
}

async function demonstrateAttractorEvolution() {
  console.log('\n🔬 Chaos Attractor Evolution Demo');
  console.log('═'.repeat(60));

  const attractor = new LorenzAttractor();
  attractor.setState([1, 1, 1]);

  console.log('Lorenz Attractor Evolution (first 10 steps):');
  console.log('Step |     X     |     Y     |     Z');

  for (let i = 0; i < 10; i++) {
    const state = attractor.state;
    console.log(`${i.toString().padStart(4)} | ${state[0].toFixed(6).padStart(9)} | ${state[1].toFixed(6).padStart(9)} | ${state[2].toFixed(6).padStart(9)}`);
    attractor.evolve();
  }

  // Generate longer trajectory for analysis
  for (let i = 0; i < 990; i++) {
    attractor.evolve();
  }

  const lyapunov = attractor.calculateLyapunovExponent();
  const fractal = attractor.calculateFractalDimension();
  const properties = attractor.getProperties();

  console.log('\n📊 Attractor Analysis:');
  console.log(`Lyapunov Exponent: ${lyapunov.toFixed(4)} (positive = chaotic)`);
  console.log(`Fractal Dimension: ${fractal.toFixed(4)}`);
  console.log(`Trajectory Length: ${properties.trajectoryLength}`);
  console.log(`Is Chaotic: ${properties.isChaotic ? 'Yes' : 'No'}`);
}

async function main() {
  console.log('🚀 Universal Bottleneck Resolver - Live Demonstration\n');

  // Demonstrate attractor evolution
  await demonstrateAttractorEvolution();

  // Demonstrate full bottleneck resolution
  await demonstrateClimateResolution();

  console.log('\n✨ Demo Complete!');
  console.log('💡 Try: npm run cli -- resolve --interactive');
  console.log('🌐 Try: npm run api');
}

if (require.main === module) {
  main().catch(error => {
    console.error('💥 Demo failed:', error.message);
    process.exit(1);
  });
}

module.exports = { demonstrateClimateResolution, demonstrateAttractorEvolution };