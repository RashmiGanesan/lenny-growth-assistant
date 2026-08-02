import os
import pickle
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from sentence_transformers import SentenceTransformer

class RAGSystem:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize RAG system with FAISS and sentence transformer"""
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.document_metadata = {}
        self.is_loaded = False
        
    def load_index(self, index_path: str, documents_path: str):
        """Load FAISS index and associated documents"""
        try:
            # Load FAISS index
            import faiss
            self.index = faiss.read_index(index_path)
            
            # Load documents with metadata
            with open(documents_path, 'rb') as f:
                data = pickle.load(f)
            
            # Handle both old format (list of strings) and new format (dict with metadata)
            if isinstance(data, dict):
                self.documents = data.get('chunks', [])
                self.document_metadata = data
            else:
                self.documents = data
                self.document_metadata = {'chunks': data}
            
            self.is_loaded = True
            total_docs = len(self.documents)
            print(f"✅ Loaded FAISS index with {total_docs} document chunks")
            return True
            
        except Exception as e:
            print(f"❌ Error loading index: {e}")
            self.is_loaded = False
            return False
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant document chunks with metadata"""
        if not self.is_loaded:
            print("⚠️  FAISS index not loaded. Please create index first.")
            return []
        
        try:
            # Encode query
            query_embedding = self.model.encode([query]).astype('float32')
            
            # Search FAISS index
            distances, indices = self.index.search(query_embedding, top_k)
            
            # Retrieve documents with metadata
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if 0 <= idx < len(self.documents):
                    result = {
                        'text': self.documents[idx],
                        'distance': float(distance),
                        'index': int(idx),
                        'source': self.document_metadata.get('sources', [])[idx] if 'sources' in self.document_metadata else 'Unknown'
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"❌ Error searching index: {e}")
            return []
    
    def get_relevant_context(self, query: str, top_k: int = 5) -> str:
        """Get formatted context from search results for LLM processing"""
        results = self.search(query, top_k)
        
        if not results:
            return "No relevant context found in the transcripts."
        
        # Format context with detailed structure for better LLM comprehension
        context_parts = []
        
        # Start with a summary of what was found
        context_parts.append(f"RELEVANT TRANSCRIPT EXTRACTS FOR: '{query}'")
        context_parts.append("=" * 60)
        
        for i, result in enumerate(results):
            source_file = result.get('source', 'Unknown Transcript').replace('_', ' ').replace('.txt', '')
            relevance_score = 1.0 - result['distance']  # Convert distance to similarity
            similarity_percent = round(relevance_score * 100, 1)
            
            context_text = result['text'].strip()
            
            # Format with clear structure
            context_parts.append(f"\n📄 EXTRACT {i+1} (Similarity: {similarity_percent}% | Source: {source_file}):")
            context_parts.append("-" * 40)
            context_parts.append(context_text)
        
        # Add metadata about the search
        context_parts.append(f"\n📊 Search Summary: Found {len(results)} relevant excerpts from transcripts.")
        
        return "\n".join(context_parts)
    
    def get_detailed_context(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Get detailed search results including metadata"""
        results = self.search(query, top_k)
        
        return {
            'query': query,
            'total_results': len(results),
            'results': results,
            'is_loaded': self.is_loaded
        }

# Example usage
if __name__ == "__main__":
    # This is a test script to verify the RAG system
    rag = RAGSystem()
    
    # Get absolute paths for test
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_index_path = os.path.join(base_dir, "../data/faiss_index/index.faiss")
    test_documents_path = os.path.join(base_dir, "../data/faiss_index/documents.pkl")
    
    if os.path.exists(test_index_path) and os.path.exists(test_documents_path):
        success = rag.load_index(test_index_path, test_documents_path)
        if success:
            # Test search
            test_queries = [
                "How do startups grow?",
                "What is product market fit?",
                "Airbnb growth strategy",
                "Founder challenges"
            ]
            
            for query in test_queries:
                print(f"\n🔍 Query: '{query}'")
                context = rag.get_relevant_context(query)
                print(f"📝 Context:\n{context[:300]}...")
                
                # Get detailed results
                details = rag.get_detailed_context(query)
                print(f"📊 Results: {details['total_results']} found")
    else:
        print("FAISS index not found. Please run:")
        print("python create_faiss_index.py")