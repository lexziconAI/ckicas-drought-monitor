"use strict";
/**
 * Integration Test Script
 *
 * Tests the streaming architecture integration with synthetic receipts
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const path = __importStar(require("path"));
const stream_processor_1 = require("./src/receipts/stream-processor");
const streaming_analyzer_1 = require("./src/learning/streaming-analyzer");
const atomic_updater_1 = require("./src/context/atomic-updater");
const embedding_service_1 = require("./src/services/embedding-service");
async function createSyntheticReceipts(count) {
    const receipts = [];
    for (let i = 0; i < count; i++) {
        receipts.push({
            id: `test-receipt-${i + 1}`,
            timestamp: new Date().toISOString(),
            task: `Test task ${i + 1}`,
            execution: {
                strategy: i % 2 === 0 ? 'parallel' : 'sequential',
                model: 'gpt-4',
                agent_count: Math.floor(Math.random() * 10) + 1,
                duration_ms: Math.floor(Math.random() * 5000) + 1000,
                wall_clock_speedup: Math.random() * 2 + 0.5,
                cost: Math.random() * 2
            },
            constitutional: {
                yama_adherence: Math.random() * 100,
                violations_detected: Math.random() > 0.9 ? ['test-violation'] : []
            },
            outcome: {
                success: Math.random() > 0.1, // 90% success rate
                quality_score: Math.random() * 100
            }
        });
    }
    return receipts;
}
async function testStreamingIntegration() {
    console.log('🧪 Testing Axiom-X Streaming Integration...');
    try {
        // Create mock output channel
        const outputChannel = {
            appendLine: (msg) => console.log(`[OUTPUT] ${msg}`),
            show: () => { }
        };
        // Create mock extension context
        const mockContext = {
            globalStorageUri: { fsPath: path.join(__dirname, 'test-storage') }
        };
        // Initialize components
        const workspacePath = path.join(__dirname, '../');
        const receiptsPath = path.join(workspacePath, 'test-receipts.jsonl');
        const contextPath = path.join(workspacePath, '.axiom', 'context.json');
        // Create receipt stream processor
        const receiptStream = new stream_processor_1.ReceiptStreamProcessor(workspacePath, contextPath, outputChannel);
        // Create atomic updater
        const atomicUpdater = new atomic_updater_1.AtomicContextUpdater(contextPath, outputChannel);
        // Create streaming analyzer
        const streamingAnalyzer = new streaming_analyzer_1.StreamingPatternAnalyzer(atomicUpdater, undefined, // embedding service optional
        outputChannel);
        // Create embedding service
        const embeddingService = new embedding_service_1.EmbeddingService(mockContext, workspacePath);
        streamingAnalyzer.setEmbeddingService(embeddingService);
        // Initialize receipt stream
        await receiptStream.initialize();
        // Connect streaming analyzer to receipt events
        receiptStream.on('receipt', async (receipt) => {
            console.log(`📄 Processing receipt: ${receipt.task}`);
            await streamingAnalyzer.processReceipt(receipt);
        });
        // Generate and emit synthetic receipts
        console.log('📤 Generating 10 synthetic receipts...');
        const syntheticReceipts = await createSyntheticReceipts(10);
        for (const receipt of syntheticReceipts) {
            await receiptStream.emitReceipt(receipt);
            await new Promise(resolve => setTimeout(resolve, 100)); // Small delay
        }
        // Wait for processing
        await new Promise(resolve => setTimeout(resolve, 2000));
        // Get stats
        const streamStats = receiptStream.getStats();
        const learningStats = streamingAnalyzer.getMetrics();
        console.log('✅ Integration test completed successfully!');
        console.log('📊 Stream Stats:', streamStats);
        console.log('📊 Learning Stats:', learningStats);
        console.log('📊 Check test-receipts.jsonl and .axiom/context.json for results');
        // Cleanup
        await receiptStream.dispose();
    }
    catch (error) {
        console.error('❌ Integration test failed:', error);
        process.exit(1);
    }
}
// Run the test
testStreamingIntegration();
//# sourceMappingURL=test-integration.js.map