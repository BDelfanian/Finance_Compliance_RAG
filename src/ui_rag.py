import streamlit as st
import json
from run_embeddings_retrieval import retrieve  # your existing code

st.title("Regulatory Retrieval Assistant")

query_text = st.text_area("Enter your regulatory query:", "")

regulator_options = ["CSSF", "DORA", "EBA"]
regulator_map = {
    "CSSF": ("cssf", "CSSF", "LU"),
    "DORA": ("dora", "European Union", "EU"),
    "EBA": ("eba", "European Banking Authority", "EU")
}

regulator_choice = st.selectbox("Select regulator:", regulator_options)

if st.button("Retrieve"):
    store_key, authority, jurisdiction = regulator_map[regulator_choice]
    result = retrieve(
        query_text=query_text,
        vector_store_key=store_key,
        authority=authority,
        jurisdiction=jurisdiction,
        top_k=5
    )

    st.subheader("Retrieved Chunks")
    if result["retrieved_chunks"]:
        for chunk in result["retrieved_chunks"]:
            st.markdown(f"**ID:** {chunk['chunk_id']}")
            st.markdown(f"**Reference:** {chunk['source_reference']}")
            st.markdown(f"**Similarity:** {chunk['similarity_score']:.2f}")
            st.markdown("---")
    else:
        st.write("No relevant chunks found.")
