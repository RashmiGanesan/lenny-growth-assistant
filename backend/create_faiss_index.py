#!/usr/bin/env python3
"""
FAISS Index Creation Script for Lenny Growth Assistant

This script:
1. Reads all .txt transcript files from data/transcripts/
2. Splits transcripts into meaningful chunks (500 tokens with overlap)
3. Generates embeddings using SentenceTransformer all-MiniLM-L6-v2
4. Creates a FAISS vector index
5. Saves index and documents to data/faiss_index/
"""

import os
import sys
import pickle
import re
from typing import List, Tuple
import numpy as np

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import faiss
    from sentence_transformers import SentenceTransformer
    from sentence_transformers.util import cos_sim
except ImportError as e:
    print(f"Missing required packages: {e}")
    print("Install with: pip install faiss-cpu sentence-transformers")
    sys.exit(1)


def get_transcript_files(transcripts_dir: str) -> List[str]:
    """Get all .txt files from transcripts directory"""
    transcript_files = []
    
    if not os.path.exists(transcripts_dir):
        print(f"Transcripts directory not found: {transcripts_dir}")
        return transcript_files
    
    for filename in os.listdir(transcripts_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(transcripts_dir, filename)
            transcript_files.append(filepath)
    
    return transcript_files


def read_transcript_file(filepath: str) -> str:
    """Read and clean transcript file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Clean content - remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        return content
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return ""


def split_into_chunks(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Split text into chunks of approximately chunk_size tokens with overlap.
    Simple whitespace-based splitting for demonstration.
    """
    if not text:
        return []
    
    # Split by sentences for better chunk boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        words = sentence.split()
        sentence_length = len(words)
        
        if current_length + sentence_length > chunk_size and current_chunk:
            # Save current chunk
            chunks.append(' '.join(current_chunk))
            
            # Start new chunk with overlap
            overlap_words = current_chunk[-overlap:] if overlap < len(current_chunk) else current_chunk
            current_chunk = overlap_words
            current_length = len(overlap_words)
        
        current_chunk.append(sentence)
        current_length += sentence_length
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def create_embeddings(text_chunks: List[str], model: SentenceTransformer) -> np.ndarray:
    """Create embeddings for all text chunks"""
    if not text_chunks:
        return np.array([])
    
    print(f"Creating embeddings for {len(text_chunks)} chunks...")
    
    # Encode all chunks in batches for efficiency
    embeddings = model.encode(text_chunks, show_progress_bar=True)
    
    return np.array(embeddings).astype('float32')


def create_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """Create FAISS index with L2 distance metric"""
    if len(embeddings) == 0:
        raise ValueError("No embeddings to index")
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    return index


def create_index(transcripts_dir: str, save_dir: str, model_name: str = "all-MiniLM-L6-v2") -> Tuple[bool, str]:
    """
    Main function to create FAISS index from transcripts
    Returns: (success, message)
    """
    print("=" * 60)
    print("Creating FAISS Index for Lenny Growth Assistant")
    print("=" * 60)
    
    # Check directories
    if not os.path.exists(transcripts_dir):
        return False, f"Transcripts directory not found: {transcripts_dir}"
    
    os.makedirs(save_dir, exist_ok=True)
    
    # Get transcript files
    transcript_files = get_transcript_files(transcripts_dir)
    
    if not transcript_files:
        return False, f"No .txt files found in {transcripts_dir}"
    
    print(f"Found {len(transcript_files)} transcript files:")
    for filepath in transcript_files:
        print(f"  - {os.path.basename(filepath)}")
    
    # Load model
    print(f"\nLoading sentence transformer model: {model_name}")
    model = SentenceTransformer(model_name)
    
    # Read and chunk transcripts
    all_chunks = []
    chunk_sources = []  # Track which file each chunk came from
    
    for filepath in transcript_files:
        content = read_transcript_file(filepath)
        if content:
            filename = os.path.basename(filepath)
            chunks = split_into_chunks(content)
            
            for chunk in chunks:
                all_chunks.append(chunk)
                chunk_sources.append(filename)
            
            print(f"  {filename}: {len(chunks)} chunks")
    
    if not all_chunks:
        return False, "No content found in transcript files"
    
    print(f"\nTotal chunks created: {len(all_chunks)}")
    
    # Create embeddings
    embeddings = create_embeddings(all_chunks, model)
    
    # Create FAISS index
    print("\nCreating FAISS index...")
    index = create_faiss_index(embeddings)
    
    # Save index
    index_path = os.path.join(save_dir, "index.faiss")
    documents_path = os.path.join(save_dir, "documents.pkl")
    
    print(f"\nSaving index to: {index_path}")
    faiss.write_index(index, index_path)
    
    # Save documents with metadata
    document_data = {
        'chunks': all_chunks,
        'sources': chunk_sources,
        'total_documents': len(all_chunks),
        'embedding_dimension': embeddings.shape[1]
    }
    
    with open(documents_path, 'wb') as f:
        pickle.dump(document_data, f)
    
    # Test the index
    print("\nTesting the index...")
    test_queries = [
        "How do startups grow?",
        "What is product market fit?",
        "Airbnb growth strategy"
    ]
    
    for query in test_queries:
        query_embedding = model.encode([query]).astype('float32')
        distances, indices = index.search(query_embedding, 1)
        
        if len(indices[0]) > 0:
            idx = indices[0][0]
            if 0 <= idx < len(all_chunks):
                chunk_preview = all_chunks[idx][:150] + "..." if len(all_chunks[idx]) > 150 else all_chunks[idx]
                print(f"  Query: '{query}' -> Found chunk from '{chunk_sources[idx]}'")
    
    print("\n" + "=" * 60)
    print("Index creation complete!")
    print(f"  - Index file: {index_path}")
    print(f"  - Documents file: {documents_path}")
    print(f"  - Total chunks indexed: {len(all_chunks)}")
    print(f"  - Embedding dimension: {embeddings.shape[1]}")
    print("=" * 60)
    
    return True, "Index created successfully"


def main():
    """Main function with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create FAISS index from transcripts')
    parser.add_argument('--transcripts-dir', default='../data/transcripts',
                       help='Directory containing transcript files (default: ../data/transcripts)')
    parser.add_argument('--save-dir', default='../data/faiss_index',
                       help='Directory to save FAISS index (default: ../data/faiss_index)')
    parser.add_argument('--model', default='all-MiniLM-L6-v2',
                       help='SentenceTransformer model name (default: all-MiniLM-L6-v2)')
    
    args = parser.parse_args()
    
    # Get absolute paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    transcripts_dir = os.path.join(base_dir, args.transcripts_dir)
    save_dir = os.path.join(base_dir, args.save_dir)
    
    # Create index
    success, message = create_index(transcripts_dir, save_dir, args.model)
    
    if success:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()