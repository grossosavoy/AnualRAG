from pypdf import PdfReader, PdfWriter

def extract_first_n_pages(input_pdf, output_pdf, num_pages=130):
    """
    Extracts the first `num_pages` pages from a PDF and saves them as a new file.

    Args:
        input_pdf (str): Path to the original PDF.
        output_pdf (str): Path to save the new PDF.
        num_pages (int): Number of pages to extract (default: 30).
    """
    # Open the original PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Add the first `num_pages` pages
    for i in range(min(num_pages, len(reader.pages))):  # Ensure we don't exceed total pages
        writer.add_page(reader.pages[i])

    # Save the new PDF
    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"✅ Extracted first {num_pages} pages and saved to: {output_pdf}")
