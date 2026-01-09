"""
STEP 6 — Citation Agent (Adapter)
--------------------------------
This agent is a thin adapter over STEP 5's citation-bound
answer generation logic.

Design principles:
- ZERO new logic
- ZERO prompt changes
- Deterministic passthrough
- Explicit contract normalization
"""

from typing import Dict, Any, List

from src.generation.citation_bound_answer_generation import (
    generate_citation_bound_answer_cached
)
from src.orchestrator.agent_schema import AgentResult
from src.orchestrator.agent_validation import validate_agent_result


async def citation_agent(
    query: str,
    retrieval_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    STEP 6 adapter for STEP 5 citation-bound answer generation.

    Responsibilities:
    - Generate citation-bound answer (STEP 5)
    - Return validated AgentResult for orchestration
    - Include raw retrieval payload if needed downstream
    """

    # -------------------------------
    # STEP 5 passthrough
    # -------------------------------
    citation_output = generate_citation_bound_answer_cached(
        query_text=query,
        top_k=5
    )

    retrieved_chunks: List[dict] = citation_output.get("retrieved_chunks", [])
    answer_text: str = citation_output.get("answer", "")
    confidence: float = float(citation_output.get("answer_confidence", 0.0))
    timestamp: str = citation_output.get("timestamp", "")

    # -------------------------------
    # AgentResult normalization
    # -------------------------------
    agent_result: AgentResult = {
        "agent_name": "citation",
        "answer": answer_text,
        "citations": retrieved_chunks,
        "confidence": confidence,
        "warnings": [],
    }

    validate_agent_result(agent_result)

    # -------------------------------
    # Return BOTH validated agent result and raw retrieval chunks
    # -------------------------------
    return {
        "agent_result": agent_result,
        "retrieved_chunks": retrieved_chunks,
        "timestamp": timestamp,
    }
