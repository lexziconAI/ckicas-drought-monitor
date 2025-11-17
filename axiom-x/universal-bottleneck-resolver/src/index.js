#!/usr/bin/env node

/**
 * Universal Bottleneck Resolver
 * Main entry point for CLI and API server
 */

const BottleneckResolverCLI = require('./cli/BottleneckResolverCLI');
const BottleneckResolverAPI = require('./api/BottleneckResolverAPI');

async function main() {
  const args = process.argv.slice(2);

  // Check if running as API server
  if (args.includes('--api') || args.includes('serve') || process.env.RUN_API === 'true') {
    const port = process.env.PORT || 3000;
    const api = new BottleneckResolverAPI(port);

    try {
      await api.start();
    } catch (error) {
      console.error('💥 Failed to start API server:', error.message);
      process.exit(1);
    }

    return;
  }

  // Run CLI
  const cli = new BottleneckResolverCLI();

  try {
    await cli.run();
  } catch (error) {
    console.error('💥 CLI execution failed:', error.message);
    process.exit(1);
  }
}

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('💥 Uncaught Exception:', error.message);
  console.error(error.stack);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('💥 Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Run the application
if (require.main === module) {
  main().catch(error => {
    console.error('💥 Fatal error:', error.message);
    process.exit(1);
  });
}