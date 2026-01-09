"""
STEP 6.1 — Agent Output Schema
------------------------------
Defines a strict, auditable contract for all STEP 6 agents.
"""

from typing import TypedDict, List


class AgentResult(TypedDict):
    agent_name: str
    answer: str
    citations: List[str]
    confidence: float
    warnings: List[str]
