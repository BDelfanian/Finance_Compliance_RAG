"""
STEP 6 — Multi-Agent Orchestrator
--------------------------------
Deterministic orchestration layer coordinating
compliance-grade agents built in STEP 4 & STEP 5.

LangChain is used ONLY as an execution wrapper.
NO logic is delegated to LangChain.
"""

from typing import Dict, Any
from datetime import datetime, timezone
import asyncio

# LangChain-wrapped agents (STEP 6.3)
from src.orchestrator.langchain_wrappers import (
    retrieval_chain,
    citation_chain,
    summarization_chain,
    risk_assessment_chain,
)

# -------------------------------
# Orchestrator
# -------------------------------

class MultiAgentOrchestrator:
    """
    Deterministic orchestration layer.

    Responsibilities:
    - Execute agents in the correct order
    - Enforce fail-fast behavior
    - Aggregate outputs
    - Attach audit metadata
    """

    def __init__(self, model_version: str):
        self.model_version = model_version

    async def run(self, query: str) -> Dict[str, Any]:
        start_time = datetime.now(timezone.utc).isoformat()

        # -------------------------------
        # 1. Retrieval (fail-fast)
        # -------------------------------
        retrieval_result = await retrieval_chain.ainvoke(query)

        if not retrieval_result:
            raise RuntimeError("Retrieval agent returned no results")

        # -------------------------------
        # 2. Citation-bound answer (fail-fast)
        # -------------------------------
        citation_payload = {
            "query": query,
            "retrieval_result": retrieval_result,
        }

        citation_result = await citation_chain.ainvoke(citation_payload)

        agent_citation = citation_result.get("agent_result")
        if not agent_citation or not agent_citation.get("citations"):
            raise RuntimeError("Citation agent failed or returned no citations")

        # -------------------------------
        # 3. Parallel downstream agents
        # -------------------------------
        summary_payload = {
            "citation_result": agent_citation,
            "mode": "executive",
        }

        risk_payload = {
            "citation_result": agent_citation,
            "retrieval_result": retrieval_result,
        }

        summary_result, risk_result = await asyncio.gather(
            summarization_chain.ainvoke(summary_payload),
            risk_assessment_chain.ainvoke(risk_payload),
        )

        # -------------------------------
        # 4. Confidence fusion (conservative)
        # -------------------------------
        final_confidence = min(
            agent_citation.get("confidence", 0.0),
            risk_result.get("confidence", 0.0),
        )

        if risk_result.get("warnings"):
            final_confidence *= 0.8

        # -------------------------------
        # 5. Audit metadata
        # -------------------------------
        audit_trail = {
            "query": query,
            "model_version": self.model_version,
            "agents": [
                "retrieval",
                "citation",
                "summarization",
                "risk_assessment",
            ],
            "timestamp": start_time,
        }

        # -------------------------------
        # 6. Aggregated response
        # -------------------------------
        return {
            "answer": agent_citation,
            "summary": summary_result,
            "risk": risk_result,
            "confidence": round(final_confidence, 3),
            "audit_trail": audit_trail,
        }


# -------------------------------
# Sync convenience wrapper
# -------------------------------

def run_orchestrator(query: str, model_version: str = "gpt-4.1") -> Dict[str, Any]:
    orchestrator = MultiAgentOrchestrator(model_version=model_version)
    return asyncio.run(orchestrator.run(query))
