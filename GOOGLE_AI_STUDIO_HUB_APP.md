# 🌌 TRIGNUM T-CHIP Master Hub: Application Specification

**Goal:** Build a single, unified web application (via Google AI Studio & Streamlit) that aggregates the entire TRIGNUM-300M repository into an interactive, multi-tab "Course & Pitch Hub."

This application will allow the user (and potential investors/partners) to interact with the Engine, view 3D magnetic simulations, take an educational guided tour of the codebase, and instantly access outreach strategies.

---

## 1. App Architecture (Streamlit Multipage)

The app will be structured with a persistent left-hand sidebar for navigation and a main content area.

### 🧭 Sidebar Navigation

- **HOME:** The Pitch & Executive Summary
- **MODULE 1: The Engine (Live Demos)**
- **MODULE 2: The Data (Metrics & Dashboards)**
- **MODULE 3: The Theory (3D Magnetics & Simulations)**
- **MODULE 4: The Code (Repository Tour)**
- **MODULE 5: The Handoff (Pitch Deck & Partners)**

---

## 2. Module Specifications

### 🏠 HOME: The Trignum Pitch

- **Hero Section:** "TRIGNUM-300M: The Pre-Flight Check for Autonomous AI."
- **Interactive Metric:** A massive, animated counter showing the `82,544 samples/sec` throughput.
- **The Hook:** A 3-sentence tl;dr of Subtractive Epistemology.

### ⚙️ MODULE 1: The Engine (Live Demos)

_Consolidating all `src/examples` into web interfaces._

- **The Paradox Tester:** A text area where the user can paste LLM output. Clicking `[Run Subtractive Filter]` triggers the live `SubtractiveFilter` Python class.
- **T-CHIP State Visualizer:** An interactive LED (Blue/Red/Gold) that changes state based on the logic validation of the text input.

### 📊 MODULE 2: The Data (Metrics & Dashboards)

_Integrating the pre-flight JSON benchmarks._

- **HaluEval Confusion Matrix:** A Plotly visualization of the 58k sample benchmark, highlighting exactly where the filter scored 100% precision.
- **F1 Explanation Alert:** A visual callout explaining the "Recall Gap" (why structural filters don't catch factual falsehoods, and why that's a feature, not a bug).

### 📐 MODULE 3: The Theory (3D Simulations)

_Embedding `trignum_tetrahedron.py` and `demo/index.html`._

- **Streamlit + Three.js:** An embedded iframe running the 3D WebGL rotating tetrahedron.
- **Interactive Controls:** Sliders to adjust the "Magnetic Force" of the Alpha, Beta, and Gamma planes to visualize how illogic is pulled to the Beta face.

### 📁 MODULE 4: The Code (Course Walkthrough)

_Breaking down the architecture for education._

- An interactive file-tree component. Clicking a file (e.g., `pyramid.py`) displays heavily annotated, educational commentary explaining what it does.
- Code blocks highlighting the `UNIVERSAL_ILLOGICS` set.

### 🎯 MODULE 5: Target Partners & Pitch Handoff

_The outreach arm of the application. Contains the exact names, roles, and emails._

#### A. Target Acquisition Profile (Who needs to buy/collaborate with TRIGNUM)

1. **Physical AI / Robotics (NVIDIA):** Sentient robots cannot afford logical conflicts in motor-control prompts. (Target: NeMo Guardrails Team, Project GROOT).
2. **Sovereign AI Nations (UAE, France, Saudi Arabia):** Nations building local LLMs that need a guaranteed security governor that doesn't rely on OpenAI APIs.
3. **Medical Diagnostics Platforms:** Healthcare AI cannot provide concluding treatments that contradict the stated symptoms in the same prompt.
4. **Autonomous Agent Startups (AutoGPT, LangChain):** Agentic workflows that loop infinitely or crash due to downstream hallucination errors.

#### B. The Outreach Assets

- **Downloadable Pitch Deck:** (Placeholder button to download a PDF presentation).
- **The Technical Position Paper:** Embedded HTML viewer for the `TRIGNUM_300M_Position_Paper.html`.
- **Pre-Written Email Templates:** Exact copy-paste templates (like the UNDP draft) for different partner tiers.

---

## 3. Required Tech Stack for Execution

- **Interface:** `streamlit` (Fastest way to build python data-apps)
- **Visuals:** `plotly` (For the benchmark charts) and `streamlit.components.v1` (For the 3D iframe)
- **Engine execution:** Standard Python, importing `src.trignum_core` directly into the Streamlit session state.

---

> **Gemini 3.1 Instruction:** When executing this plan, create a `hub_app.py` in the root directory. Use Streamlit tabs (`st.tabs()`) or a sidebar radio button (`st.sidebar.radio()`) to seamlessly link these 5 modules together without requiring multiple file executions.
