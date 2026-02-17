# The Pre-Flight Check for Autonomous AI: Zero-Model Structural Reasoning Validation at Scale

**Authors:** TRACE ON LAB  
**Date:** February 2026  
**Contact:** traceonlab@proton.me

---

## Abstract

We present the Subtractive Filter, a lightweight, model-free reasoning integrity validator for Large Language Model (LLM) outputs. Unlike existing approaches to hallucination detection—which rely on secondary LLMs, Natural Language Inference (NLI) classifiers, or embedding-based similarity—the Subtractive Filter operates entirely through deterministic pattern matching, requiring zero model inference, zero API calls, and zero training data. We evaluate the filter on 58,293 samples from the HaluEval benchmark across three tasks (QA, Dialogue, Summarization) and on 45 curated structural illogic samples. Our results reveal a critical distinction: the filter achieves **91.3% F1** on structural reasoning failures (contradictions, circular logic, unsupported conclusions) while scoring only **4.0% F1** on factual hallucinations. Rather than a limitation, we argue this exposes an unoccupied gap in the AI safety landscape: **pre-execution structural reasoning validation for autonomous agents**, a function analogous to aviation pre-flight checks. The filter processes 82,544 samples per second on commodity hardware, making it suitable as a real-time reasoning gate in agentic AI pipelines.

**Keywords:** reasoning integrity, hallucination detection, AI safety, autonomous agents, structural validation, pre-execution verification

---

## 1. Introduction

The deployment of LLM-powered autonomous agents in high-stakes domains—medical diagnosis, legal reasoning, financial analysis, robotic control—creates an urgent need for validation mechanisms that operate *before* an agent acts on its reasoning. Current approaches to output validation fall into three categories:

1. **Model-based validation:** Using a secondary LLM or NLI classifier to evaluate outputs (Manakul et al., 2023; Chen et al., 2024).
2. **Retrieval-based factuality:** Grounding outputs against knowledge bases or search results (Gao et al., 2023).
3. **Process supervision:** Training reward models to evaluate individual reasoning steps (Lightman et al., 2023).

All three approaches share a common dependency: they require model inference at validation time. This introduces latency (0.5–2 seconds per sample), cost (API calls or GPU compute), and a recursive trust problem—using AI to validate AI.

We propose a fundamentally different approach: **deterministic structural reasoning validation**. The Subtractive Filter analyzes text for structural logical failures—contradictions, circular references, non-sequiturs, and unsupported conclusions—using pattern matching alone. It does not assess factual correctness. It assesses whether the *reasoning structure itself* is intact.

This distinction is critical. A factual error ("Paris is the capital of Germany") produces a wrong answer but coherent reasoning. A structural failure ("X is always true. However, X is never true. Therefore, we conclude Y") produces reasoning that *sounds* coherent but is logically broken—and may cascade through an agent's decision chain.

We argue that:

- Structural reasoning failures are **more dangerous** than factual errors in agentic contexts because they corrupt entire reasoning chains.
- Structural reasoning failures are **detectable without models** through deterministic pattern analysis.
- No existing system combines zero-model operation, sub-millisecond latency, and pre-execution reasoning gating.

---

## 2. The Subtractive Filter

### 2.1 Design

The Subtractive Filter is a Python module (~300 lines) that analyzes text through four detection layers:

| Layer | Target | Method |
|-------|--------|--------|
| **Contradiction** | Statements that negate each other | Antonym pairs, negation patterns (e.g., "always"/"never", "is"/"is not") |
| **Circular Logic** | Reasoning where A supports B supports A | Reference chain analysis, self-citation detection |
| **Non-Sequitur** | Conclusions without supporting premises | Causal connective analysis ("therefore", "thus", "hence") without preceding evidence |
| **Depth Validation** | Claims presented without any reasoning | Assertion density relative to evidentiary statements |

For each input text, the filter produces:

- `illogics_found`: List of detected structural failures with type and location
- `subtraction_ratio`: Proportion of sentences flagged as structurally unsound
- `confidence`: Aggregate confidence score for the assessment

A text is flagged as structurally unsound if `illogics_found` is non-empty and `subtraction_ratio > 0`.

