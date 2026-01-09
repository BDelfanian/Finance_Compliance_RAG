"""
STEP 6 — Orchestrator Tests
--------------------------
Pytest-based validation of deterministic orchestration logic.

These tests deliberately mock agents to:
- Validate fail-fast behavior
- Validate confidence fusion
- Validate risk downgrade logic
- Avoid dependence on LLMs or vector stores
"""

import pytest
from src.orchestrator.multi_agent_orchestrator import MultiAgentOrchestrator


# -------------------------------
# Mock agent implementations
# -------------------------------

async def mock_retrieval_agent(query: str):
    return {
        "chunks": [
            {"source_id": "REG-1", "text": "Sample regulation text"},
            {"source_id": "REG-2", "text": "Another regulation"},
        ]
    }


async def mock_citation_agent(query: str, retrieval_result: dict):
    return {
        "agent_name": "citation",
        "answer": "Regulated entities must disclose X.",
        "citations": [
            {"source_id": "REG-1", "excerpt": "must disclose X", "confidence": 0.9}
        ],
        "confidence": 0.8,
        "warnings": None,
    }


async def mock_summarization_agent(citation_result: dict):
    return {
        "agent_name": "summarization",
        "answer": "Entities must disclose X.",
        "citations": citation_result["citations"],
        "confidence": 0.75,
        "warnings": None,
    }


async def mock_risk_agent(citation_result: dict, retrieval_result: dict):
    return {
        "agent_name": "risk_assessment",
        "answer": "Partial regulatory coverage detected.",
        "citations": citation_result["citations"],
        "confidence": 0.6,
        "warnings": ["Partial regulatory coverage"],
    }


# -------------------------------
# Test helpers
# -------------------------------

@pytest.fixture
def orchestrator(monkeypatch):
    """
    Orchestrator with mocked agents injected.
    """
    from src.orchestrator import multi_agent_orchestrator as mao

    monkeypatch.setattr(mao, "retrieval_agent", mock_retrieval_agent)
    monkeypatch.setattr(mao, "citation_agent", mock_citation_agent)
    monkeypatch.setattr(mao, "summarization_agent", mock_summarization_agent)
    monkeypatch.setattr(mao, "risk_assessment_agent", mock_risk_agent)

    return MultiAgentOrchestrator(model_version="test-model")


# -------------------------------
# Tests
# -------------------------------

@pytest.mark.asyncio
async def test_orchestrator_happy_path(orchestrator):
    result = await orchestrator.run("test query")

    assert "answer" in result
    assert "summary" in result
    assert "risk" in result
    assert "audit_trail" in result

    # Confidence should be min(citation=0.8, risk=0.6) with downgrade
    assert result["confidence"] < 0.6


@pytest.mark.asyncio
async def test_fail_fast_on_missing_retrieval(monkeypatch):
    async def empty_retrieval(query: str):
        return None

    from src.orchestrator import multi_agent_orchestrator as mao
    monkeypatch.setattr(mao, "retrieval_agent", empty_retrieval)

    orchestrator = MultiAgentOrchestrator(model_version="test-model")

    with pytest.raises(RuntimeError):
        await orchestrator.run("test query")


@pytest.mark.asyncio
async def test_fail_fast_on_missing_citations(monkeypatch):
    async def bad_citation_agent(query: str, retrieval_result: dict):
        return {"answer": "text", "citations": [], "confidence": 0.9}

    from src.orchestrator import multi_agent_orchestrator as mao
    monkeypatch.setattr(mao, "retrieval_agent", mock_retrieval_agent)
    monkeypatch.setattr(mao, "citation_agent", bad_citation_agent)

    orchestrator = MultiAgentOrchestrator(model_version="test-model")

    with pytest.raises(RuntimeError):
        await orchestrator.run("test query")
