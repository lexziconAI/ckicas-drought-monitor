# AXIOM-X DUAL-SYSTEM ARCHITECTURE - VISUAL DOCUMENTATION

## Layer 1: System Overview

```
╔══════════════════════════════════════════════════════════════════╗
║                     AXIOM-X ORCHESTRATOR                        ║
║              Constitutional AI Governance Layer                  ║
║                                                                  ║
║  ┌─────────────────────────────────────────────────────────┐   ║
║  │  Yama Principles (Ethical Constraints)                   │   ║
║  │  ├─ Ahimsa: Non-harm verification                        │   ║
║  │  ├─ Satya: Transparent reasoning                         │   ║
║  │  ├─ Asteya: Attribution enforcement                      │   ║
║  │  ├─ Brahmacharya: Resource efficiency                    │   ║
║  │  └─ Aparigraha: Knowledge sharing                        │   ║
║  └─────────────────────────────────────────────────────────┘   ║
╚══════════════════════════════════════════════════════════════════╝
                              │
              ┌───────────────┴────────────────┐
              │                                 │
╔═════════════▼═══════════╗      ╔═════════════▼══════════════╗
║   PHASE 2 VALIDATOR     ║      ║  INFRASTRUCTURE WORKERS   ║
║      (Validation)       ║      ║      (Development)        ║
║                         ║      ║                           ║
║  Agents: 2,794          ║      ║  Workers: 100             ║
║  Batch: 400 concurrent  ║      ║  Continuous execution     ║
║  Duration: 4-5 min      ║      ║  Specialties: 5 types     ║
║                         ║      ║                           ║
║  ┌──────────────────┐  ║      ║  ┌────────────────────┐  ║
║  │ 270 Scouts       │  ║      ║  │ 30 Code Generators │  ║
║  │ 27 Extractors    │  ║      ║  │ 20 Architects      │  ║
║  │ 1,350 Validators │  ║      ║  │ 20 Testers         │  ║
║  │ 1,147 Specialists│  ║      ║  │ 15 Documenters     │  ║
║  └──────────────────┘  ║      ║  │ 15 Optimizers      │  ║
║                         ║      ║  └────────────────────┘  ║
╚═════════════╬═══════════╝      ╚═════════════╬════════════╝
              │                                 │
              └────────────┬────────────────────┘
                           │
╔═══════════════════════════▼════════════════════════════════════╗
║              BEAST MODE ORCHESTRATOR                           ║
║           Multi-Provider Load Balancer                         ║
║                                                                ║
║  ┌────────────────────────────────────────────────────────┐  ║
║  │  Provider Distribution (800 concurrent capacity)       │  ║
║  │                                                         │  ║
║  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │  ║
║  │  │Anthropic│  │ OpenAI  │  │ Google  │  │  Groq   │ │  ║
║  │  │  150    │  │  150    │  │  100    │  │  200    │ │  ║
║  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │  ║
║  │                                                         │  ║
║  │  ┌─────────┐  ┌──────────┐                            │  ║
║  │  │ Cohere  │  │Fireworks │                            │  ║
║  │  │  100    │  │   100    │                            │  ║
║  │  └─────────┘  └──────────┘                            │  ║
║  │                                                         │  ║
║  │  Rate Limiting: 2-second recovery between batches     │  ║
║  │  Thompson Sampling: Adaptive provider selection       │  ║
║  └────────────────────────────────────────────────────────┘  ║
╚════════════════════════════════════════════════════════════════╝
```

## Layer 2: Data Flow

```
INPUT:
┌──────────────────────────────────────┐
│ Axiom-X Codebase                     │
│ ├─ 100+ Python files                 │
│ ├─ JSON performance receipts         │
│ ├─ YAML configurations               │
│ └─ Historical breakthrough data      │
└──────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│ Phase 2: File Discovery & Mining     │
│ └─ 500 scouts scan directories       │
│ └─ 500 miners parse receipts         │
└──────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│ Phase 2: Comparison & Validation     │
│ └─ 647 agents compare files          │
│ └─ AST analysis, performance delta   │
│ └─ Constitutional compliance check   │
└──────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│ Phase 2: Canonical Selection         │
│ └─ Multi-criteria ranking            │
│ └─ Consensus validation (>0.85)      │
│ └─ Redundancy identification         │
└──────────────────────────────────────┘
                 │
                 ▼
OUTPUT:
┌──────────────────────────────────────┐
│ ✅ canonical_files_map.yaml          │
│ ✅ redundant_files_list.json         │
│ ✅ performance_timeline.json         │
│ ✅ CONSTITUTIONAL_RECEIPT.json       │
└──────────────────────────────────────┘

PARALLEL PROCESS (Infrastructure):
┌──────────────────────────────────────┐
│ Continuous Development               │
│ ├─ New feature generation            │
│ ├─ Architecture designs              │
│ ├─ Test suite creation               │
│ └─ Documentation writing             │
└──────────────────────────────────────┘
```

---

END ARCHITECTURE VISUAL