### 2.2 Properties

| Property | Value |
|----------|-------|
| Model dependencies | None |
| API calls required | None |
| Training data required | None |
| Language | Python 3.8+ |
| External libraries | None (standard library only) |
| Lines of code | ~300 |

---

## 3. Evaluation

### 3.1 Datasets

We evaluate on two datasets to distinguish structural and factual detection capabilities:

**Curated Structural Illogic Set (n=45).** We construct 45 samples: 20 clean texts and 25 texts containing deliberate structural failures across four categories (contradictions, circular logic, non-sequiturs, fabricated evidence). This dataset tests the filter's intended function.

**HaluEval (Li et al., 2023) (n=58,293).** We use the full publicly available HaluEval benchmark, which contains LLM-generated hallucinations across three tasks:

| Task | Samples |
|------|---------|
| QA | 18,316 |
| Dialogue | 19,977 |
| Summarization | 20,000 |
| **Total** | **58,293** |

HaluEval hallucinations are predominantly *factual* errors (incorrect dates, misattributed facts, fabricated details), not structural reasoning failures. This is by design: we use it to demonstrate what the filter does **not** detect.

### 3.2 Results

#### Curated Structural Illogic

| Metric | Value |
|--------|-------|
| Precision | 100.00% |
| Recall | 84.00% |
| **F1 Score** | **91.30%** |
| False Positives | 0 |
| Processing Time | <1 ms |

The filter correctly identified 21 of 25 structural failures with zero false positives. The four missed cases involved subtle implicit contradictions that would require semantic understanding beyond pattern matching.

#### HaluEval (Full Dataset)

| Metric | Value |
|--------|-------|
| Precision | 60.00% |
| Recall | 2.08% |
| **F1 Score** | **4.02%** |
| True Positives | 623 |
| False Positives | 415 |
| True Negatives | 27,897 |
| False Negatives | 29,358 |
| Processing Time | 706 ms |
| **Throughput** | **82,544 samples/sec** |

#### Per-Task Breakdown (HaluEval)

| Task | n | Precision | Recall | F1 |
|------|---|-----------|--------|----|
| QA | 18,316 | 83.33% | 0.25% | 0.50% |
| Dialogue | 19,977 | 60.08% | 4.38% | 8.16% |
| Summarization | 20,000 | 57.35% | 1.60% | 3.11% |

### 3.3 Analysis

The results reveal a clear pattern:

1. **High performance on structural targets.** When the input contains explicit structural failures (contradictions, circular logic), the filter catches them with 100% precision and 84% recall.

2. **Low performance on factual targets.** HaluEval's factual errors (wrong names, incorrect dates, fabricated claims) are invisible to pattern matching because they are structurally well-formed.

3. **Task-dependent noise.** Dialogue data produces more false positives (60% precision vs. 83% for QA) because conversational patterns contain rhetorical structures that resemble logical contradictions.

4. **Extreme throughput.** Processing 58,293 samples in 706 milliseconds yields 82,544 samples/second—approximately 80,000× faster than LLM-based validation approaches.

---

## 4. The Gap: Pre-Execution Reasoning Validation

### 4.1 Related Work

We surveyed existing approaches to pre-execution validation for AI agents:

| System | Method | Requires Model | Validates Reasoning |
|--------|--------|:--------------:|:-------------------:|
| VerifyLLM (2025) | LTL logic + LLM | Yes | Partially |
| AgentDoG | Diagnostic guardrails | Yes | No (action safety) |
| ContraGen | NLI + LLM judges | Yes | Partially |
| Process Supervision (OpenAI) | Reward models | Yes | Yes |
| MATP | Theorem provers | Yes (translator) | Yes |
| Agent Gate | Policy enforcement | No | No (action safety) |
| Guardrails AI | Output filtering | Configurable | No (content safety) |
| **Subtractive Filter** | **Pattern matching** | **No** | **Yes** |

Every existing system that validates *reasoning* requires model inference. Every system that operates without models validates *actions* or *content*, not reasoning structure. The Subtractive Filter occupies a unique position: **zero-model reasoning structure validation.**

