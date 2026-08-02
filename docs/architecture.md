# Architecture Document: Lenny Growth Assistant

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                        │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │     HTML/CSS    │  │   JavaScript    │                   │
│  │                 │  │                 │                   │
│  │  Chat Interface │  │   API Client    │                   │
│  │  Artifact View  │  │  State Manager  │                   │
│  │  Settings Panel │  │   Event Handler │                   │
│  └─────────────────┘  └─────────────────┘                   │
└───────────────────────────────┬─────────────────────────────┘
                                │ HTTP/HTTPS
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │   API Gateway   │  │   Business      │                   │
│  │                 │  │    Logic        │                   │
│  │  Routing Layer  │  │   RAG System    │                   │
│  │  Auth Middleware│  │   LLM Service   │                   │
│  │  Error Handling │  │   Database      │                   │
│  └─────────────────┘  └─────────────────┘                   │
└───────────────────────────────┬─────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │   FAISS     │ │   Groq      │ │   Supabase  │
        │   Index     │ │    API      │ │  Database   │
        │             │ │             │ │             │
        │ Transcript  │ │  Llama 3.3  │ │ Chat History│
        │  Vectors    │ │   70B       │ │  Sessions   │
        └─────────────┘ └─────────────┘ └─────────────┘
```

## Component Architecture

### 1. Frontend Layer

#### HTML Structure
- Single-page application
- Three-column layout
- Semantic markup
- Responsive design

#### CSS Architecture
- Component-based styling
- CSS variables for theming
- Mobile-first approach
- Animation system

#### JavaScript Architecture
- Module pattern for organization
- Event-driven architecture
- Promise-based API calls
- Local state management

### 2. Backend Layer

#### FastAPI Application
```python
# Application Structure
app/
├── main.py              # Entry point
├── api/                 # API endpoints
│   ├── chat.py          # Chat endpoints
│   ├── sessions.py      # Session management
│   └── artifacts.py     # Artifact generation
├── services/            # Business logic
│   ├── rag.py           # RAG service
│   ├── llm.py           # LLM service
│   └── database.py      # Database service
├── models/              # Data models
│   ├── chat.py          # Chat models
│   ├── session.py       # Session models
│   └── artifact.py      # Artifact models
└── utils/               # Utilities
    ├── helpers.py       # Helper functions
    └── validators.py    # Input validation
```

#### API Design
- RESTful endpoints
- JSON request/response
- Proper status codes
- Error standardization

### 3. Data Layer

#### Vector Storage (FAISS)
- Sentence transformer embeddings
- Cosine similarity search
- Chunk-based indexing
- Batch updates

#### Relational Storage (Supabase)
- Session management
- Message history
- User preferences (future)
- Analytics data (future)

#### External Services
- Groq API for LLM
- Ollama for local LLM
- Supabase for database

## Data Flow

### 1. Chat Request Flow
```
1. User → Frontend → POST /chat
2. FastAPI → Request Validation
3. FastAPI → RAG Service → FAISS Search
4. RAG Service → Context Retrieval
5. FastAPI → LLM Service → Response Generation
6. LLM Service → Groq/Ollama API
7. FastAPI → Database Service → Save Message
8. FastAPI → Response to Frontend
9. Frontend → Display Response
10. Frontend → Show Artifact (if applicable)
```

### 2. RAG Pipeline
```
1. Query → Sentence Transformer → Embedding
2. Embedding → FAISS Index → Similarity Search
3. Search Results → Document Retrieval
4. Documents → Context Assembly
5. Context → Prompt Engineering
6. Prompt → LLM → Response
```

### 3. Artifact Generation Flow
```
1. User Request → Type Detection
2. Context → RAG Retrieval
3. Prompt → Artifact-Specific Template
4. LLM → Structured Output
5. Output → Format Validation
6. Validation → Response Packaging
```

## Integration Points

### 1. Groq API Integration
- Authentication via API key
- Model selection (Llama 3.3, 8B, Gemma 2)
- Rate limiting and retries
- Error handling

### 2. Ollama Integration
- Local HTTP API
- Model management
- Connection pooling
- Fallback strategies

### 3. Supabase Integration
- PostgreSQL connection
- Session management
- Message storage
- Real-time updates (future)

### 4. FAISS Integration
- Index loading/creation
- Vector similarity search
- Memory management
- Batch processing

## Security Architecture

### Authentication & Authorization
- API key management
- Session validation
- Rate limiting
- Input sanitization

### Data Security
- Environment variable storage
- HTTPS enforcement
- SQL injection prevention
- XSS protection

### Privacy Considerations
- Transcript data handling
- User message storage
- Data retention policies
- GDPR compliance (future)

## Scalability Design

### Horizontal Scaling
- Stateless backend
- Database connection pooling
- Load balancing ready
- CDN for static assets

### Performance Optimization
- Caching strategies
- Database indexing
- Async operations
- Connection reuse

### Monitoring & Observability
- Request logging
- Error tracking
- Performance metrics
- Usage analytics

## Deployment Architecture

### Development Environment
- Local Python environment
- Node.js for frontend
- Supabase local (future)
- Docker containers (optional)

### Production Environment
```
┌────────────────────────────────────────────────────────────��┐
│                      Load Balancer                          │
│                         (Nginx)                             │
└─────────────────────────────┬───────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │   FastAPI   │ │   FastAPI   │ │   FastAPI   │
        │   Instance  │ │   Instance  │ │   Instance  │
        │     #1      │ │     #2      │ │     #3      │
        └─────────────┘ └─────────────┘ └─────────────┘
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   (Supabase)    │
                    └─────────────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │   Groq      │ │   FAISS     │ │   S3/Cloud  │
        │    API      │ │   Index     │ │   Storage   │
        └─────────────┘ └─────────────┘ └─────────────┘
```

## Technology Choices

### Backend (FastAPI)
- **Why**: Async support, automatic docs, Python ecosystem
- **Alternatives**: Flask, Django, Express.js
- **Decision**: Best for AI/ML integration, fast development

### Frontend (Vanilla JS)
- **Why**: Simple, no build step, fast loading
- **Alternatives**: React, Vue, Svelte
- **Decision**: Minimal complexity for MVP

### Vector Database (FAISS)
- **Why**: Fast similarity search, Python native
- **Alternatives**: Pinecone, Weaviate, Qdrant
- **Decision**: Local, free, integrates with transformers

### LLM Provider (Groq)
- **Why**: Fast inference, free tier, Llama 3.3
- **Alternatives**: OpenAI, Anthropic, local models
- **Decision**: Best free option for quality/speed

### Database (Supabase)
- **Why**: PostgreSQL, real-time, free tier
- **Alternatives**: Firebase, MongoDB, SQLite
- **Decision**: SQL familiarity, generous free tier

## Development Guidelines

### Code Structure
- Modular design
- Single responsibility
- Dependency injection
- Configuration management

### Testing Strategy
- Unit tests for services
- Integration tests for APIs
- End-to-end tests for flows
- Performance testing

### Documentation
- API documentation (OpenAPI)
- Code comments
- Architecture diagrams
- Deployment guides