"""
STEP 6.2 — Summarization Agent (Corrected)
-----------------------------------------
Produces conservative, role-aware summaries
derived strictly from citation-bound answers (STEP 5).

NO new interpretation
NO new citations
NO scope expansion
"""

from typing import Dict, Any, List
import re

from src.orchestrator.agent_schema import AgentResult
from src.orchestrator.agent_validation import validate_agent_result


def _clean_answer_text(answer: str) -> List[str]:
    """
    Normalize answer text:
    - Remove bullets (leading and inline)
    - Remove headings
    - Normalize dash artifacts
    - Split into clean sentences
    """

    # -------------------------------
    # 1. Normalize inline bullet artifacts
    # -------------------------------
    # Examples handled:
    # ". - Sentence" / ". – Sentence" / ". — Sentence"
    normalized = re.sub(r"\s+[–—-]\s+", " ", answer)

    lines = normalized.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # Drop empty lines
        if not line:
            continue

        # Drop headings
        if line.endswith(":"):
            continue

        # Remove leading bullet prefixes
        for prefix in ["- ", "• ", "* "]:
            if line.startswith(prefix):
                line = line[len(prefix):].strip()

        cleaned_lines.append(line)

    # -------------------------------
    # 2. Conservative sentence split
    # -------------------------------
    sentences: List[str] = []

    for line in cleaned_lines:
        parts = [p.strip() for p in line.split(".") if p.strip()]
        sentences.extend(parts)

    return sentences


async def summarization_agent(
    citation_result: Dict[str, Any],
    mode: str = "executive",
) -> AgentResult:
    """
    mode:
    - executive: high-level management summary
    - audit: slightly more detailed, control-focused
    """

    answer_text = citation_result.get("answer", "")
    citations = citation_result.get("citations", [])
    base_confidence = float(citation_result.get("confidence", 0.0))

    if not answer_text:
        result: AgentResult = {
            "agent_name": "summarization",
            "answer": "Summary unavailable due to missing citation-bound answer.",
            "citations": citations,
            "confidence": 0.0,
            "warnings": ["Missing citation-bound answer"],
        }
        validate_agent_result(result)
        return result

    sentences = _clean_answer_text(answer_text)

    if not sentences:
        result: AgentResult = {
            "agent_name": "summarization",
            "answer": "Summary unavailable due to unprocessable source content.",
            "citations": citations,
            "confidence": 0.0,
            "warnings": ["Unprocessable source content"],
        }
        validate_agent_result(result)
        return result

    # -------------------------------
    # Role-aware compression
    # -------------------------------

    if mode == "executive":
        selected = sentences[:2]
    elif mode == "audit":
        selected = sentences[:4]
    else:
        raise ValueError(f"Unsupported summarization mode: {mode}")

    summary_text = ". ".join(selected)
    if not summary_text.endswith("."):
        summary_text += "."

    # Summary confidence must not exceed source confidence
    summary_confidence = round(min(base_confidence, 0.95), 3)

    result: AgentResult = {
        "agent_name": "summarization",
        "answer": summary_text,
        "citations": citations,
        "confidence": summary_confidence,
        "warnings": [],
    }

    validate_agent_result(result)
    return result
