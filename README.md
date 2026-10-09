# AI Agent with Memory

A Streamlit AI assistant demonstrating short-term conversation memory
and long-term user memory using Groq and SQLite.

## Features

- Conversational AI chat interface
- Short-term memory using recent conversation messages
- Explicitly requested long-term memory saving
- SQLite persistence for saved memories
- Keyword-based memory retrieval
- Memory management and search
- Individual memory deletion
- Delete-all functionality
- User-controlled memory saving

## Technologies

- Python
- Streamlit
- Groq API
- SQLite

## Project Structure

```text
AI-Agent-Memory/
├── app.py
├── memory_manager.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml