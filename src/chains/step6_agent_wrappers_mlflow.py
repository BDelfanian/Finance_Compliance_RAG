import json
import tempfile
from typing import Dict, Any, Callable, Awaitable

import mlflow
from langchain_core.runnables import Runnable

# -------------------------------
# MLflow Logging Helper
# -------------------------------
async def log_agent_run(agent_name: str, payload: Dict[str, Any]):
    """
    Logs the agent payload to MLflow in JSON format.
    Automatically starts a run if none exists.
    """
    # Start a nested run if already in a run; else a new run
    with mlflow.start_run(run_name=agent_name, nested=True):
        tmp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        json.dump(payload, tmp_file, indent=2)
        tmp_file.close()
        mlflow.log_artifact(tmp_file.name, artifact_path=agent_name)


# -------------------------------
# Runnable wrapper with MLflow
# -------------------------------
def wrap_agent_with_mlflow(agent_fn: Callable[..., Awaitable[Dict[str, Any]]]) -> Runnable:
    """
    Wraps an async agent with:
    - MLflow logging
    - LangChain Runnable interface
    """

    async def wrapped_fn(inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Run the original agent
        outputs = await agent_fn(**inputs)

        # Log to MLflow
        try:
            await log_agent_run(agent_name=outputs.get("agent_result", {}).get("agent_name", "unknown"),
                                payload=outputs)
        except Exception as e:
            print(f"MLflow logging skipped: {e}")

        return outputs

    # RunnableLambda equivalent: sync dummy + async afunc
    from langchain_core.runnables import RunnableLambda
    return RunnableLambda(lambda x: x, afunc=wrapped_fn)


# -------------------------------
# Example agent chain wrappers
# -------------------------------
from src.agents.retrieval_agent import retrieval_agent
from src.agents.citation_agent import citation_agent
from src.agents.summarization_agent import summarization_agent
from src.agents.risk_assessment_agent import risk_assessment_agent

# Wrap agents with MLflow logging
retrieval_chain = wrap_agent_with_mlflow(retrieval_agent)
citation_chain = wrap_agent_with_mlflow(citation_agent)
summarization_chain = wrap_agent_with_mlflow(summarization_agent)
risk_assessment_chain = wrap_agent_with_mlflow(risk_assessment_agent)
