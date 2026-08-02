# Product Requirements Document: Lenny Growth Assistant

## Overview
An AI-powered chat application that answers questions from Lenny's Podcast transcripts, generates essays, and creates HTML/Markdown artifacts.

## Problem Statement
Founders and startup enthusiasts need quick access to insights from Lenny's Podcast but lack:
- Searchable access to transcript knowledge
- Ability to generate structured content from insights
- Interactive learning experience

## Solution
A chat interface that:
1. Answers questions using transcript context
2. Generates essays/articles from insights
3. Creates HTML/Markdown artifacts
4. Provides artifact previews

## Target Users
- Startup founders
- Product managers
- Growth marketers
- Startup enthusiasts
- Content creators

## Core Features

### 1. Chat Interface
- ChatGPT-like conversation
- Session management
- Message history

### 2. RAG System
- FAISS vector search
- Sentence transformer embeddings
- Context retrieval from transcripts

### 3. Content Generation
- Essay generation (Ship30for30 style)
- HTML artifact creation
- Markdown artifact creation

### 4. Artifact Viewer
- HTML rendering preview
- Markdown formatting
- Side-by-side with chat

### 5. Multi-LLM Support
- Groq API (Llama 3.3)
- Ollama (local)
- Provider switching

## Technical Architecture

### Backend (FastAPI)
```
User Request → FastAPI → Router
                      ├── Q&A → RAG → LLM
                      ├── Essay Generator → LLM
                      └── Artifact Generator → LLM
```

### Frontend
```
HTML + CSS + JavaScript
├── Chat Interface
├── Artifact Viewer
└── Settings Panel
```

### Data Flow
1. User sends message
2. Frontend → Backend API
3. RAG searches transcripts
4. LLM generates response
5. Response saved to Supabase
6. Response displayed in chat
7. Artifacts shown in viewer

## Success Metrics
- Response accuracy from transcripts
- User engagement (messages per session)
- Artifact generation usage
- Session duration

## Future Enhancements
- User authentication
- Transcript upload interface
- Custom prompt templates
- Export functionality
- Mobile app
- API rate limiting
- Analytics dashboard

## Constraints
- 3-hour development window
- Minimal viable product
- Focus on core features
- Simple deployment