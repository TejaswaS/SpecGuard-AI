import pymupdf

def extract_pdf_text(files_bytes):
    
    # Extract text from every page of a PDF.

    # Returns:
    #     List of dictionaries containing page number and text.
    
    document = pymupdf.open(stream = files_bytes, filetype = "pdf")

    pages = []
    for page_number, page in enumerate(document, start = 1):
        text = page.get_text("text")
        pages.append({
            "page": page_number,
            "text": text
        })
    document.close()
    return pages
