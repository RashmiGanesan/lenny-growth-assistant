from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

from utils import (
    generate_session_id,
    format_chat_response,
    format_essay_prompt,
    format_rag_prompt,
    format_html_prompt,
    format_markdown_prompt
)

from rag import RAGSystem
from llm import LLMProvider
from database import Database


# Load .env variables
load_dotenv()


# -----------------------------
# Initialize FastAPI
# -----------------------------

app = FastAPI(
    title="Lenny Growth Assistant API",
    version="1.0.0"
)


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Initialize Services
# -----------------------------

rag_system = RAGSystem()

database = Database()

llm_provider = LLMProvider("groq")


# -----------------------------
# Load FAISS Index
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

index_path = os.path.join(
    BASE_DIR,
    "../data/faiss_index/index.faiss"
)

documents_path = os.path.join(
    BASE_DIR,
    "../data/faiss_index/documents.pkl"
)


if os.path.exists(index_path) and os.path.exists(documents_path):

    rag_system.load_index(
        index_path,
        documents_path
    )

    print("✅ FAISS index loaded")

else:
    print("❌ FAISS index not found")


# -----------------------------
# Request Models
# -----------------------------

class ChatRequest(BaseModel):

    message: str

    session_id: Optional[str] = None

    response_type: str = "text"



class ChatResponse(BaseModel):

    content: str

    type: str

    session_id: str

    timestamp: str



class SessionResponse(BaseModel):

    session_id: str



class HistoryResponse(BaseModel):

    messages: List[Dict[str, Any]]



# -----------------------------
# Routes
# -----------------------------


@app.get("/")
async def home():

    return {

        "name": "Lenny Growth Assistant API",

        "status": "running",

        "version": "1.0.0",

        "docs":
        "http://127.0.0.1:8000/docs"

    }



@app.get("/health")
async def health():

    return {

        "status": "healthy",

        "rag_loaded": rag_system.is_loaded

    }



@app.post(
    "/new-chat",
    response_model=SessionResponse
)
async def new_chat():

    session_id = generate_session_id()

    database.create_session(session_id)


    return {

        "session_id": session_id

    }



@app.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    try:

        # create session
        session_id = (
            request.session_id
            if request.session_id
            else generate_session_id()
        )


        if not request.session_id:

            database.create_session(session_id)



        # save user message

        database.save_message(

            session_id,

            "user",

            request.message,

            request.response_type

        )



        # Retrieve document context from transcripts
        context = ""

        # Always retrieve context for knowledge-based responses
        # HTML and Markdown can also benefit from transcript content
        if rag_system.is_loaded and request.response_type in ["text", "essay", "html", "markdown"]:
            context = rag_system.get_relevant_context(request.message)
            print(f"📚 Retrieved context for '{request.message}'")
            
            # Log context quality for debugging
            if context.startswith("No relevant context"):
                print(f"⚠️  Limited context found for query: {request.message}")
            else:
                # Count extracts found
                import re
                extract_matches = re.findall(r'EXTRACT \d+', context)
                print(f"✅ Found {len(extract_matches)} relevant transcript extracts")



        # Create appropriate prompt based on response type
        if request.response_type == "essay":
            prompt = format_essay_prompt(request.message, context)
        elif request.response_type == "html":
            prompt = format_html_prompt(request.message, context)
        elif request.response_type == "markdown":
            prompt = format_markdown_prompt(request.message, context)
        else:
            # Text responses use RAG prompt
            prompt = format_rag_prompt(request.message, context)



        # Generate answer

        response = llm_provider.generate_response(

            prompt,

            request.response_type

        )



        # Save AI response

        database.save_message(

            session_id,

            "ai",

            response["content"],

            response["type"]

        )



        return format_chat_response(

            response["content"],

            response["type"],

            session_id

        )


    except Exception as e:

        print(
            "CHAT ERROR:",
            e
        )

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )




@app.get(
    "/history/{session_id}",
    response_model=HistoryResponse
)
async def history(session_id:str):

    messages = database.get_chat_history(
        session_id
    )


    return {

        "messages":messages

    }



@app.post("/switch-provider")
async def switch_provider(provider:str):

    global llm_provider


    if provider not in [
        "groq",
        "ollama"
    ]:

        raise HTTPException(

            status_code=400,

            detail="Only groq or ollama allowed"

        )


    llm_provider = LLMProvider(provider)


    return {

        "message":
        "Provider changed",

        "provider":
        provider

    }




# -----------------------------
# Run Server
# -----------------------------

if __name__ == "__main__":

    import uvicorn


    print("==============================")
    print("🚀 Lenny Growth Assistant API")
    print("==============================")
    print(
        "RAG:",
        rag_system.is_loaded
    )

    print(
        "LLM:",
        llm_provider.provider
    )

    print(
        "Database: SQLite"
    )


    uvicorn.run(

        "app:app",

        host="0.0.0.0",

        port=8000,

        reload=False

    )