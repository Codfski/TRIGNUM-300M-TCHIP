# TRIGNUM-300M / T-CHIP — External Engineering Handoff

**Target:** Gemini / Copilot / External Engineers  
**Purpose:** Independent technical evaluation, calibration, and architectural continuation  
**Status:** Pre-Flight (Experimental Logical Filtering Layer)

---

## 1. Executive Summary

TRIGNUM-300M is not a language model and is not intended to compete with LLMs.

It is a **deterministic Validator-Driven Feedback layer** designed to run before or alongside an Agentic workflow in order to:

> _"Provide structural constraint-checking for Foundational Agentic Reasoning, removing impossible thought-trajectories prior to external action."_

This system follows a **subtractive epistemology**:

```
Truth ≈ Input − Detectable Illogics
```

Instead of verifying correctness (open-ended, expensive),  
we eliminate known-invalid reasoning forms (finite, computable).

Think of it as:

> _"A deterministic 'Critic/Evaluator' for single-agent reflection and Multi-Agent Systems (MAS)."_

---

## 2. What Has Been Built So Far

### Core Component

**`SubtractiveFilter`** — detects universal reasoning pathologies:

| Illogic Type          | Description                                |
| --------------------- | ------------------------------------------ |
| `contradiction`       | A ∧ ¬A — mutually exclusive claims coexist |
| `circular_reference`  | A proves B proves A                        |
| `non_sequitur`        | Conclusion doesn't follow premises         |
| `category_error`      | Wrong logical frame applied to data        |
| `false_dichotomy`     | Only two options when more exist           |
| `infinite_regress`    | Explanation requires an infinite chain     |
| `ad_hominem`          | Attacking person, not argument             |
| `appeal_to_authority` | True because X said so                     |
| `straw_man`           | Attacking a misrepresented position        |
| `begging_question`    | Conclusion assumed in premises             |

These are treated as **cross-domain invariants** rather than dataset-specific hallucinations.

### Current Processing Model

```
Raw Text
   ↓
Pattern-based Illogic Detection
   ↓
Subtract Invalid Structures
   ↓
Return Residual ("Truth Candidate")
```

No embeddings. No training. No probabilistic scoring. **This is intentional.**

---

## 3. Benchmark Results (Observed Behaviour)

### Throughput

- ≈ 52,581 samples / second
- ≈ 1.1 seconds for 58,338 evaluations
- **Zero API calls. Runs entirely offline.**

This confirms the architecture is lightweight enough for:

- Edge deployment for Embodied Agents
- Inline inference sanitation for self-evolving agents
- Agentic Search (RAG) pre-processing
- Real-time Critic/Evaluator roles in Multi-Agent Swarms

---

### ⚠️ DO NOT READ THESE NUMBERS IN ISOLATION

The aggregate metrics below cover **factual hallucination datasets** (HaluEval, TruthfulQA) where T-CHIP is not designed to operate. Reading only the aggregate will misrepresent the system.

### Aggregate Metrics (all databases, including factual datasets)

| Metric    | Value  | Note                                            |
| --------- | ------ | ----------------------------------------------- |
| Precision | 0.62   | When it flags, it's right 62% of the time       |
| Recall    | 0.03   | Low **by design** — not catching factual errors |
| F1        | 0.059  | Misleading in this context (see §4)             |
| Accuracy  | 0.49   | Split ~50/50 on factual datasets by chance      |
| Samples   | 58,338 | Across 4 databases                              |

### Structural Logic Suite (T-CHIP's Actual Mandate)

| Metric           | Value          | Interpretation                          |
| ---------------- | -------------- | --------------------------------------- |
| **Precision**    | **1.00**       | **Zero false alarms on clean text**     |
| **Recall**       | **0.84**       | Catches 84% of planted logic faults     |
| **F1**           | **0.913**      | Strong performance on its design target |
| **Accuracy**     | **0.911**      | 91.1% overall correct classification    |
| False Alarm Rate | **0.0%**       | No clean statements wrongly flagged     |
| Speed            | **41,763/sec** | Structural suite alone                  |

**The structural suite is the correct evaluation surface for T-CHIP.**  
The aggregate numbers measure the wrong capability.

### Per-Database Breakdown

