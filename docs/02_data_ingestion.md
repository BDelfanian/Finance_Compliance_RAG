# Data Ingestion

## Objective

The goal of the ingestion phase is to collect authoritative
regulatory documents and store them in a controlled and traceable
manner for downstream processing.

## Process

1. Documents are manually downloaded from official sources
2. Files are stored without renaming in `data/raw/`
3. No modification is applied to original files

## Rationale

Manual ingestion was selected to:
- Ensure authenticity of sources
- Avoid accidental inclusion of non-authoritative versions
- Maintain full control over document provenance
