# AI Coding Agent Instructions for Finance Compliance RAG

## Project Overview
This is a Retrieval-Augmented Generation (RAG) system for financial regulatory compliance analysis. The system processes regulatory documents (CSSF, DORA, EBA, GDPR) through extraction, regulation-aware chunking, embedding, and multi-agent retrieval workflows. **Critical focus**: explainability, traceability, and human oversight over performance.

## Architecture & Data Flow
- **Data Pipeline**: `data/raw/` PDFs → `data/processed/extracted_text/` → `data/processed/chunks/` JSON → embeddings → retrieval
- **Core Components**: 
  - `src/chunking/`: Regulation-specific parsers (CSSF sections, DORA articles)
  - `retrieval/`: Embedding storage and search
  - `agents/`: Query routing, reasoning, compliance analysis
  - `app/`: API and CLI interfaces
- **Chunking Strategy**: Structure-based at legally meaningful units (articles/sections) to preserve regulatory integrity. See `docs/05_chunking_strategy.md`

## Key Patterns & Conventions
- **Parser Pattern**: Each regulation has custom parser inheriting `BaseParser` (e.g., `CSSFParser` uses `SECTION_PATTERN = re.compile(r"(\d+\.\d+\.\d+)\.\s+(.*)")`)
- **Chunk Metadata**: Include `document_id`, `authority`, `jurisdiction`, `binding_level`, `article_number`, `text` for traceability
- **Validation First**: Always run validation after chunking (`validate_chunks.run_validation()`)
- **File Naming**: `{regulation}_{identifier}_{unit}.json` (e.g., `cssf_circular_20_750_sections.json`)
- **Error Handling**: Use assertions for critical failures (e.g., `assert len(chunks) > 0, "❌ No chunks created!"`)

## Developer Workflows
- **Setup**: `python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt`
- **Chunking**: Run `scripts/run_chunking.py` for specific documents; uses `pdfplumber` for text extraction
- **Testing**: Manual validation required; no automated tests yet (prototype phase)
- **Dependencies**: Minimal - `pdfplumber` for PDF processing, regex for parsing

## Integration Points
- **External APIs**: None currently (prototype)
- **Data Sources**: Official regulatory PDFs only; manual ingestion for authenticity
- **Agent Communication**: Query router → retriever → reasoning agent → compliance agent
- **Storage**: JSON files for chunks; future embedding store in `retrieval/embed_store.py`

## Critical Constraints
- **Legal Integrity**: Never break regulatory meaning across chunks
- **Traceability**: Every output must link to source document/article
- **Human Oversight**: No automated decision-making; all analysis requires human review
- **Reproducibility**: Use virtual environment; document all manual steps

## Common Pitfalls
- Don't use generic chunking (fixed-size/page-based) - breaks legal context
- Always validate chunks before embedding
- Preserve document structure in extracted text
- Match parser patterns to actual document formatting

## Key Reference Files
- `docs/05_chunking_strategy.md`: Why regulation-aware chunking matters
- `src/chunking/dora_chunker.py`: Article-level parsing example
- `scripts/chunking/section_parser.py`: Section detection logic
- `data/processed/chunks/cssf_circular_20_750_sections.json`: Output format example