/**
 * Universal Bottleneck Resolver API Server
 * REST API for chaos-theoretic bottleneck resolution
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const BottleneckResolver = require('./core/BottleneckResolver');
const ClimateCoordination = require('./domains/ClimateCoordination');
const HealthcareResources = require('./domains/HealthcareResources');
const SupplyChainOptimization = require('./domains/SupplyChainOptimization');

class BottleneckResolverAPI {
  constructor(port = 3000) {
    this.port = port;
    this.app = express();
    this.resolver = null;
    this.setupMiddleware();
    this.setupRoutes();
  }

  setupMiddleware() {
    // Security middleware
    this.app.use(helmet());

    // CORS support
    this.app.use(cors());

    // Compression
    this.app.use(compression());

    // Body parsing
    this.app.use(express.json({ limit: '10mb' }));
    this.app.use(express.urlencoded({ extended: true }));

    // Request logging
    this.app.use((req, res, next) => {
      console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
      next();
    });
  }

  setupRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        version: '1.0.0'
      });
    });

    // Get available domains
    this.app.get('/domains', (req, res) => {
      const domains = this.getAvailableDomains();
      res.json({
        domains,
        count: domains.length
      });
    });

    // Get domain details
    this.app.get('/domains/:domain', (req, res) => {
      try {
        const domain = this.getDomainDetails(req.params.domain);
        res.json(domain);
      } catch (error) {
        res.status(404).json({ error: error.message });
      }
    });

    // Resolve bottleneck
    this.app.post('/resolve', async (req, res) => {
      try {
        const options = req.body;
        const result = await this.resolver.resolveBottleneck(options.bottleneck, options);

        res.json({
          success: true,
          result,
          timestamp: new Date().toISOString()
        });
      } catch (error) {
        console.error('Resolution error:', error);
        res.status(500).json({
          success: false,
          error: error.message,
          timestamp: new Date().toISOString()
        });
      }
    });

    // Get exploration history
    this.app.get('/explorations/:bottleneckId', async (req, res) => {
      try {
        const history = await this.resolver.getExplorationHistory(req.params.bottleneckId);
        res.json({
          explorations: history,
          count: history.length
        });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    // Get solution details
    this.app.get('/solutions/:solutionId', async (req, res) => {
      try {
        const solution = await this.resolver.getSolution(req.params.solutionId);
        res.json(solution);
      } catch (error) {
        res.status(404).json({ error: error.message });
      }
    });

    // Deploy solution
    this.app.post('/deploy/:solutionId', async (req, res) => {
      try {
        const solution = await this.resolver.getSolution(req.params.solutionId);
        const explorationResult = {
          bestSolution: {
            solution: JSON.parse(solution.solution),
            score: solution.score
          },
          bottleneck: req.body.bottleneck || {}
        };

        const deploymentPlan = await this.resolver.exportForDeployment(
          explorationResult,
          req.body.options || {}
        );

        res.json({
          success: true,
          deploymentId: deploymentPlan.deploymentId,
          plan: deploymentPlan
        });
      } catch (error) {
        res.status(500).json({
          success: false,
          error: error.message
        });
      }
    });

    // Get system status
    this.app.get('/status', async (req, res) => {
      try {
        const status = await this.getSystemStatus();
        res.json(status);
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    // Simulation endpoints
    this.app.post('/simulate/:domain', async (req, res) => {
      try {
        const domain = req.params.domain;
        const solution = req.body.solution;
        const simulation = this.runDomainSimulation(domain, solution);

        res.json({
          success: true,
          simulation,
          domain
        });
      } catch (error) {
        res.status(500).json({
          success: false,
          error: error.message
        });
      }
    });

    // Batch resolution
    this.app.post('/batch-resolve', async (req, res) => {
      try {
        const { bottlenecks, options } = req.body;
        const results = [];

        for (const bottleneck of bottlenecks) {
          try {
            const result = await this.resolver.resolveBottleneck(bottleneck, options);
            results.push({
              bottleneck,
              result,
              success: true
            });
          } catch (error) {
            results.push({
              bottleneck,
              error: error.message,
              success: false
            });
          }
        }

        res.json({
          success: true,
          results,
          total: results.length,
          successful: results.filter(r => r.success).length
        });
      } catch (error) {
        res.status(500).json({
          success: false,
          error: error.message
        });
      }
    });

    // Error handling middleware
    this.app.use((error, req, res, next) => {
      console.error('Unhandled error:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
        timestamp: new Date().toISOString()
      });
    });

    // 404 handler
    this.app.use((req, res) => {
      res.status(404).json({
        success: false,
        error: 'Endpoint not found',
        path: req.path,
        method: req.method
      });
    });
  }

  getAvailableDomains() {
    return [
      {
        id: 'climate',
        name: 'Climate Coordination',
        description: 'Optimize climate change mitigation and adaptation',
        dimensions: 5,
        endpoint: '/domains/climate'
      },
      {
        id: 'healthcare',
        name: 'Healthcare Resources',
        description: 'Optimize medical resource allocation',
        dimensions: 6,
        endpoint: '/domains/healthcare'
      },
      {
        id: 'supply_chain',
        name: 'Supply Chain Optimization',
        description: 'Optimize logistics and inventory management',
        dimensions: 6,
        endpoint: '/domains/supply_chain'
      }
    ];
  }

  getDomainDetails(domainId) {
    let template;

    switch (domainId) {
      case 'climate':
        template = new ClimateCoordination();
        break;
      case 'healthcare':
        template = new HealthcareResources();
        break;
      case 'supply_chain':
        template = new SupplyChainOptimization();
        break;
      default:
        throw new Error(`Unknown domain: ${domainId}`);
    }

    return {
      id: domainId,
      ...template.getMetadata(),
      variables: template.getVariables(),
      constraints: template.getConstraints(),
      objective: template.getObjective(),
      attractorPreferences: template.getAttractorPreferences()
    };
  }

  async getSystemStatus() {
    return {
      status: 'operational',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      components: {
        database: 'connected',
        attractors: ['lorenz', 'chen', 'rossler'],
        domains: ['climate', 'healthcare', 'supply_chain'],
        api: 'running'
      },
      capabilities: {
        maxConcurrentExplorations: 10,
        supportedStrategies: ['parallel', 'sequential', 'adaptive'],
        maxIterations: 50000,
        timeoutLimit: 3600 // seconds
      }
    };
  }

  runDomainSimulation(domain, solution) {
    let template;

    switch (domain) {
      case 'healthcare':
        template = new HealthcareResources();
        return template.simulatePatientFlow(solution);
      case 'supply_chain':
        template = new SupplyChainOptimization();
        return template.simulateSupplyChainDynamics(solution);
      case 'climate':
        template = new ClimateCoordination();
        // Climate simulation would be more complex
        return { message: 'Climate simulation not yet implemented' };
      default:
        throw new Error(`Unknown domain for simulation: ${domain}`);
    }
  }

  async initialize() {
    try {
      this.resolver = new BottleneckResolver();
      await this.resolver.initialize();
      console.log('🚀 Bottleneck Resolver API initialized');
    } catch (error) {
      console.error('❌ Failed to initialize API:', error.message);
      throw error;
    }
  }

  async start() {
    await this.initialize();

    return new Promise((resolve) => {
      this.server = this.app.listen(this.port, () => {
        console.log(`🌐 API Server running on port ${this.port}`);
        console.log(`📖 API Documentation: http://localhost:${this.port}`);
        console.log(`❤️  Health Check: http://localhost:${this.port}/health`);
        resolve(this.server);
      });
    });
  }

  async stop() {
    if (this.server) {
      await new Promise((resolve) => {
        this.server.close(resolve);
      });
      console.log('🛑 API Server stopped');
    }

    if (this.resolver) {
      await this.resolver.close();
    }
  }
}

// Export for testing and standalone usage
module.exports = BottleneckResolverAPI;

// Start server if called directly
if (require.main === module) {
  const port = process.env.PORT || 3000;
  const api = new BottleneckResolverAPI(port);

  // Graceful shutdown
  process.on('SIGINT', async () => {
    console.log('\n🛑 Shutting down gracefully...');
    await api.stop();
    process.exit(0);
  });

  process.on('SIGTERM', async () => {
    console.log('\n🛑 Shutting down gracefully...');
    await api.stop();
    process.exit(0);
  });

  api.start().catch(error => {
    console.error('💥 Failed to start API server:', error.message);
    process.exit(1);
  });
}