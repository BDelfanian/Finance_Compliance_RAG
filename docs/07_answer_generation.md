# STEP 5 — Citation-Bound Answer Generation

## Purpose

STEP 5 extends the RAG pipeline to generate **compliance-aware, citation-bound answers** using the retrieval output from STEP 4.
It provides:

* Multi-regulator coverage (CSSF, DORA, EBA)
* Inline source citations for auditability
* Confidence scoring
* Multi-turn conversational context in a session
* Cached responses for faster repeated queries

---

## Components

### 1. `citation_bound_answer_generation.py`

Handles retrieval + LLM call:

* **Functions:**

  * `generate_citation_bound_answer(query_text: str, top_k: int = 5)`

    * Retrieves top K chunks per regulator
    * Constructs a **strict citation-bound prompt**
    * Calls GPT-5 mini (OpenAI API)
    * Returns a structured response:

      ```json
      {
        "query": "...",
        "answer": "...",
        "answer_confidence": 0.57,
        "retrieved_chunks": [...],
        "retrieval_filters": {...},
        "timestamp": "..."
      }
      ```
  * `generate_citation_bound_answer_cached(query_text: str, top_k: int = 5)`

    * Same as above, but caches results to speed up repeated queries

* **LLM Call (`llm_call`)**

  * Uses `gpt-5-mini` model
  * `temperature=1.0` (required)
  * Strict citation-bound system prompt

---

### 2. Streamlit UI — Multi-Turn Conversational Context

File: `step5_multiturn_ui.py`

**Features:**

* **Text area input** for regulatory query or follow-up
* **Slider** to select number of top chunks per regulator
* **Submit button** triggers generation
* **Session-based conversation memory**

  * Stores all previous queries and answers in `st.session_state.conversation`
* **Answer display**

  * Question/Answer with confidence and timestamp
  * Reverse chronological order (latest query first)
* **Supports follow-up queries** without losing context

**Usage:**

```bash
streamlit run src/step5_multiturn_ui.py
```

---

### 3. Example Query

```text
Explain reporting obligations for EU financial entities under CSSF, DORA, and EBA.
```

**Example Response (formatted for audit):**

* **Duty to report major ICT-related incidents:**
  Financial entities must report major ICT-related incidents to the relevant competent authority; where a firm has more than one supervisor, Member States must designate a single competent authority; significant credit institutions report to the designated national competent authority, which forwards the report to the ECB.
  **Ref:** [DORA Article 19 / Article 19 / 1]

* **Use of templates and alternative means:**
  Financial entities must produce initial and subsequent notifications using Article 20 templates; if technically impossible, alternative means may be used.
  **Ref:** [DORA Article 19 / Article 19 / 1]

* **Content requirement:**
  The reports must include all necessary information for the competent authority to assess significance and cross-border impact.
  **Ref:** [DORA Article 19 / Article 19 / 1]

---

### 4. Key Notes

* **Cached answers** prevent repeated API calls for identical queries.
* **Multi-turn support** allows follow-ups without losing session context.
* **Confidence score** (0–1) helps assess answer reliability.
* **Audit-friendly output** with inline source citations.

---

### 5. Optional Enhancements

* Highlight headings in answers (e.g., “Duty to report…”)
* Copy-to-clipboard button for answers
* Persistent history using local JSON storage
* Preprocessing to split long answers into readable bullet points

---

### 6. Dependencies

* `streamlit>=1.25`
* `openai>=1.0.0`
* STEP 4 packages for retrieval and embeddings
* Standard Python libraries: `os`, `json`, `datetime`

---

### 7. Running the UI

1. Activate your Python environment:

```bash
conda activate .venv
```

2. Run the Streamlit multi-turn UI:

```bash
streamlit run src/step5_multiturn_ui.py
```

3. Enter a regulatory query or follow-up in the text area.
4. Adjust `top_k` to control the number of chunks retrieved per regulator.
5. Review the answer, confidence, and timestamp in the session panel.

---

### 8. References

* **DORA Articles 19–20**: Incident reporting obligations
* **CSSF & EBA**: National / regulatory source retrieval