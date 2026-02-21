# 🧲 Available LLM Hallucination Benchmark Datasets

As part of the TRIGNUM-300M pre-flight checks, here is a comprehensive list of the top active public databases, leaderboards, and benchmarks for detecting LLM hallucinations, compiled from GitHub and HuggingFace.

## 1. General & Dialogue Hallucination Datasets

- **HaluEval (Currently Used)**: A large collection of generated and human-annotated hallucination samples for Q&A, dialogue, and summarization.
- **TruthfulQA**: A widely used benchmark to measure whether a language model is truthful in generating answers to questions. Contains questions that humans often answer falsely due to misconceptions.
- **Factool / FactScore**: Tools and datasets designed to evaluate the factual precision of long-form LLM generation.
- **SelfCheckGPT**: A zero-shot framework to detect hallucinations in LLMs by comparing multiple sampled responses.

## 2. Advanced / Enterprise Leaderboards

- **Vectara HHEM (Hughes Hallucination Evaluation Model)**: A prominent open-source model and leaderboard specifically built to score LLM summaries for factual consistency and hallucination rates. (Available on HuggingFace Space).
- **MIND (HELM Benchmark)**: A benchmark containing texts from various LLMs with human-annotated labels, embeddings, and hidden-layer activations.
- **RAGTruth**: A large-scale benchmark specifically targeting hallucinations in Retrieval-Augmented Generation (RAG) applications.

## 3. Domain-Specific Datasets

- **MedHallu**: A medical-specific benchmark with 10,000 high-quality Q&A pairs (based on PubMedQA) designed exclusively for detecting hallucinations in medical LLM outputs.
- **Placebo-Bench**: A specialized benchmark for hallucination detection within the pharmaceutical and clinical domain.
- **FELM-Science**: Focuses on factuality evaluation for language models in scientific reasoning and math.

## 4. Nuanced / Next-Gen Datasets

- **AuthenHallu**: The first hallucination detection benchmark built entirely from real, authentic LLM-human interactions rather than synthetically generated traps.
- **HalluVerse25**: A multilingual benchmark categorizing fine-grained types of hallucinations across English, Arabic, and Turkish.
- **SHROOM (SemEval-2024 Task-6)**: Shared-task on hallucinations and related observable overgeneration mistakes, often using reference-based evaluation.

---

### 📝 Next Steps for Pre-Flight Testing

To expand TRIGNUM's Level 1 Benchmark validation, we can select one of these datasets (e.g., **TruthfulQA**, **Vectara's HHEM Dataset**, or **MedHallu**) to build an automated integration pipeline just like we did for HaluEval.
