import ollama
import numpy as np

def generate_embeddings(chunks, model_name="nomic-embed-text"):
    """
    Generate embeddings using Ollama's local embedding model.
    
    Args:
        chunks (list): List of text chunks.
        model_name (str): Name of the Ollama embedding model.
    
    Returns:
        np.ndarray: Embeddings as a NumPy array.
    """
    print(f"🔹 Using Ollama to generate embeddings with model: {model_name}")

    embeddings = []
    for chunk in chunks:
        response = ollama.embeddings(model=model_name, prompt=chunk)
        embeddings.append(response["embedding"])  # Extract the embedding vector

    embedding_matrix = np.array(embeddings)

    print(f"✅ Ollama embeddings generated successfully! Shape: {embedding_matrix.shape}")
    return embedding_matrix
