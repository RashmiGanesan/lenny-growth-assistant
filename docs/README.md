# Lenny Growth Assistant

An AI-powered chat application that answers questions from Lenny's Podcast transcripts, generates essays, and creates HTML/Markdown artifacts.

## Features

1. **Chat Interface**: ChatGPT-like interface for Q&A about startup growth
2. **RAG System**: Retrieves relevant information from podcast transcripts
3. **Essay Generation**: Converts answers into Ship30for30-style articles
4. **Artifact Generation**: Creates HTML/Markdown outputs
5. **Artifact Viewer**: Renders artifacts beside the chat
6. **Multi-LLM Support**: Switch between Groq API and Ollama (local)

## Project Structure

```
lenny-growth-assistant/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── rag.py              # RAG system with FAISS
│   ├── llm.py              # LLM provider (Groq/Ollama)
│   ├── database.py         # Supabase integration
│   ├── utils.py            # Helper functions
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── frontend/
│   ├── index.html         # Main HTML file
│   ├── style.css          # CSS styles
│   └── script.js          # Frontend JavaScript
├── data/
│   ├── transcripts/       # Podcast transcripts
│   └── faiss_index/      # FAISS index files
└── docs/
    └── README.md         # This file
```

## Quick Start

### 1. Backend Setup

```bash
cd lenny-growth-assistant/backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start the backend server
python app.py
```

### 2. Frontend Setup

Open `frontend/index.html` in your browser or use a local server:

```bash
# Using Python's built-in server
cd lenny-growth-assistant/frontend
python -m http.server 8080
```

Then open `http://localhost:8080` in your browser.

### 3. Configuration

#### Environment Variables (.env)
```
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
GROQ_API_KEY=your_groq_api_key_here
OLLAMA_BASE_URL=http://localhost:11434
```

#### FAISS Index Setup
1. Place transcript text files in `data/transcripts/`
2. Run the index creation script (to be implemented)
3. The system will automatically load the index on startup

## API Endpoints

- `POST /new-chat` - Create new chat session
- `POST /chat` - Send message and get AI response
- `GET /history/{session_id}` - Get chat history
- `POST /switch-provider` - Switch LLM provider
- `GET /health` - Health check

## Development

### Running the Project

```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
cd frontend
python -m http.server 8080
```

### Adding Transcripts

1. Add transcript text files to `data/transcripts/`
2. Create FAISS index (script to be implemented)
3. Restart backend to load new index

## Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: HTML, CSS, JavaScript
- **RAG**: FAISS, Sentence Transformers
- **LLM**: Groq API (Llama 3.3) / Ollama
- **Database**: SPostgreSQL
