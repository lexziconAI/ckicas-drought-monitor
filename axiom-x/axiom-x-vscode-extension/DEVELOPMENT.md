# Axiom-X Extension Development Guide

## 🎯 Vision

**An IDE that teaches itself to orchestrate better** - providing a **10-50x productivity multiplier** by learning optimal parallelization patterns from constitutional receipts.

## 🏗️ Architecture

### Core Components

#### 1. **Receipt Watcher** (`src/services/receipt-watcher.ts`)
- Monitors workspace for receipt files using chokidar
- Processes receipts in PARALLEL (embed + analyze)
- Fire-and-forget storage (non-blocking)
- Detects novel insights and notifies user

#### 2. **Embedding Service** (`src/services/embedding-service.ts`)
- OpenAI `text-embedding-3-large` (3072-dim vectors)
- ChromaDB vector storage in extension global storage
- Semantic similarity search
- Finds similar past executions

#### 3. **Pattern Analyzer** (`src/services/pattern-analyzer.ts`)
- Claude 3.7 powered analysis
- Calculates success rates for spawn patterns
- Generates optimization suggestions
- Detects novel patterns (meta-learning)
- Persists knowledge base

#### 4. **CodeLens Provider** (`src/providers/codelens-provider.ts`)
- Inline intelligence in editor
- Shows success rates for spawn patterns
- Warnings for Yama violations
- Optimization suggestions with expected speedup

#### 5. **Tree Data Provider** (`src/providers/tree-data-provider.ts`)
- Sidebar view of receipts
- Grouped by clusters/patterns
- Click to view details

#### 6. **Commands** (`src/commands/index.ts`)
- `analyzeWorkspace` - Analyze all patterns
- `suggestSpawn` - AI-powered spawn recommendations
- `visualizeClusters` - View receipt clusters
- `showSpawnAnalysis` - Detailed pattern analysis
- `applyOptimization` - Apply suggested changes
- `forceRescan` - Re-process all receipts

## 🚀 Development Workflow

### 1. Setup

```bash
cd axiom-x-vscode-extension
npm install
npm run compile
```

### 2. Configure API Keys

Create `.env` in workspace root:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run Extension

Press `F5` in VS Code to launch Extension Development Host.

### 4. Test Features

1. **Receipt Watching**: Create a file ending in `_receipt.json`
2. **CodeLens**: Open TypeScript/JavaScript/Python file with `Promise.all()`
3. **Commands**: Open command palette (`Ctrl+Shift+P`) and search "Axiom-X"
4. **Tree View**: Check sidebar for "Constitutional Receipts"

### 5. Debug

- Console: Use `outputChannel.appendLine()` - visible in "Axiom-X Intelligence" output
- Breakpoints: Set in any `.ts` file
- DevTools: `Help > Toggle Developer Tools` in Extension Development Host

## 📊 Receipt Schema

Flexible schema supporting multiple formats:

```json
{
  "task": "Description of what was attempted",
  "execution": {
    "strategy": "parallel|sequential|fractal",
    "agent_count": 10,
    "model": "claude-3-7-sonnet-20250219"
  },
  "constitutional": {
    "yama_adherence": 0.95,
    "violations": []
  },
  "outcome": {
    "success": true,
    "duration": 45.2,
    "quality_score": 0.87
  }
}
```

## 🧠 Meta-Learning Pipeline

1. **Receipt Created** → Receipt Watcher detects file
2. **Parallel Processing**:
   - Embed receipt (OpenAI)
   - Analyze pattern (Claude)
3. **Storage**: Store embedding + metadata in ChromaDB
4. **Pattern Detection**: Find similar receipts, calculate success rates
5. **Novel Insights**: Claude detects new patterns
6. **Knowledge Base**: Update persistent learning
7. **CodeLens Update**: Refresh inline intelligence

## 🔧 Configuration

Extension settings in `.vscode/settings.json`:

```json
{
  "axiom-x.receiptPaths": ["**/*_receipt.json"],
  "axiom-x.embeddingModel": "text-embedding-3-large",
  "axiom-x.analysisModel": "claude-3-7-sonnet-20250219",
  "axiom-x.enableCodeLens": true,
  "axiom-x.autoEmbedReceipts": true,
  "axiom-x.minSimilarReceipts": 5
}
```

## 🎨 Design Patterns

### Parallel-First Architecture

All independent operations use `Promise.all()`:

```typescript
const [embeddingSvc, patternSvc] = await Promise.all([
  initializeEmbeddingService(),
  initializePatternAnalyzer()
]);
```

### Fire-and-Forget Receipts

Receipt processing is non-blocking:

```typescript
// Don't await storage - background worker
this.embeddingService.store(id, embedding, metadata);
```

### Constitutional Meta-Learning

System learns from Yama violations:

```typescript
if (analysis.warnings.some(w => w.type === 'yama_violation')) {
  // Update patterns to avoid this mistake
  await patternAnalyzer.updatePatterns(receipt, similar);
}
```

## 📦 Building & Publishing

### Build VSIX Package

```bash
npm install -g @vscode/vsce
vsce package
```

Creates `axiom-x-intelligence-0.1.0.vsix`.

### Install Locally

```bash
code --install-extension axiom-x-intelligence-0.1.0.vsix
```

### Publish to Marketplace

1. Create publisher account: https://marketplace.visualstudio.com/manage
2. Generate PAT (Personal Access Token)
3. Login: `vsce login <publisher>`
4. Publish: `vsce publish`

## 🧪 Testing

### Unit Tests (TODO)

```bash
npm test
```

### Integration Tests (Manual)

1. Create test receipts in `test_data/`
2. Run extension
3. Verify:
   - Receipts appear in tree view
   - CodeLens shows success rates
   - Optimizations suggested
   - Novel patterns detected

## 🔮 Future Enhancements

### Phase 2 (Quick - 1-2 weeks)

- [ ] WebView cluster visualization (UMAP dimensionality reduction)
- [ ] Spawn recommender (LLM-powered suggestions)
- [ ] CKICAS receipt bridge (Python integration)
- [ ] Hover provider (detailed pattern info on hover)
- [ ] Quick actions (one-click apply optimizations)

### Phase 3 (Thorough - 1-3 months)

- [ ] Real-time collaborative learning (share patterns across team)
- [ ] A/B testing spawns (compare strategies automatically)
- [ ] Constitutional policy editor (visual Yama rule management)
- [ ] Benchmark suite integration (link to performance data)
- [ ] Multi-language support (Java, C#, Go, Rust)

## 📚 Resources

- [VS Code Extension API](https://code.visualstudio.com/api)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Anthropic Claude](https://docs.anthropic.com/claude/docs)
- [ChromaDB](https://docs.trychroma.com/)

## 🐛 Known Issues

1. **ChromaDB Persistence**: Collection recreated on each activation (fix: use workspace storage)
2. **Pattern Detection Regex**: May miss complex patterns (TODO: use AST parsing)
3. **Type Safety**: Some `any` casts for third-party modules (TODO: create declaration files)

## 🤝 Contributing

This is internal Axiom Intelligence tooling. For questions:
- See architecture docs in parent directory
- Check CHECKPOINT_PRE_MAJOR_OVERHAUL.md for system state
- Review ADVANCED_FRACTAL_ARMY_RESULTS.json for patterns

---

**Status**: ✅ MVP Complete (2025-01-28)
**Next**: Test with real CKICAS receipts, then deploy Phase 2
