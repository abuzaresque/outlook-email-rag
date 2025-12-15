# Outlook Email RAG Assistant

A Retrieval-Augmented Generation (RAG) based email querying application built with Streamlit and LangChain.
This application fetches emails from Microsoft Graph API, processes them using a Retrieval-Augmented Generation (RAG) pipeline, and allows users to ask natural language questions about their emails.

## Features

- **Email Fetching**: Retrieve emails from Microsoft Outlook using Graph API for a specific date.
- **Intelligent Q&A**: Ask questions about your emails and get AI-powered answers using Groq's LLaMA model.
- **Vector Store Persistence**: Emails are stored in a local Chroma vector database for efficient retrieval.
- **Streamlit Interface**: User-friendly web interface for configuration and interaction.
- **Date-based Organization**: Vector stores are organized by date for historical querying.

## Prerequisites

- Python 3.8 or higher
- Groq API key
- Internet connection for API calls

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Agentic_A1
   ```

2. Install dependencies:
   ```bash
   pip install streamlit requests langchain langchain-community langchain-groq chromadb python-dotenv
   ```

> ℹ️ The `.env` file is optional.  
> API keys can either be stored in `.env` **or** entered manually in the Streamlit sidebar.

If using `.env`, create a file in the root directory:
   ```env
   GROQ_API_KEY=optional_if_entered_in_ui
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser to the provided URL (usually http://localhost:8501).

3. In the sidebar:
   - Enter your Microsoft Graph Access Token
   - Enter your Groq API Key
   - Select a date for email fetching

4. Click "Fetch Emails" to retrieve emails for the selected date.

5. Once emails are fetched, enter a question in the "Ask a Question" field and click "Analyze" to get an AI-generated response.

## Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key for LLM access

### Microsoft Graph API (Access Token)

This application uses a Microsoft Graph **access token** to fetch emails.

#### Option 1: Using Microsoft Graph Explorer (Recommended for Students)

1. Go to https://developer.microsoft.com/en-us/graph/graph-explorer
2. Sign in with your Outlook account
3. Open the **Permissions** tab
4. Click **Modify permissions**
5. Enable `Mail.Read` and consent
6. Run any query (e.g. `/me/messages`)
7. Open the **Access token** tab and copy the token
8. Paste the token into the Streamlit sidebar

> ⚠️ Paste only the raw token — do NOT include the word `Bearer`.
>

> ℹ️ Graph Explorer tokens expire after a short time (usually ~1 hour).  
> If you receive a 403 error, generate and paste a fresh token.


#### Option 2: Azure App Registration (Advanced)

Users may alternatively register an Azure AD application and obtain a token using MSAL.  
This is **not required** to run the project.

## How It Works

1. **Email Fetching**: Uses Microsoft Graph API to retrieve emails for a specific date.

2. **Document Processing**: Emails are converted to LangChain Document objects with metadata (subject, sender, date, body preview).

3. **Text Splitting**: Documents are split into chunks using CharacterTextSplitter for better retrieval.

4. **Vector Store**: Chunks are embedded using HuggingFace embeddings and stored in Chroma vector database, persisted locally by date.

5. **Retrieval QA**: A RetrievalQA chain is created using Groq's LLaMA model and the vector store as retriever.

6. **Query Processing**: User questions are processed through the QA chain to provide relevant answers based on email content.

Although the assignment allows OpenAI or Hugging Face models, this implementation uses Groq's LLaMA model as a compatible LLM backend with LangChain.

## Dependencies

- `streamlit`: Web interface framework
- `requests`: HTTP requests for Graph API
- `langchain`: Core framework for LLM chains and document processing
- `langchain-community`: Community integrations for vector stores and embeddings
- `langchain-groq`: Groq LLM integration
- `chromadb`: Vector database for embeddings
- `python-dotenv`: Environment variable management

## Notes & Known Issues

- First-time embedding generation may take 20–60 seconds depending on system performance.
- Subsequent runs are fast due to persisted vector stores.
- If a protobuf-related error occurs, ensure:
  ```bash
  pip install protobuf==3.20.3
  ```

## Project Structure

```
Agentic_A1/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration and environment variables
├── email_utils.py         # Email fetching utilities
├── rag_pipeline.py        # RAG pipeline implementation
├── vector_store/          # Persisted Chroma databases (by date)
├── README.md              # This file
└── .env                   # Environment variables (create this)
```

## Disclaimer

This application requires access to your email data. Ensure you have proper permissions and handle API keys securely. The app stores email data locally in vector stores - review privacy implications before use.
