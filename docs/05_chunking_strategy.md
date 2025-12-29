# Regulation-Aware Chunking Strategy

## 1. Purpose and Context

This document describes the chunking strategy adopted in this project and explains **why** it is required, **how** it is designed, and **why this specific approach is suitable for regulatory and compliance-oriented RAG systems**.

Chunking is a foundational design decision in Retrieval-Augmented Generation (RAG). In regulated financial environments, poor chunking directly leads to incorrect retrieval, loss of legal meaning, and non-explainable AI outputs. The strategy defined here prioritises semantic integrity, explainability, and auditability over raw technical convenience.

---

## 2. What Is Chunking?

Chunking is the process of splitting long source documents into **smaller, self-contained text units** ("chunks") that serve as the atomic units for:
- embedding,
- retrieval,
- and downstream reasoning by AI agents.

In a RAG pipeline, **models never retrieve entire documents**. They retrieve chunks. Therefore, the quality, boundaries, and meaning of chunks directly determine the quality of system outputs.

---

## 3. Why Chunking Is Necessary

Chunking is required for three complementary reasons:

### 3.1 Technical Constraints
- Large language models have finite context windows
- Embedding very long texts reduces semantic precision
- Smaller units improve similarity search performance

### 3.2 Semantic Integrity
- Regulatory documents contain multiple obligations, definitions, and exceptions
- Retrieving an entire document introduces noise
- Retrieving partial obligations risks misinterpretation

### 3.3 Governance and Explainability
- Compliance decisions must be traceable to precise sources
- AI-assisted analysis must be auditable
- Each retrieved unit must be independently interpretable

Without chunking, a RAG system cannot be considered reliable or defensible in a compliance context.

---

## 4. Overview of Chunking Approaches

Several chunking approaches exist. Their suitability varies significantly depending on domain.

### 4.1 Fixed-Size (Token or Character-Based) Chunking
- Splits text every N tokens or characters
- Advantages: simple to implement
- Limitations:
  - Breaks legal meaning
  - Arbitrary boundaries
  - Not explainable

**Unsuitable for regulatory use cases**.

---

### 4.2 Page-Based Chunking
- One chunk per document page
- Limitations:
  - Pages have no legal meaning
  - Obligations often span pages

**Not appropriate for compliance analysis**.

---

### 4.3 Paragraph-Based Chunking
- Splits text by paragraphs
- Advantages:
  - Preserves local coherence
- Limitations:
  - Paragraphs may lack full legal context
  - Legal obligations often span multiple paragraphs

**Partially useful, but insufficient alone**.

---

### 4.4 Semantic Chunking
- Uses topic-change detection or ML-based segmentation
- Advantages:
  - Topic-aware splitting
- Limitations:
  - Difficult to validate
  - Hard to audit
  - Non-deterministic boundaries

**Risky in regulated environments**.

---

### 4.5 Structure-Based Chunking (Recommended)

- Splits text according to document structure
- Uses legally meaningful units such as:
  - Articles
  - Sections
  - Clauses

**This approach preserves meaning, supports explainability, and aligns with regulatory reasoning.**

---

## 5. Regulation-Aware Chunking

### 5.1 Definition

Regulation-aware chunking means:

> Chunk boundaries align with **legally meaningful and citable units**, not arbitrary text lengths.

In regulatory documents, legal meaning is encoded in structure. Ignoring that structure leads to incorrect interpretation.

---

### 5.2 Legal Structure Considerations

Typical regulatory documents follow a hierarchy such as:

- Title
- Chapter
- Section
- **Article**
- Paragraphs and sub-points

Among these, **Articles represent the smallest legally binding and independently interpretable units**.

---

## 6. Adopted Chunking Strategy

### 6.1 Primary Chunk Unit

The primary chunking unit in this project is the **Article**.

Each chunk:
- Contains exactly one Article
- Includes all paragraphs and sub-points of that Article
- Does not span multiple Articles

---

### 6.2 Rationale

Article-level chunking:
- Preserves full legal meaning
- Matches how regulators cite obligations
- Enables precise retrieval
- Supports explainability and auditability

This represents the best trade-off between granularity and semantic completeness.

---

## 7. Chunk Metadata Design

Each chunk is enriched with structured metadata to support retrieval, reasoning, and traceability.

### 7.1 Required Metadata Fields

- `document_id`
- `document_title`
- `authority` (e.g. CSSF, EBA, EU)
- `jurisdiction` (e.g. Luxembourg, EU)
- `binding_level` (Regulation, Directive, Circular, Guideline)
- `article_number`
- `article_title` (if available)
- `text`

Metadata enables downstream agents to reason not only over text, but also over regulatory context.

---

## 8. Storage Format

Chunks are stored as structured JSON files.

Reasons:
- Explicit structure
- Easy validation
- Agent-friendly
- Audit-ready

Each JSON object corresponds to exactly one Article-level chunk.

---

## 9. Validation Rules

Before chunks are used for embedding or retrieval, the following conditions must be satisfied:

- Each chunk corresponds to exactly one Article
- Article numbering matches the source document
- No chunk mixes multiple obligations
- A human reader can understand the chunk in isolation

Chunks failing these checks must be corrected before downstream use.

---

## 10. Limitations and Future Extensions

Some Articles may be very long and exceed ideal context lengths. In such cases, **controlled sub-chunking** may be introduced in later iterations, while preserving the Article as the top-level reference.

Any refinement must maintain legal traceability and explainability.

---

## 11. Summary

This chunking strategy is designed to meet the requirements of regulated financial environments by prioritising:
- semantic integrity,
- explainability,
- and auditability.

Structure-based, regulation-aware chunking at the Article level provides a robust foundation for compliant RAG and multi-agent workflows.