| Database                     | Purpose                        | Samples | Precision | Recall |        F1 |
| ---------------------------- | ------------------------------ | ------: | --------: | -----: | --------: |
| [A] TRIGNUM Structural Suite | Logic faults (T-CHIP's domain) |      45 |      1.00 |   0.84 | **0.913** |
| [B] HaluEval QA              | Factual LLM errors             |  18,316 |      0.86 |  0.003 |     0.006 |
| [C] HaluEval Dialogue        | Factual dialogue errors        |  19,977 |      0.60 |  0.044 |     0.083 |
| [D] HaluEval Summarization   | Factual summary errors         |  20,000 |      0.61 |  0.043 |     0.080 |

---

## 4. Why Classical Hallucination Benchmarks Mis-Evaluate This System

Datasets like HaluEval and TruthfulQA test:

> _"Whether a statement matches ground truth knowledge."_

TRIGNUM tests:

> _"Whether reasoning violates logical coherence constraints."_

| Dataset asks             | T-CHIP answers                   |
| ------------------------ | -------------------------------- |
| Is this factually wrong? | Is this structurally impossible? |

These are **orthogonal axes**. TRIGNUM is operating at a pre-factual layer.

---

## 5. Current Weakness (Important)

Detection is presently **lexical-heuristic**.

Example:

```
if "always" and "never" appear → contradiction
```

This is insufficient because:

- Logical conflict ≠ word collision
- Many hallucinations are structurally valid but factually false
- The system lacks an intermediate reasoning representation

> **Clarification:** The fact that T-CHIP cannot detect factually-false-but-structurally-valid claims is **correct by design**, not a gap to fix. The Claim Representation Layer (§6) is intended to improve precision on _structural_ detection only. Factual grounding remains a separate pipeline concern (Tensor RAG layer).

---

## 6. Required Architectural Shift (Critical Next Step)

We must insert a **Claim Representation Layer** before filtering.

### Target Pipeline

```
Text
 ↓
Claim Extraction
 ↓
Relation Graph
 ↓
Logical Validation (SubtractiveFilter)
 ↓
Clean Reasoning Substrate
 ↓
LLM / RAG / Generation
```

This allows the filter to operate on **meaning structure**, not tokens.

---

## 7. Minimal Representation Schema (Do NOT Overbuild)

We are **NOT** building symbolic AI.

We need only a lightweight triple form:

```python
Claim(
    subject  = "Drug A",
    relation = "causes",
    object   = "Liver Damage",
    polarity = "asserted"   # or "negated"
)
```

Contradiction becomes computable:

```
(A causes B) ∧ (A does_not_cause B)
```

**No ontology required. No reasoning engine required.** Just relational normalization.

---

## 8. What Engineers Should Implement Next

### Task 1 — Claim Extraction Adapter

Build a deterministic parser that converts sentences into:

```
(subject, relation, object, polarity)
```

**Implementation constraint:** O(n), no ML training, runs offline.

**Recommended library:** `spaCy` (`en_core_web_sm`) — deterministic, lightweight, zero training cost, compatible with the project's sovereign-compute philosophy.

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

---

### Task 2 — Structural Conflict Engine

Replace keyword detection with relation validation. Detect:

- Predicate negation conflicts: `(A causes B)` + `(A not causes B)`
- Self-referential loops: claim chain circles back to its own subject
- Unsupported causal jumps: "therefore" with no supporting relation path
- Recursive justification chains: A justified by B justified by A

---

### Task 3 — Calibration Harness

Do **NOT** evaluate using hallucination datasets alone.

#### Evaluation Axes

| Axis                           | Description                                                       | Current      | Target              |
| ------------------------------ | ----------------------------------------------------------------- | ------------ | ------------------- |
| Structural Logic F1            | Detection on curated logic faults                                 | 0.913        | **> 0.95**          |
| False Alarm Rate               | Clean text wrongly flagged                                        | 0.0%         | **< 2%**            |
| Downstream LLM Error Reduction | Fewer structural errors in LLM generation when used as pre-filter | (unmeasured) | **> 15% reduction** |

We care about **error prevention**, not classification accuracy.

---

### Task 4 — Integration Simulation

Test TRIGNUM as a front-layer to a small open model:

```
User Query
  → TRIGNUM sanitation
  → LLM generation
  → Compare hallucination delta
```

Measure whether removing illogic reduces fabrication.  
Suggested model: `Mistral-7B-Instruct` or `Phi-3-mini` (lightweight, locally runnable).

---

## 9. Repository Structure (Start Here)

```
TRIGNUM-300M-TCHIP/
│
├── src/trignum_core/
│   ├── subtractive_filter.py        ← Core filter (START HERE)
│   └── ...
│
├── benchmarks/
│   ├── hallucination_benchmark.py   ← Structural test suite (30 curated cases)
│   ├── tchip_preflight_report.py    ← Full cross-database benchmark runner
│   ├── tchip_preflight_results.json ← Latest benchmark output (real numbers)
│   ├── multi_dataset_benchmark.py   ← Cross-domain runner (TQA + HaluEval + Med)
│   └── AVAILABLE_HALLUCINATION_DATASETS.md  ← Dataset research
│
├── tests/                           ← 34 passing unit tests
├── paper/                           ← Position paper (HTML)
├── T-CHIP CLEARED FOR TAKEOFF.md    ← Public-facing conceptual overview
└── README.md
```

---

## 10. Environment

```
Python:       3.10+
Dependencies: None (stdlib only — current implementation is dependency-free)
Optional:     spaCy >= 3.7  (required for Task 1 Claim Extraction)
Test runner:  python -m unittest discover tests/
Benchmark:    python benchmarks/tchip_preflight_report.py
```

---

## 11. What This Project Is (Correct Positioning)

TRIGNUM is best described as:

> _"A Pre-Semantic Reasoning Sanitizer for Generative Systems"_

| Traditional Systems   | TRIGNUM Role                               |
| --------------------- | ------------------------------------------ |
| Compiler type-checker | Validator-Driven Feedback for Agentic LLMs |

It validates **reasoning geometry**, not answer truth.

---

## 12. What It Is NOT

Do **NOT** evolve this into:

- a fact checker
- a verifier model
- a classifier
- another LLM
- a knowledge-grounding engine

That would destroy its computational advantage.

---

## 13. Success Criteria Going Forward

The project succeeds if:

- ✔ It runs faster than generation (`< 1ms per reasoning chain`)
- ✔ It reduces downstream hallucinations indirectly
- ✔ It remains training-free
- ✔ It works cross-domain without tuning
- ✔ It behaves like a structural invariant layer

---

## 14. Immediate Deliverables

1. Implement Claim Extraction Prototype (spaCy, O(n), no training)
2. Replace lexical contradiction detection with relational validation
3. Re-run benchmark using structure-aware filter
4. Provide delta analysis vs. current metrics (target F1 > 0.95 on structural suite)
5. Stress test with adversarial phrasing

---

## Closing Note

This system explores a different question than modern AI:

> _"Instead of asking how machines can know more,  
> ask how they can avoid reasoning incorrectly."_

That inversion is the entire premise.

---

_TRACE ON LAB © 2026 | Sovereign Architecture | TRIGNUM-300M T-CHIP_
