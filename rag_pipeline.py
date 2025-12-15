# rag_pipeline.py
import os
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

def build_retrieval_chain(emails, groq_api_key, target_date_str):
    """Create or load a Chroma vector store for a specific date, then return a QA chain."""

    if not emails:
        st.warning("No emails found to process.")
        return None

    # Create a directory path for this specific date
    persist_dir = os.path.join("vector_store", target_date_str)
    os.makedirs(persist_dir, exist_ok=True)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Load existing vector store if available
    if os.path.exists(os.path.join(persist_dir, "chroma.sqlite3")):
        # st.info(f" Found existing vector store for {target_date_str} — loading...")
        vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        # st.info(f" Creating new vector store for {target_date_str}...")

        # Convert emails to LangChain Documents
        docs = []
        for mail in emails:
            content = (
                f"Subject: {mail.get('subject', 'No Subject')}\n"
                f"From: {mail.get('from', {}).get('emailAddress', {}).get('address', 'Unknown')}\n"
                f"Received: {mail.get('receivedDateTime', 'Unknown')}\n\n"
                f"Body: {mail.get('bodyPreview', '')}"
            )
            docs.append(Document(page_content=content))

        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        vectordb = Chroma.from_documents(chunks, embeddings, persist_directory=persist_dir)
        vectordb.persist()
        # st.success(f" Vector store created for {target_date_str} and saved locally.")

    # Initialize Groq LLM
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=groq_api_key
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever()
    )

    return qa_chain
