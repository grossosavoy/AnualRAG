from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(markdown_file, chunk_size=500, chunk_overlap=50):
    with open(markdown_file, "r", encoding="utf-8") as f:
        text = f.read()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)

    print(f"✅ Total Chunks Created: {len(chunks)}")
    return chunks
