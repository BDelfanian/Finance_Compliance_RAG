# STEP 4 — Embeddings, Retrieval & Validation

**Compliance-Safe RAG System**

---

## 4.1 Objective

The objective of STEP 4 is to establish a **controlled, auditable, and regulation-aware semantic retrieval layer** for previously validated regulatory chunks (STEP 3), covering CSSF, DORA, and EBA sources.

STEP 4 ensures:

* **Legal fidelity** — only approved regulatory text is retrievable
* **Governance enforcement** — symbolic hard filters prevent out-of-scope retrieval
* **Auditability** — each retrieval is traceable, timestamped, and reproducible
* **Compliance safety** — prevents hallucination and cross-regulatory contamination

> STEP 4 is strictly a retrieval layer. It does **not** interpret, summarize, or provide legal advice.

---

## 4.2 Inputs from STEP 3

### Assumptions

* All chunks are **validated, regulation-aware, and frozen**
* Stored as JSON with mandatory metadata fields

### Required Metadata Schema

```json
{
  "chunk_id": "CSSF_CIRC_22_806_ART_12_3",
  "source_regulation": "CSSF",
  "document_id": "CSSF_22_806",
  "article": "12(3)",
  "jurisdiction": "LU",
  "authority": "CSSF",
  "binding_level": "mandatory",
  "temporal_validity": {
    "effective_from": "2022-10-01",
    "effective_to": null
  },
  "chunk_type": "obligation",
  "text": "...",
  "validation_status": "approved"
}
```

Only chunks with `validation_status = approved` are eligible for embedding and retrieval.

---

## 4.3 Embedding Strategy

### 4.3.1 Embedded Data

* **Embed only**: `text`, `chunk_id`
* **Never embed**: metadata, interpretations, summaries, cross-chunk references

This ensures semantic vectors represent **pure regulatory language** only.

---

### 4.3.2 Segmented Vector Stores

| Vector Store | Contents |
|-------------|----------|
| `vs_cssf` | CSSF circulars & regulations |
| `vs_dora` | DORA Level 1 legal text |
| `vs_eba` | EBA Guidelines, RTS, ITS |

Segmentation prevents:

* Cross-authority contamination
* Normative hierarchy conflicts
* Ambiguous legal applicability

---

### 4.3.3 Embedding Model Requirements

* Version-locked and deterministic
* Stable dimensionality
* No training on user queries
* Compatible with EU data sovereignty expectations

---

## 4.4 Retrieval Architecture

### 4.4.1 Two-Phase Retrieval

#### Phase 1 — Hard Filtering (Symbolic)

Filters applied **before** semantic search:

* Authority
* Jurisdiction
* Temporal validity
* Binding level
* Validation status
* Document scope

Semantic similarity **cannot override** legal applicability.

---

#### Phase 2 — Semantic Retrieval (Vector Search)

* Performed only on filtered chunks
* k-NN search using cosine similarity (FAISS Inner Product on L2-normalized vectors)
* Conservative `k` (typically 5–10)
* Similarity threshold enforced

---

### 4.4.2 Retrieval Output Contract

```json
{
  "query_id": "Q_2025_001",
  "retrieved_chunks": [
    {
      "chunk_id": "...",
      "source_regulation": "CSSF",
      "article": "...",
      "similarity_score": 0.83
    }
  ],
  "filters_applied": {
    "authority": "CSSF",
    "jurisdiction": "LU",
    "binding_level": "mandatory"
  },
  "retrieval_timestamp": "2025-12-30T15:00:00Z"
}
```

All outputs are logged and replayable for audit purposes.

---

## 4.5 Compliance Controls

1. **No hallucination by design**
   * No matching chunk → no answer downstream
   * Mandatory citation in STEP 5

2. **Auditability & Explainability**
   * Query → chunk traceability
   * Model and index version traceability
   * Deterministic replay

3. **Separation of duties**
   * STEP 4: retrieval only
   * STEP 5: answer generation

---

## 4.6 Retrieval Validation Protocol

### 4.6.1 Validation Objectives

The validation suite ensures:

* Semantic relevance
* Regulatory isolation
* Deterministic behavior
* Threshold enforcement
* Schema integrity

---

### 4.6.2 Test Assets

```
src/
├─ run_embeddings_retrieval.py
└─ tests/
   ├─ test_retrieval_validation.py
   ├─ golden_queries.json
   └─ __init__.py
```

Golden queries define **expected retrieval behavior** and are SME-approved.

---

### 4.6.3 Test Execution

Run tests from project root:

```bash
pytest src/tests -v
```

All tests must pass before STEP 5 activation.

---

## 4.7 Out of Scope

* Legal interpretation
* Authority hierarchy resolution
* Legal advice generation

---

## 4.8 Transition Statement

> STEP 3 is frozen.
> STEP 4 establishes a compliance-safe, auditable retrieval layer.
> Passing validation is a mandatory gate to STEP 5.

---

## 4.9 Change Log

| Version | Date | Change | Approved By |
|-------|------|-------|-------------|
| 1.0 | 2025-12-30 | Initial STEP 4 definition | Compliance Lead |
| 1.1 | 2026-01-01 | Added retrieval validation & test harness | Model Risk |

---

## 4.10 Model Risk Management (MRM) Sign-Off

**Model Component:** STEP 4 — Embeddings & Retrieval

| Role | Name | Signature | Date |
|-----|------|-----------|------|
| Model Owner | | | |
| Compliance Officer | | | |
| Legal Counsel | | | |
| Model Risk Management | | | |

**Approval Statement**

> The STEP 4 retrieval layer has been reviewed and validated. It satisfies governance, auditability, and regulatory compliance requirements and is approved for controlled downstream use in STEP 5.

