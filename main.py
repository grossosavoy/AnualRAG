from extract import extract_text
from chunker import chunk_text
from embeddings import generate_embeddings
from vector_store import store_embeddings, search_faiss
from pathlib import Path

# Define output folder and markdown file path
output_folder = Path("parsed")
output_markdown = output_folder / "output.md"
faiss_index_path = output_folder / "faiss_index.bin"

# Step 1: Check if Markdown file exists
if output_markdown.exists():
    print(f"✅ Markdown file already exists: {output_markdown}")
else:
    print("🔹 Markdown file not found. Extracting from PDF...")
    pdf_path = "./pdfs/Nykredit_group_anual_report.pdf"
    markdown_file = extract_text(pdf_path)

    if markdown_file is None:
        print("❌ Error: Markdown extraction failed. Exiting.")
        exit()

# Step 2: Chunk text
chunks = chunk_text(output_markdown)

# Step 3: Generate Embeddings using Ollama
embeddings = generate_embeddings(chunks)

# Step 4: Store Embeddings in FAISS
store_embeddings(embeddings, output_folder)

# Step 5: Run Query-Based Retrieval
while True:
    user_query = input("\n🔍 Enter your query (or type 'exit' to quit): ")
    
    if user_query.lower() == "exit":
        print("👋 Exiting search...")
        break
    
    # Retrieve relevant chunks
    results = search_faiss(user_query, faiss_index_path, chunks, top_k=3)

    print("\n🔍 **Top Matching Chunks:**")
    for idx, chunk in enumerate(results, 1):
        print(f"\n📌 **Match {idx}:**")
        print(chunk)
        print("-" * 50)
