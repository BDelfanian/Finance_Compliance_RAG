import re
from typing import List, Dict, Tuple


PARAGRAPH_PATTERN = re.compile(
    r"^(\d+)\.\s+(.*)",
    re.MULTILINE
)

SECTION_TITLE_PATTERN = re.compile(
    r"^[A-Z][A-Za-z\s\-]{5,}$",
    re.MULTILINE
)


def find_sections(text: str) -> List[Tuple[str, int]]:
    """
    Returns list of (section_title, position)
    """
    sections = []
    for match in SECTION_TITLE_PATTERN.finditer(text):
        sections.append((match.group(0).strip(), match.start()))
    return sections


def find_paragraphs(text: str) -> List[Tuple[str, int]]:
    """
    Returns list of (paragraph_number, position)
    """
    paragraphs = []
    for match in PARAGRAPH_PATTERN.finditer(text):
        paragraphs.append((match.group(1), match.start()))
    return paragraphs


def build_paragraph_chunks(text: str) -> List[Dict]:
    paragraphs = find_paragraphs(text)
    sections = find_sections(text)

    chunks = []

    if not paragraphs:
        return chunks

    def section_for_position(pos):
        current = None
        for section in sections:
            if section[1] <= pos:
                current = section
            else:
                break
        return current

    for i, (para_no, start_pos) in enumerate(paragraphs):
        end_pos = paragraphs[i + 1][1] if i + 1 < len(paragraphs) else len(text)
        content = text[start_pos:end_pos].strip()

        section = section_for_position(start_pos)

        chunks.append({
            "chunk_id": f"eba_outsourcing_paragraph_{para_no}",
            "document_id": "eba_gl_outsourcing",
            "document_title": "EBA Guidelines on Outsourcing Arrangements",
            "authority": "European Banking Authority",
            "jurisdiction": "EU",
            "binding_level": "Guideline (Comply or Explain)",
            "paragraph_number": para_no,
            "section_title": section[0] if section else "",
            "text": content
        })

    return chunks
