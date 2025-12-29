# Text Extraction

## Objective

Convert regulatory PDF documents into clean, readable text
while preserving legal structure (headings, numbering, sections).

This step is a prerequisite for retrieval-based AI systems.

## Tooling

- Python 3
- pdfplumber

The PDFs used are text-based; OCR was not required.

## Method

- Each PDF is processed page by page
- Extracted text is concatenated in reading order
- Minimal cleaning is applied to remove empty lines
- No semantic transformation is performed

## Output

Extracted files are stored in `data/processed/` as UTF-8 text files,
with filenames matching the source documents.

## Validation

Manual validation was performed to ensure:
- Section numbering is preserved
- Headings are readable
- Text order is coherent

If extraction quality is insufficient, processing is stopped
and corrected before downstream use.
