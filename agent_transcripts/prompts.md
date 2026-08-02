# Agent Transcripts & Prompts

## Development Context
This document contains the prompts and instructions used during the development of the Lenny Growth Assistant project.

## Project Creation Prompt

**Original Request:**
```
Project: Lenny Growth Assistant
Goal: Build an AI-powered chat application that answers questions from Lenny's Podcast transcripts, generates essays, and creates HTML/Markdown artifacts.

Tech Stack (Simple):
Backend: FastAPI, Python, FAISS (RAG), Sentence Transformers, Ollama (Llama 3.2), Supabase PostgreSQL
Frontend: HTML, CSS, JavaScript (no React if you prefer)

Features:
1. Chat: ChatGPT-like interface
2. New Chat: Start fresh conversations
3. Store Chats: Save in Supabase
4. Knowledge Base (RAG): Load transcripts into FAISS
5. Essay Generation: Convert answers into Ship30for30-style articles
6. Artifact Generation: HTML/Markdown outputs
7. Artifact Viewer: Display artifacts beside chat
8. LLM Toggle: Switch between Ollama/Cloud models

Overall Flow:
User → HTML + CSS + JavaScript Chat UI → FastAPI → Router → Q&A/Essay/Artifact → LLM → Supabase → Show Chat + Artifact Viewer
```

## Implementation Decisions

### 1. File Structure
- Minimal 5 backend Python files
- 3 frontend files (HTML, CSS, JS)
- Documentation in `/docs`
- Data directories for transcripts

### 2. Technology Choices
- **Groq API** over OpenAI (free tier, Llama 3.3)
- **Ollama** fallback for local development
- **FAISS** for local vector search
- **Supabase** for free PostgreSQL
- **Vanilla JS** for simplicity

### 3. Component Design

#### Backend Components:
- `app.py`: FastAPI server with endpoints
- `rag.py`: FAISS-based retrieval system
- `llm.py`: Groq/Ollama integration
- `database.py`: Supabase operations
- `utils.py`: Helper functions

#### Frontend Components:
- Three-column layout (sidebar, chat, artifact)
- Responsive design
- Mock responses for development
- Artifact preview system

### 4. Key Features Implemented

#### RAG System:
- Sentence transformer embeddings
- FAISS similarity search
- Context retrieval from transcripts
- Fallback to mock data

#### LLM Integration:
- Groq API with Llama 3.3 70B
- Ollama local support
- Prompt engineering for different response types
- Error handling and fallbacks

#### Artifact Generation:
- HTML formatting with CSS
- Markdown rendering
- Preview system with iframe
- Type-specific prompts

### 5. Development Challenges & Solutions

#### Challenge 1: FAISS Index Setup
- **Problem**: Transcript data not available initially
- **Solution**: Mock RAG system with sample data
- **Future**: Index creation script for real transcripts

#### Challenge 2: API Key Management
- **Problem**: Sensitive keys in code
- **Solution**: `.env` file with template
- **Future**: Environment variable validation

#### Challenge 3: Frontend-Backend Integration
- **Problem**: Cross-origin requests
- **Solution**: CORS middleware in FastAPI
- **Future**: Production CORS configuration

#### Challenge 4: Error Handling
- **Problem**: API failures break user experience
- **Solution**: Mock responses with clear errors
- **Future**: Comprehensive error reporting

### 6. Prompt Engineering

#### RAG Prompt Template:
```
Answer the question based only on the provided context from Lenny's Podcast transcripts.

CONTEXT:
{context}

QUESTION:
{question}

INSTRUCTIONS:
1. Answer ONLY using information from the context
2. If context doesn't contain relevant information, say "I don't have information about that"
3. Be specific and reference examples from context
4. Keep answers concise but informative
```

#### Essay Prompt Template:
```
Convert the following information into a Ship30for30-style article (~1250 words).

CONTEXT FROM TRANSCRIPTS:
{context}

USER QUESTION:
{question}

Write a compelling article with:
1. A strong hook that grabs attention
2. Clear bullet points for key takeaways
3. Bold highlights for important concepts
4. A clear, actionable takeaway

Structure:
- Introduction with hook
- 3-5 key points with examples
- Practical applications
- Conclusion with clear takeaway

Write in a conversational, engaging tone with concrete examples from startups mentioned in transcripts.
```

#### Artifact Prompt Templates:
- **HTML**: "Create HTML content about: {topic}"
- **Markdown**: "Create markdown content about: {topic}"

### 7. Testing Instructions

#### Backend Testing:
```bash
cd backend
python app.py  # Starts on http://localhost:8000
```

#### Frontend Testing:
```bash
cd frontend
python -m http.server 8080  # Open http://localhost:8080
```

#### API Testing:
```bash
# Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/new-chat
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"Hello", "response_type":"text"}'
```

### 8. Deployment Notes

#### Environment Setup:
1. Install Python dependencies: `pip install -r requirements.txt`
2. Configure `.env` file with API keys
3. Set up Supabase database tables
4. Create FAISS index from transcripts

#### Production Considerations:
- Use proper CORS origins
- Implement rate limiting
- Add authentication (future)
- Set up monitoring
- Use CDN for frontend

### 9. Future Enhancements

#### Priority 1:
- Transcript upload interface
- FAISS index creation UI
- User authentication
- Export functionality

#### Priority 2:
- Mobile responsive improvements
- Real-time updates
- Analytics dashboard
- Custom prompt templates

#### Priority 3:
- Multiple knowledge bases
- Team collaboration features
- API documentation portal
- Mobile app

### 10. Lessons Learned

#### What Worked Well:
- Minimal file structure kept focus
- Mock systems allowed parallel development
- Clear component separation
- Progressive enhancement approach

#### What Could Improve:
- Better error handling in frontend
- More comprehensive testing
- Configuration validation
- Documentation automation

### 11. Quick Start Commands

```bash
# 1. Navigate to project
cd lenny-growth-assistant

# 2. Start backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# 3. Start frontend (new terminal)
cd frontend
python -m http.server 8080

# 4. Open browser
# Backend: http://localhost:8000
# Frontend: http://localhost:8080
```

### 12. Troubleshooting

#### Common Issues:
1. **Backend not starting**: Check Python version and dependencies
2. **CORS errors**: Verify FastAPI CORS configuration
3. **API key errors**: Check `.env` file format
4. **Frontend not connecting**: Verify backend is running on port 8000

#### Debug Steps:
1. Check console logs in browser
2. Test API endpoints directly with curl
3. Verify environment variables
4. Check network tab for request/response

---

**Project Status**: MVP Complete  
**Development Time**: ~2 hours  
**Lines of Code**: ~1500  
**Files Created**: 13  
**Next Steps**: Add real transcript data, implement index creation, deploy to cloud