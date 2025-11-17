# execute_final_rounds.py Documentation

**Generated:** 2025-11-09T14:29:53.806088
**Source:** C:\Users\regan\ID SYSTEM\axiom-x\execute_final_rounds.py
**Worker ID:** doc-11

## Constitutional Principles Applied

- **Ahimsa**: Generate clear, helpful documentation that prevents confusion and errors
- **Satya**: Ensure all generated content is accurate and truthful
- **Asteya**: Properly attribute any examples or code snippets
- **Brahmacharya**: Focus on essential documentation without unnecessary complexity
- **Aparigraha**: Generate only what's needed, no redundant content

---

# execute_final_rounds.py Documentation

## Purpose & Overview

### What This File Does
`execute_final_rounds.py` is a specialized orchestration script that executes the final two rounds (19 and 20) of the Axiom-X Phase 1 adversarial debate system. It manages the closing arguments from all AI debaters and facilitates a meta-debate among judges to synthesize final conclusions.

### Role in the Axiom-X System
This file represents the culmination of Phase 1 in the Axiom-X self-optimization framework. It:
- Collects final synthesized positions from 9 different AI models (debaters)
- Enables judges to evaluate and debate the presented arguments
- Generates comprehensive receipts for constitutional compliance
- Prepares the system for Phase 2-5 execution based on debate conclusions

### Key Functionality
- **Round 19 Execution**: Orchestrates closing arguments from all debaters with controlled concurrency
- **Round 20 Execution**: Facilitates a judge-vs-judge meta-debate
- **Receipt Generation**: Creates cryptographic receipts for all debate interactions
- **Asynchronous Task Management**: Uses semaphores to control concurrent API calls and prevent rate limiting
- **Error Handling**: Implements retry logic and comprehensive error recovery

---

## Architecture Overview

```
execute_final_rounds.py
│
├── FinalRoundsExecutor (Main Class)
│   ├── __init__()
│   ├── execute_closing_arguments()      # Round 19
│   ├── execute_judge_debate()           # Round 20
│   └── run()                            # Main orchestrator
│
└── main() (Entry Point)
```

---

## Class Documentation

### `FinalRoundsExecutor`

The primary class responsible for executing the final rounds of Phase 1 debate.

#### Class Attributes

```python
DEBATERS = [
    "anthropic-sonnet", 
    "anthropic-opus", 
    "openai-gpt4o", 
    "openai-o1",
    "google-gemini2", 
    "groq-llama", 
    "cohere-command", 
    "google-gemini-pro", 
    "openai-gpt4o-mini"
]
```
List of AI models participating as debaters in the adversarial system.

```python
JUDGES = ["mistral-large", "together-ai", "fireworks"]
```
List of AI models serving as judges to evaluate and synthesize debate outcomes.

#### Methods

##### `__init__(self)`

**Purpose**: Initializes the executor and sets up the output directory.

**Parameters**: None

**Returns**: None

**Side Effects**: 
- Creates `self-optimization/phase1` directory if it doesn't exist

**Example**:
```python
executor = FinalRoundsExecutor()
```

---

##### `async execute_closing_arguments(self)`

**Purpose**: Executes Round 19 where all debaters provide closing arguments.

**Parameters**: None

**Returns**: `dict`
- Dictionary containing closing arguments from all debaters
- Structure:
  ```python
  {
      "round": 19,
      "timestamp": "ISO-8601 timestamp",
      "debater_name": {
          "task_id": "unique_task_id",
          "response": "closing argument text",
          "receipt": "constitutional_receipt_hash",
          "success": True/False
      },
      # ... repeated for each debater
  }
  ```

**Process Flow**:
1. Creates prompts for each debater requesting closing arguments
2. Uses semaphore (limit: 6) to control concurrent API calls
3. Routes tasks through the infrastructure router
4. Generates constitutional receipts for each response
5. Saves results to `round_19_closing.json`

