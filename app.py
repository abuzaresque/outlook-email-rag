# app.py
import streamlit as st
from datetime import datetime, timedelta

from config import GROQ_API_KEY, GRAPH_ACCESS_TOKEN
from email_utils import fetch_emails
from rag_pipeline import build_retrieval_chain

def main():
    st.set_page_config(page_title="Outlook Email RAG Assistant", layout="wide")
    st.title("Email Query Assistant (Groq + LangChain)")

    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        access_token = st.text_area(
            "Microsoft Graph Access Token",
            value=GRAPH_ACCESS_TOKEN,
            height=150
        )
        groq_key = st.text_input(
            "Groq API Key", 
            value=GROQ_API_KEY, 
            type="password"
        )
        date = st.date_input("Select Date", datetime.today() - timedelta(days=1))
        date_str = date.strftime("%Y-%m-%d")

        if st.button("Fetch Emails"):
            if access_token:
                emails = fetch_emails(access_token.strip(), date_str)
                
                st.session_state['emails'] = emails
            else:
                st.error("Access token is missing!")

    if 'emails' in st.session_state and st.session_state['emails']:
        st.subheader("Fetched Emails Preview")
        with st.expander("Show sample emails"):
            for i, mail in enumerate(st.session_state['emails'][:5]):
                st.markdown(f"**{i+1}. {mail.get('subject', 'No Subject')}**")
                st.caption(mail.get('bodyPreview', '')[:150])
                st.divider()

        st.subheader("Ask a Question")
        query = st.text_input("What do you want to know from your emails?")
        if st.button("Analyze"):
            with st.spinner("Thinking..."):
                qa_chain = build_retrieval_chain(
                    st.session_state['emails'],
                    groq_key.strip(),
                    date_str
                    )

                if qa_chain:
                    answer = qa_chain.run(query)
                    st.success(answer)

    else:
        st.info("Use the sidebar to configure and fetch emails first.")

if __name__ == "__main__":
    main()
