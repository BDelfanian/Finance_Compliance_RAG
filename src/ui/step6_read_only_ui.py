# src/ui/step6_read_only_ui.py
import streamlit as st
import asyncio

from src.chains import step6_agent_wrappers_mlflow as wrappers

st.set_page_config(page_title="Finance Compliance RAG (Read-only)", layout="wide")
st.title("Finance Compliance RAG – Read-only UI")

query = st.text_input("Enter regulatory query:", "")

if query:
    st.info("Processing query...")

    async def run_agents(query_text):
        # 1️⃣ Retrieval
        retrieval_result = await wrappers.retrieval_chain.ainvoke({"query": query_text})
        
        # 2️⃣ Citation-bound answer
        citation_result = await wrappers.citation_chain.ainvoke({
            "query": query_text,
            "retrieval_result": retrieval_result,
        })
        
        # 3️⃣ Summarization
        summary_result = await wrappers.summarization_chain.ainvoke(citation_result)
        
        # 4️⃣ Risk assessment
        risk_result = await wrappers.risk_assessment_chain.ainvoke({
            "citation_result": citation_result,
            "retrieval_result": retrieval_result
        })

        return retrieval_result, citation_result, summary_result, risk_result

    # Run the async pipeline
    retrieval_result, citation_result, summary_result, risk_result = asyncio.run(run_agents(query))

    # Display outputs
    st.subheader("Retrieval Output")
    st.json(retrieval_result)

    st.subheader("Citation-bound Answer")
    st.json(citation_result)

    st.subheader("Summarization")
    st.json(summary_result)

    st.subheader("Risk Assessment")
    st.json(risk_result)
