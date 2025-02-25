import faiss
import numpy as np
from pathlib import Path
from embeddings import generate_embeddings

def search_faiss(query, faiss_index_path, chunks, top_k=5):
    """
    Search the FAISS vector database for similar text chunks.
    
    Args:
        query (str): The user's query.
        faiss_index_path (str): Path to the FAISS index file.
        chunks (list): List of text chunks.
        top_k (int): Number of results to retrieve.

    Returns:
        list: Matching text chunks.
    """
    if not Path(faiss_index_path).exists():
        print("❌ FAISS index file not found!")
        return []

    print(f"🔍 Searching for: {query}")

    # Load FAISS index
    index = faiss.read_index(str(faiss_index_path))

    # Convert query to embedding
    query_embedding = generate_embeddings([query])  # Returns a NumPy array

    # Perform search
    D, I = index.search(query_embedding, k=top_k)  # Search for top_k results

    # Retrieve matching chunks
    matched_chunks = [chunks[i] for i in I[0] if i < len(chunks)]
    
    return matched_chunks

def store_embeddings(embeddings, output_folder="parsed"):
    """
    Store embeddings in a FAISS vector database.
    
    Args:
        embeddings (np.ndarray): NumPy array of embeddings.
        output_folder (str): Path to store the FAISS index.
    
    Returns:
        str: Path to saved FAISS index.
    """
    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True)

    faiss_index_path = output_folder / "faiss_index.bin"

    # Get the embedding dimension
    dimension = embeddings.shape[1]

    # Create FAISS index with L2 (Euclidean) distance
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save the index
    faiss.write_index(index, str(faiss_index_path))

    print(f"✅ Stored {embeddings.shape[0]} embeddings in FAISS at: {faiss_index_path}")
    return faiss_index_path
