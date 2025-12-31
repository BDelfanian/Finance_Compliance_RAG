import re
from typing import List, Dict, Tuple


CHAPTER_PATTERN = re.compile(
    r"^CHAPTER\s+([IVX]+)\b\s*(.*)?$",
    re.MULTILINE
)

ARTICLE_PATTERN = re.compile(
    r"^Article\s+(\d+)\b(?:\s*[–-]\s*(.*))?$",
    re.MULTILINE
)


def find_chapters(text: str) -> List[Tuple[str, int, str]]:
    """
    Returns list of (chapter_id, position, title)
    """
    chapters = []

    for match in CHAPTER_PATTERN.finditer(text):
        chapter_id = f"CHAPTER {match.group(1)}"
        title = (match.group(2) or "").strip()
        chapters.append((chapter_id, match.start(), title))

    return chapters


def find_articles(text: str) -> List[Tuple[str, int, str]]:
    """
    Returns list of (article_number, position, title)
    """
    articles = []

    for match in ARTICLE_PATTERN.finditer(text):
        article_number = match.group(1)
        title = (match.group(2) or "").strip()
        articles.append((article_number, match.start(), title))

    return articles


def build_article_chunks(text: str) -> List[Dict]:
    articles = find_articles(text)
    chapters = find_chapters(text)

    chunks = []

    if not articles:
        return chunks

    # helper to find chapter context
    def chapter_for_position(pos):
        current = None
        for chap in chapters:
            if chap[1] <= pos:
                current = chap
            else:
                break
        return current

    for i, (article_no, start_pos, title) in enumerate(articles):
        end_pos = articles[i + 1][1] if i + 1 < len(articles) else len(text)
        content = text[start_pos:end_pos].strip()

        chapter = chapter_for_position(start_pos)

        chunks.append({
            "chunk_id": f"dora_article_{article_no}",
            "document_id": "dora_2022_2554",
            "document_title": "Regulation (EU) 2022/2554 (DORA)",
            "authority": "European Union",
            "jurisdiction": "EU",
            "binding_level": "EU Regulation",
            "chapter": f"{chapter[0]} – {chapter[2]}" if chapter else "",
            "article_number": f"Article {article_no}",
            "article_title": title,
            "text": content
        })

    return chunks