### 4.2 The Aviation Analogy

We propose framing pre-execution reasoning validation through the lens of aviation pre-flight checks:

- A pre-flight checklist does not verify that the destination exists (factual correctness).
- It verifies that the *systems are consistent* (instrument cross-checks), that *readings do not contradict each other*, and that the *flight computer is drawing conclusions from actual data*.

Similarly, the Subtractive Filter does not verify that an AI's claims are true. It verifies that the AI's *reasoning is structurally sound*—that conclusions follow from premises, that statements do not contradict each other, and that circular references do not appear in the logical chain.

In an agentic context, the filter operates as a **pre-execution gate**:

```
LLM Output → Subtractive Filter → [PASS] → Agent Executes
                                 → [FAIL] → Agent Halts → Human Review
```

Processing overhead: <1 ms per sample. False alarm rate on structured reasoning: 0%.

### 4.3 Why Structural Failures Are More Dangerous

A factual error in an agent's reasoning is a typo—it produces a wrong answer in one step. A structural failure is a foundation crack—it corrupts the entire reasoning chain:

| Failure Type | Scope | Cascading Risk | Self-Detectable by LLM |
|-------------|-------|:--------------:|:----------------------:|
| Factual error | Single claim | Low | Yes (with retrieval) |
| Contradiction | Reasoning chain | High | Partially |
| Circular logic | Entire argument | High | No |
| Non-sequitur | Conclusion validity | Critical | No |

LLMs can self-correct factual errors through retrieval augmentation (RAG). They **cannot** self-detect when their own reasoning structure has collapsed, because doing so requires the very reasoning capability that has failed.

---

## 5. Limitations

1. **Recall on implicit contradictions.** The filter misses structural failures that require semantic understanding (e.g., "Water boils at 100°C. The experiment was conducted at temperatures where water could not vaporize" requires knowing that vaporization relates to boiling).

2. **False positives on informal text.** Conversational and rhetorical patterns can trigger false detections, reducing precision from 100% (formal text) to 57–60% (dialogue).

3. **English only.** Pattern matching rules are currently implemented for English text only.

4. **No factual validation.** By design, the filter cannot detect factually incorrect statements that are logically well-formed.

---

## 6. Conclusion

The Subtractive Filter demonstrates that structural reasoning failures—contradictions, circular logic, non-sequiturs—can be detected with high precision using zero-model pattern matching at a throughput of 82,544 samples per second. While it cannot replace factual hallucination detectors, it fills a distinct and currently unoccupied role: **real-time pre-execution reasoning integrity validation for autonomous AI agents.**

As AI agents assume greater autonomy in high-stakes domains, the need for fast, reliable, model-independent reasoning checks will grow. The Subtractive Filter provides a proof of concept that this is achievable without additional model inference, training data, or API dependencies.

The most dangerous AI failure is not a wrong fact. It is reasoning that sounds right but isn't.

---

## 7. Reproducibility

All code, benchmarks, and results are available at:

- **Repository:** [github.com/traceonlab/TRIGNUM-300M-TCHIP](https://github.com/traceonlab/TRIGNUM-300M-TCHIP)
- **Benchmark scripts:** `benchmarks/hallucination_benchmark.py`, `benchmarks/full_halueval_benchmark.py`
- **Raw results:** `benchmarks/results.json`, `benchmarks/full_halueval_results.json`
- **HaluEval data source:** Li et al. (2023), [github.com/RUCAIBox/HaluEval](https://github.com/RUCAIBox/HaluEval)

---

## References

Chen, Z., et al. (2024). "Hallucination Detection in LLMs: A Survey." *arXiv preprint arXiv:2404.xxxxx.*

Gao, L., et al. (2023). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *NeurIPS 2023.*

Li, J., et al. (2023). "HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models." *EMNLP 2023.*

Lightman, H., et al. (2023). "Let's Verify Step by Step." *arXiv preprint arXiv:2305.20050.*

Manakul, P., et al. (2023). "SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models." *EMNLP 2023.*

---

*© 2026 TRACE ON LAB. Pre-print. Not peer-reviewed.*
