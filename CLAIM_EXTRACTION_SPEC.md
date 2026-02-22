# TRIGNUM — Claim Extraction Layer

## Level-2 Implementation Specification

**Target:** Gemini / Copilot / External Engineers  
**Role:** Insert structural reasoning representation before `SubtractiveFilter`  
**Priority:** Critical — unlocks meaningful structural evaluation  
**Prerequisite:** Read `ENGINEERING_HANDOFF.md` first

---

## 1. Objective

Transform raw natural language into a minimal logical shape that allows TRIGNUM to detect impossibilities **structurally** rather than **lexically**.

We are NOT building semantic understanding.

> **We are building reasoning geometry extraction.**

---

## 2. Design Constraints (Must Not Be Violated)

| Constraint                      | Reason                                         |
| ------------------------------- | ---------------------------------------------- |
| No ML training                  | Must remain deterministic + deployable offline |
| O(n) processing                 | Must stay faster than LLM inference            |
| No ontology                     | Avoid domain lock-in                           |
| No knowledge base               | TRIGNUM is structure-only                      |
| Language-agnostic extensibility | Required for multilingual future               |

---

## 3. Target Data Structure

All sentences must reduce into atomic claims:

```python
@dataclass
class Claim:
    subject:     str
    relation:    str
    object:      str
    polarity:    int   # +1 = asserted, -1 = negated
    modality:    str   # optional: "possible" | "certain" | "claimed"
    source_span: str   # original text fragment
```

### Example

**Input text:**

```
"Drug A does not cause liver damage."
```

**Output:**

```python
Claim(
    subject     = "Drug A",
    relation    = "causes",
    object      = "liver damage",
    polarity    = -1,
    modality    = "certain",
    source_span = "Drug A does not cause liver damage."
)
```

---

## 4. Extraction Rules (Deterministic)

### 4.1 Sentence Segmentation

Split on:

- `.` (period)
- `;` (semicolon)
- Causal connectors: `because`, `therefore`, `thus`, `hence`, `so`

Each segment is processed independently.

---

### 4.2 Relation Detection — Verb Normalization

Map verb phrases to canonical relations using rule-based lemmatization only:

| Surface Form                    | Canonical Relation |
| ------------------------------- | ------------------ |
| causes / leads to / results in  | `causes`           |
| is / equals / means             | `equals`           |
| belongs to / is part of         | `member_of`        |
| depends on / requires           | `depends_on`       |
| proves / supports / justifies   | `justifies`        |
| contradicts / opposes / negates | `negates`          |
| increases / raises              | `increases`        |
| decreases / reduces             | `decreases`        |

**Rule:** If no canonical match found → use raw verb lemma. Never discard.

---

### 4.3 Negation Detection

If sentence contains any of:

```
not, never, no, cannot, does not, will not, is not, are not
```

Set `polarity = -1`.  
Default `polarity = +1`.

---

### 4.4 Entity Extraction (Shallow — No Coreference)

Extract noun chunks only:

```
[Subject NP]  [Verb Phrase]  [Object NP]
```

**Primary:** Use spaCy dependency parsing (`en_core_web_sm`)  
**Fallback:** Regex noun-phrase capture if spaCy not installed  
**Hard rule:** Do NOT resolve coreference. Take surface forms as-is.

---

## 5. Structural Illogic Detection — Rewritten Core

Once claims are extracted, `SubtractiveFilter` operates on `Claim` sets, not raw text.

### 5.1 Contradiction Rule

```
IF: (A, R, B, polarity=+1)  AND  (A, R, B, polarity=-1)
THEN: → contradiction
```

Same subject, same relation, same object, opposite polarity.

---

### 5.2 Circular Justification Rule

```
IF: A justifies B
AND: B justifies A
THEN: → circular_reference
```

Detect cycles of length 2+ in the justification chain.

---

### 5.3 Infinite Regress Rule

Detect dependency chains longer than a configurable threshold (default: 5) without a grounded premise (a claim not depending on any other claim in the set).

---

### 5.4 Non-Sequitur Rule

If a conclusion appears (identified by: `therefore`, `thus`, `hence`) but shares **no entities** with any premise in the same segment:

```
Premise:    climate affects crops
Conclusion: therefore vaccines fail    ← no shared entities

Graph disconnect → non_sequitur
```

---

## 6. Updated Filter Pipeline

Replace the current `_detect_text_illogics(text)` method with:

```python
def apply(self, text: str) -> FilterResult:
    claims  = extract_claims(text)          # new layer
    graph   = build_relation_graph(claims)  # new layer
    illogics = evaluate_graph(graph)        # replaces lexical heuristics
    ...
```

### Backward Compatibility

If spaCy is not installed:

- Fall back silently to existing lexical heuristic detection
- Log: `[TRIGNUM] spaCy not found — running in lexical mode`
- Zero breaking changes to existing API

---

## 7. New Evaluation Metrics

We no longer score:

> _"Did we detect hallucination?"_

We score:

> _"Did we detect structural invalidity?"_

| Metric                     | Meaning                        | Current    | Target    |
| -------------------------- | ------------------------------ | ---------- | --------- |
| Structural Conflict Recall | % real logic faults caught     | 84.0%      | **> 95%** |
| False Alarm Rate           | Clean text wrongly flagged     | 0.0%       | **< 2%**  |
| Graph Coherence Score      | % reasoning structure retained | —          | TBD       |
| LLM Error Reduction        | Downstream hallucination delta | unmeasured | **> 15%** |

---

## 8. Performance Budget

```
Claim extraction + graph validation:  < 5ms per sample (CPU-only)
If slower → redesign before merging.
```

The current lexical filter processes at **52,581 samples/second (~0.019ms/sample)**.  
The new layer must not regress below **10,000 samples/second**.

---

## 9. Delivery Milestones

| Milestone | Deliverable                                                                                |
| --------- | ------------------------------------------------------------------------------------------ |
| **A**     | `claim_extractor.py` — prototype working on 100 sentences                                  |
| **B**     | `structural_conflict_engine.py` — `SubtractiveFilter` rewritten to operate on `ClaimGraph` |
| **C**     | `benchmarks/claim_extraction_benchmark.py` — benchmark re-run vs original numbers          |
| **D**     | Integration test: TRIGNUM as front-layer to a small LLM (Mistral-7B or Phi-3-mini)         |

---

## 10. Files To Create / Modify

```
src/trignum_core/
├── claim_extractor.py           ← NEW  (Claim dataclass + extraction logic)
├── structural_conflict_engine.py ← NEW  (graph-based illogic detection)
├── subtractive_filter.py        ← MODIFY  (wire in new engine, keep fallback)
└── __init__.py                  ← MODIFY  (export new classes)

benchmarks/
└── claim_extraction_benchmark.py ← NEW  (delta analysis vs current)

tests/
└── test_claim_extractor.py      ← NEW  (unit tests for Claim extraction)
```

---

## 11. Definition of Success

> _"TRIGNUM succeeds if it becomes a structural validation layer that improves LLM reasoning reliability without adding model weight."_

**If it becomes slower, smarter, or knowledge-heavy — we failed the design.**

| ✔ Success                              | ✘ Failure                 |
| -------------------------------------- | ------------------------- |
| Faster than LLM generation             | Requires API calls        |
| Runs offline, zero dependencies (core) | Requires training data    |
| Works cross-domain without tuning      | Domain-specific rules     |
| Reduces LLM structural errors          | Adds latency > 5ms/sample |

---

_TRACE ON LAB © 2026 | Sovereign Architecture | TRIGNUM-300M T-CHIP_
