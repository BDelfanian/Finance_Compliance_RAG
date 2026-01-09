5️⃣ What You Must NOT Do (Yet)

Explicitly forbidden at STEP 6.3:

❌ ChatPromptTemplate
❌ LLMChain
❌ ConversationBufferMemory
❌ RunnableParallel
❌ LangGraph

Those belong to STEP 7+, after human-in-the-loop controls.



STEP 6.4 — MLflow lineage logging (agent-level, not orchestration-level)

This is exactly how LangChain should be introduced in regulated systems.


Here’s the one-sentence mental model for LangChain testing:

“Always wrap your async agent in a RunnableLambda (or a helper like make_chain) and patch the wrapper, not the underlying function, because ainvoke returns a coroutine and RunnableLambda requires both a dummy sync func and an async afunc.”


Enable multi-turn context/memory management for the UI.

set PYTHONPATH=E:\Data Science\Research\RAG\Projects\Finance_Compliance_RAG


