import json
import re
from pathlib import Path

EBA_NOISE_PATTERNS = [
    r"EBA/GL/\d{4}/\d+",
    r"FINAL REPORT",
    r"European Banking Authority",
]

def load_chunks(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_paragraph_boundary(chunks):
    for c in chunks:
        if c.get("document_id", "").startswith("eba"):
            para_no = c.get("paragraph_number")
            if para_no:
                expected_start = f"{para_no}."
                if not c["text"].lstrip().startswith(expected_start):
                    print(f"⚠ Paragraph boundary mismatch in {c['chunk_id']}")

def validate_paragraph_order(chunks):
    paragraph_numbers = []

    for c in chunks:
        if "paragraph_number" in c:
            try:
                paragraph_numbers.append(int(c["paragraph_number"]))
            except ValueError:
                pass

    if paragraph_numbers != sorted(paragraph_numbers):
        print("⚠ EBA paragraphs are not in numeric order")

def validate_eba_noise_removal(chunks):
    for c in chunks:
        if c.get("document_id", "").startswith("eba"):
            for pattern in EBA_NOISE_PATTERNS:
                if re.search(pattern, c["text"], re.MULTILINE):
                    print(f"⚠ EBA noise found in {c['chunk_id']}")


def run_validation(json_path: Path):
    chunks = load_chunks(json_path)
    print(f"Loaded {len(chunks)} chunks for validation.")

    validate_paragraph_boundary(chunks)
    validate_paragraph_order(chunks)
    validate_eba_noise_removal(chunks)

    print("✅ Validation complete.")
