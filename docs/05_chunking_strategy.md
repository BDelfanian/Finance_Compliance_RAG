# Regulation-Aware Chunking Strategy

## 1. Purpose and Context

This document describes the chunking strategy adopted in this project and explains **why** it is required, **how** it is designed, and **why this specific approach is suitable for regulatory and compliance-oriented RAG systems**.

Chunking is a foundational design decision in Retrieval-Augmented Generation (RAG).
In regulated financial environments, poor chunking directly leads to:

* incorrect retrieval,
* loss of legal meaning,
* and non-explainable or non-defensible AI outputs.

The strategy defined here prioritises **semantic integrity, explainability, and auditability** over raw technical convenience.

---

## 2. What Is Chunking?

Chunking is the process of splitting long source documents into **smaller, self-contained text units** (“chunks”) that serve as the atomic units for:

* embedding,
* retrieval,
* and downstream reasoning by AI agents.

In a RAG pipeline, **models never retrieve entire documents** — they retrieve chunks.
Therefore, the quality, boundaries, and legal meaning of chunks directly determine the quality and defensibility of system outputs.

---

## 3. Why Chunking Is Necessary

Chunking is required for three complementary reasons:

### 3.1 Technical Constraints

* Large language models have finite context windows
* Embedding very long texts reduces semantic precision
* Smaller units improve similarity search and ranking quality

### 3.2 Semantic Integrity

* Regulatory documents contain layered obligations, definitions, exceptions, and scope clauses
* Retrieving entire documents introduces noise
* Retrieving incomplete obligations risks legal misinterpretation

### 3.3 Governance and Explainability

* Compliance decisions must be traceable to precise legal sources
* AI-assisted analysis must be auditable
* Each retrieved unit must be independently interpretable by a human reviewer

Without structured chunking, a RAG system **cannot be considered reliable or defensible** in a compliance context.

---

## 4. Overview of Chunking Approaches

Several chunking approaches exist. Their suitability varies significantly depending on domain.

### 4.1 Fixed-Size (Token or Character-Based) Chunking

* Splits text every N tokens or characters
* Advantages: simple to implement
* Limitations:

  * Arbitrary boundaries
  * Breaks legal meaning
  * Not explainable

**Unsuitable for regulatory use cases.**

---

### 4.2 Page-Based Chunking

* One chunk per document page
* Limitations:

  * Pages have no legal meaning
  * Obligations often span pages

**Not appropriate for compliance analysis.**

---

### 4.3 Paragraph-Based Chunking

* Splits text by paragraphs
* Advantages:

  * Preserves local coherence
* Limitations:

  * Paragraphs may lack full legal context
  * Legal obligations often span multiple paragraphs

**Useful only when paragraphs are legally addressable (e.g. EBA Guidelines).**

---

### 4.4 Semantic / ML-Based Chunking

* Uses topic-change detection or ML-based segmentation
* Advantages:

  * Topic-aware splitting
* Limitations:

  * Non-deterministic
  * Hard to validate
  * Difficult to audit

**Risky in regulated environments.**

---

### 4.5 Structure-Based Chunking (Recommended)

* Splits text according to **explicit legal or supervisory structure**
* Uses legally meaningful units such as:

  * Articles
  * Sections
  * Paragraphs (where explicitly numbered)

This approach preserves legal meaning, supports explainability, and aligns with how regulators reason and cite obligations.

---

## 5. Regulation-Aware Chunking

### 5.1 Definition

Regulation-aware chunking means:

> Chunk boundaries align with **legally meaningful and citable units**, not arbitrary text lengths.

In regulatory texts, **legal meaning is encoded in structure**.
Ignoring that structure leads to incorrect interpretation and non-defensible AI outputs.

---

### 5.2 No Single “Universal” Chunk Unit

A key design insight of this project is:

> **Different regulatory authorities encode legal meaning at different structural levels.**

Therefore, regulation-aware chunking **cannot rely on a single universal unit**.

---

## 6. Adopted Chunking Strategy (Per Document Type)

### 6.1 CSSF Circulars (Luxembourg Supervisor)

**Primary chunk unit:** Supervisory Sections (e.g. `3.2.1`, `3.3.2`)

Rationale:

* CSSF Circulars express requirements at section level
* Sections group multiple numbered expectations into one supervisory obligation
* Section boundaries are stable and citable in supervisory practice

Each chunk:

* Contains exactly one section
* Includes all numbered points under that section
* Does not span multiple sections

---

### 6.2 EU Regulations (e.g. DORA – Regulation (EU) 2022/2554)

**Primary chunk unit:** Article

Rationale:

* EU Regulations are legally binding at Article level
* Articles are the smallest independently enforceable legal units
* Regulators and courts cite obligations by Article

Each chunk:

* Contains exactly one Article
* Includes all paragraphs and sub-points
* Does not span multiple Articles

---

### 6.3 EBA Guidelines

**Primary chunk unit:** Paragraph

Rationale:

* EBA Guidelines are addressed by **numbered paragraphs**
* Paragraphs are explicitly referenced in “comply or explain” assessments
* Paragraph numbering is local to logical sections and may restart

Important design note:

* Paragraph numbers are **not globally unique**
* Paragraph ordering is **not legally constrained**
* Each paragraph is treated as an atomic guidance unit

---

## 7. Chunk Metadata Design

Chunks are enriched with metadata to support retrieval, reasoning, and traceability.

### 7.1 Common Metadata Fields

All chunks include:

* `chunk_id`
* `document_id`
* `document_title`
* `authority` (CSSF, EBA, EU)
* `jurisdiction`
* `binding_level`
* `text`

### 7.2 Structure-Specific Metadata

Depending on document type, chunks may also include:

* `section_id` (CSSF)
* `article_number` (EU Regulations)
* `paragraph_number` (EBA Guidelines)
* `chapter` or `section_title` where relevant

This design allows **heterogeneous chunk structures** while remaining compatible with a unified RAG pipeline.

---

## 8. Storage Format

Chunks are stored as structured JSON files.

Reasons:

* Explicit schema
* Easy validation
* Agent-friendly
* Audit-ready
* Version-controllable

Each JSON object corresponds to **exactly one regulation-aware chunk**.

---

## 9. Validation Philosophy

Validation rules are **document-type aware** and intentionally conservative.

### 9.1 What Is Validated

* Structural boundary correctness (Article / Section / Paragraph)
* Noise and header removal
* Duplicate identifiers *within the same logical scope*
* Abnormally short chunks (extraction errors)

### 9.2 What Is Explicitly NOT Validated

* Global paragraph ordering (EBA)
* Global paragraph uniqueness (EBA)
* Cross-section numeric continuity

These constraints are **not enforced** because they do not reflect legal drafting reality.

---

## 10. Limitations and Future Extensions

Some Articles or Sections may exceed ideal context lengths.
Future iterations may introduce **controlled sub-chunking**, while preserving:

* the Article or Section as the top-level reference,
* legal traceability,
* and auditability.

Any refinement must maintain deterministic, explainable boundaries.

---

## 11. Summary

This chunking strategy is designed specifically for **regulated financial environments**.

Key principles:

* Structure over convenience
* Legal meaning over token efficiency
* Explainability over automation

By adapting chunking to **CSSF, EU Regulations, and EBA Guidelines**, this project establishes a robust, defensible foundation for compliant RAG and multi-agent workflows.
