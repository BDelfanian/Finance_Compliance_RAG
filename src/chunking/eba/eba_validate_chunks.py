import json
import re
from pathlib import Path

EBA_NOISE_PATTERNS = [
    r"EBA/GL/\d{4}/\d+",
    r"FINAL REPORT",
    r"European Banking Authority",
]

MIN_EBA_PARAGRAPH_LENGTH = 50


def load_chunks(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_paragraph_boundary(chunks):
    """
    Each EBA paragraph must start with its paragraph number (e.g. '1.', '2.')
    """
    for c in chunks:
        if c.get("document_id", "").startswith("eba"):
            para_no = c.get("paragraph_number")
            if para_no:
                expected_start = f"{para_no}."
                if not c["text"].lstrip().startswith(expected_start):
                    print(f"⚠ Paragraph boundary mismatch in {c['chunk_id']}")


def validate_duplicate_paragraphs(chunks):
    """
    Detect duplicate paragraph numbers within the same document.
    """
    seen = set()

    for c in chunks:
        if c.get("document_id", "").startswith("eba"):
            para_no = c.get("paragraph_number")
            if para_no:
                key = (c.get("document_id"), para_no)
                if key in seen:
                    print(f"⚠ Duplicate EBA paragraph {para_no} in {c['chunk_id']}")
                seen.add(key)


def validate_paragraph_length(chunks):
    """
    Detect abnormally short paragraphs (likely extraction errors).
    """
    for c in chunks:
        if c.get("document_id", "").startswith("eba"):
            if len(c["text"].strip()) < MIN_EBA_PARAGRAPH_LENGTH:
                print(f"⚠ Very short EBA paragraph in {c['chunk_id']}")


def validate_eba_noise_removal(chunks):
    """
    Ensure headers / metadata noise was removed.
    """
    for c in chunks:
        if c.get("document_id", "").startswith("eba"):
            for pattern in EBA_NOISE_PATTERNS:
                if re.search(pattern, c["text"], re.MULTILINE):
                    print(f"⚠ EBA noise found in {c['chunk_id']}")


def run_validation(json_path: Path):
    chunks = load_chunks(json_path)
    print(f"Loaded {len(chunks)} chunks for validation.")

    validate_paragraph_boundary(chunks)
    validate_duplicate_paragraphs(chunks)
    validate_paragraph_length(chunks)
    validate_eba_noise_removal(chunks)

    print("✅ Validation complete.")
