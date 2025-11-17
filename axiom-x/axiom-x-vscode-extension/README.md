# Axiom-X Constitutional Intelligence Extension

VS Code extension that learns optimal parallelization patterns from constitutional receipts.

## Features

- **Real-time Receipt Monitoring**: Watches for new receipts and learns patterns automatically
- **Inline Intelligence**: CodeLens shows success rates and optimization suggestions
- **Pattern Analysis**: Detects when to use parallel vs sequential execution
- **Constitutional Compliance**: Tracks Yama principle violations
- **Semantic Search**: Finds similar past executions using embeddings

## Installation

1. Install dependencies:
```bash
cd axiom-x-vscode-extension
npm install
```

2. Configure API keys in workspace `.env`:
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

3. Compile TypeScript:
```bash
npm run compile
```

4. Press F5 to debug in Extension Development Host

## Usage

The extension activates automatically when it detects receipt files in your workspace.

### Commands

- `Axiom-X: Analyze Receipt Patterns` - Analyze workspace patterns
- `Axiom-X: Suggest Parallelization Strategy` - Get AI recommendations
- `Axiom-X: Visualize Receipt Clusters` - View pattern clusters
- `Axiom-X: Force Receipt Rescan` - Re-process all receipts

### Configuration

- `axiom-x.receiptPaths` - Glob patterns for receipt files
- `axiom-x.embeddingModel` - OpenAI embedding model
- `axiom-x.analysisModel` - LLM for analysis
- `axiom-x.enableCodeLens` - Show inline intelligence
- `axiom-x.autoEmbedReceipts` - Auto-process new receipts

## License

Proprietary - Axiom Intelligence Limited
