# STEP 6 — Multi-Agent Orchestration (Compliance-Grade RAG)

## 1. Purpose and Scope

STEP 6 extends the existing **compliance-grade RAG pipeline** (STEP 4: Retrieval, STEP 5: Citation-Bound Generation) into a **multi-agent, governed decision-support system**.

The objective is to:
- Decompose complex regulatory queries into specialized agent responsibilities
- Improve reliability, interpretability, and auditability of answers
- Introduce governance, risk awareness, and modular scalability

This step explicitly targets **enterprise, financial, and regulatory use cases**, not generic chatbots.

---

## 2. Design Principles

The multi-agent architecture is governed by the following principles:

1. **Separation of Duties**  
   Each agent has a single, well-defined responsibility, mirroring financial governance models.

2. **Typed Outputs & Validation**  
   All agents return structured, schema-validated outputs (no free-form text blobs).

3. **Deterministic Orchestration**  
   Agent execution order and aggregation logic are explicit and testable.

4. **Citation-First Reasoning**  
   No agent may generate regulatory statements without traceable source citations.

5. **Auditability by Design**  
   Every run produces an evidence trail suitable for audit, compliance review, and MRM sign-off.

---

## 3. High-Level Architecture

```
User Query
    │
    ▼
Multi-Agent Orchestrator (STEP 6)
    ├── Retrieval Agent        → STEP 4
    ├── Citation Answer Agent  → STEP 5
    ├── Summarization Agent
    └── Risk Assessment Agent
    │
    ▼
Aggregated Output
    ├── Compliance Answer
    ├── Executive Summary
    ├── Risk & Gap Analysis
    ├── Confidence Score
    └── Audit Trail
    │
    ▼
Streamlit UI / API / Export Layer
```

The orchestrator itself is **not an LLM agent**. It is deterministic control logic.

---

## 4. Agent Definitions

### 4.1 Retrieval Agent

**Purpose**  
Retrieve relevant regulation-aware chunks from the vector store.

**Inputs**
- User query

**Outputs**
- Retrieved chunks
- Metadata (source, regulation, section)

**Dependencies**
- STEP 4: Embeddings & Retrieval

---

### 4.2 Citation Answer Agent

**Purpose**  
Generate a compliance answer strictly bound to retrieved citations.

**Inputs**
- User query
- Retrieved chunks

**Outputs**
- Answer text
- Citations (source_id, excerpt)
- Confidence score

**Dependencies**
- STEP 5: Citation-Bound Answer Generation

---

### 4.3 Summarization Agent

**Purpose**  
Produce concise summaries suitable for:
- Management
- Audit reports
- Executive briefings

**Constraints**
- No new regulatory interpretation
- Must rely exclusively on citation agent output

**Outputs**
- Summary text
- Confidence score

---

### 4.4 Risk Assessment Agent

**Purpose**  
Identify regulatory risk, ambiguity, or incomplete coverage.

**Responsibilities**
- Detect missing regulations
- Highlight ambiguous interpretations
- Flag low-confidence answers

**Outputs**
- Risk statements
- Warnings
- Risk-adjusted confidence score

---

## 5. Agent Output Contracts

All agents return structured outputs validated via schemas (e.g., Pydantic).

### Canonical Agent Response Schema

```python
class AgentResponse(BaseModel):
    agent_name: str
    answer: str
    citations: List[Citation]
    confidence: float
    warnings: Optional[List[str]]
```

This ensures:
- Inter-agent compatibility
- Validation before aggregation
- Stable downstream consumption (UI, API, export)

---

## 6. Orchestration Flow

1. Receive user query
2. Execute Retrieval Agent
3. Execute Citation Answer Agent
4. Execute Summarization and Risk Agents (parallel)
5. Validate all agent outputs
6. Aggregate results using confidence-weighted logic
7. Persist audit metadata
8. Return structured response

The orchestrator enforces **fail-fast behavior** if retrieval or citation steps fail.

---

## 7. Governance & MLChain Alignment

STEP 6 adopts MLChain-style lifecycle governance, even if MLChain is not explicitly used as a library.

### Tracked Artifacts

- Prompt versions
- Model versions
- Retrieved chunks
- Agent outputs
- Confidence scores
- Timestamps

### Governance Benefits

- Model Risk Management (MRM) readiness
- Regulatory reproducibility
- Post-hoc auditability
- Controlled prompt evolution

---

## 8. Confidence & Risk Handling

Confidence is treated as a **first-class signal**, not metadata.

### Example Rules

- Final confidence ≤ lowest agent confidence
- Presence of risk warnings reduces confidence
- Missing citations → confidence collapse

This prevents overconfident regulatory answers.

---

## 9. UI & API Exposure

The multi-agent outputs are exposed via:

- Streamlit UI (tabbed by agent)
- REST / internal API
- Exportable audit reports

Each agent’s output remains **visible and separable**, supporting review and challenge.

---

## 10. Testing & Validation Strategy

### Agent-Level Tests

- Schema validation
- Citation presence
- Confidence bounds

### Orchestrator-Level Tests

- Missing retrieval handling
- Conflicting agent outputs
- Low-confidence downgrade logic

Testing focuses on **regulatory safety**, not model accuracy alone.

---

## 11. Positioning Summary

With STEP 6 implemented, the system evolves from:

> "A RAG chatbot"

to:

> "A governed, multi-agent regulatory decision-support platform"

This step is the foundation for future extensions such as automated regulatory coverage tracking, jurisdiction-specific agents, and continuous compliance monitoring.

---

**Status**: Draft — Approved for implementation

