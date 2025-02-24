from pathlib import Path
from docling.document_converter import DocumentConverter

def extract_text(source_pdf, output_folder="parsed"):
    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True)
    output_markdown = output_folder / "output.md"

    converter = DocumentConverter()
    result = converter.convert(source_pdf)

    if result and hasattr(result, "document") and result.document:
        result.document.save_as_markdown(output_markdown, strict_text=True, escaping_underscores=False)
        print(f"✅ Markdown file saved at: {output_markdown}")
        return output_markdown
    else:
        print("❌ Error: Document conversion failed.")
        return None