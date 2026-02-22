# Architecture Overview

The TRIGNUM-300M framework is a deterministic logic constraint engine that operates pre-generation.

## 1. The Pyramid Logic Structure

The system is theoretically grounded in the "Tracing Pyramid":

- **Alpha Face**: Logic (Truth preservation)
- **Beta Face**: Illogic (Contradiction and Falsehood)
- **Gamma Face**: Human Context (The ultimate sovereign pulse)

## 2. Core Components

### `SubtractiveFilter`

The main Python class. Instead of fact-checking via search, it parses a prompt or LLM intermediate thought against a static set of `UNIVERSAL_ILLOGICS`. If logic fails structurally, the agent halts.

### `Evaluator`

Computes precision, recall, and F1 across multiple benchmarks to evaluate the structural filter's boundaries against semantic datasets.

### `T-CHIP Emulator`

A theoretical hardware component (and software mock) that dictates Agent execution states:

- `BLUE`: Cleared (Logic holds)
- `RED`: Halted (Illogic detected)
- `GOLD`: Human Sovereign Override

See `README.md` for execution graphs and `ROADMAP.md` for next Level 2 (Semantic Expansion) features.