**Error Handling**:
- Captures and logs individual debater failures
- Continues execution even if some debaters fail
- Records error information in output JSON

**Performance Characteristics**:
- Controlled concurrency (max 6 simultaneous requests)
- Typical execution time: 30-120 seconds depending on API response times
- Rate limiting protection through semaphore

**Example**:
```python
executor = FinalRoundsExecutor()
results = await executor.execute_closing_arguments()
print(f"Received {len(results)} closing arguments")
```

**Internal Implementation Pattern**:
```python
async def fire_closing(debater, prompt):
    async with semaphore:
        # Rate limiting control
        task_id = f"closing_{debater}_{int(time.time())}"
        result = await router.route_task(
            task_id=task_id,
            task_type="closing_argument",
            payload={...}
        )
        return result
```

---

##### `async execute_judge_debate(self)`

**Purpose**: Executes Round 20 where judges debate each other's perspectives.

**Parameters**: None

**Returns**: `dict`
- Dictionary containing judge debate results
- Structure:
  ```python
  {
      "round": 20,
      "timestamp": "ISO-8601 timestamp",
      "judge_name": {
          "task_id": "unique_task_id",
          "response": "judge's debate contribution",
          "receipt": "constitutional_receipt_hash",
          "success": True/False
      },
      # ... repeated for each judge
  }
  ```

**Process Flow**:
1. Loads Round 19 results to provide context
2. Creates prompts for judges to debate closing arguments
3. Uses semaphore (limit: 3) for controlled concurrency
4. Routes tasks and generates receipts
5. Saves results to `round_20_judge_debate.json`

**Unique Features**:
- Meta-debate: Judges evaluate other judges' perspectives
- Context-aware: References all closing arguments from Round 19
- Synthesis focus: Encourages judges to find consensus or articulate disagreements

**Example**:
```python
executor = FinalRoundsExecutor()
await executor.execute_closing_arguments()  # Must run first
judge_results = await executor.execute_judge_debate()
```

**Constitutional Compliance**:
- Generates receipts for judge contributions
- Ensures transparency in judicial synthesis
- Creates audit trail for Phase 1 conclusions

---

##### `async run(self)`

**Purpose**: Main orchestration method that executes both rounds sequentially.

**Parameters**: None

**Returns**: `dict`
- Combined results from both rounds
- Structure:
  ```python
  {
      "round_19": {...},  # Closing arguments
      "round_20": {...},  # Judge debate
      "summary": {
          "total_duration": float,  # seconds
          "rounds_completed": 2,
          "total_receipts": int
      }
  }
  ```

**Process Flow**:
1. Executes Round 19 (closing arguments)
2. Brief pause between rounds (2 seconds)
3. Executes Round 20 (judge debate)
4. Calculates execution statistics
5. Saves summary to `final_rounds_summary.json`

**Error Handling**:
- Try-catch blocks around each round
- Logs detailed error information
- Continues to next round even if previous fails

**Example**:
```python
async def main():
    executor = FinalRoundsExecutor()
    results = await executor.run()
    print(f"Completed in {results['summary']['total_duration']:.2f}s")

asyncio.run(main())
```

---

## Dependencies & Requirements

### Core Python Imports

```python
import asyncio          # Asynchronous execution
import json            # JSON serialization
import time            # Timestamp generation
from datetime import datetime  # Human-readable timestamps
from pathlib import Path       # Cross-platform path handling
import sys             # Path manipulation
```

### Axiom-X Infrastructure Dependencies

```python
from infrastructure.sidecar.router import router, TaskResult
```

**Required Components**:
- **Router**: Central task routing system for multi-model orchestration
- **TaskResult**: Data class for standardized task responses

### Commented Import (Development Reference)

```python
# from axiom_receipt_hook import generate_receipt
```
This import is commented but referenced in the file header, suggesting receipt generation functionality is integrated into the router system.