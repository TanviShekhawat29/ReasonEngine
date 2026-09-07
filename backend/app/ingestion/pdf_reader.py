import fitz


def extract_text_from_pdf(pdf_path: str) -> dict:
    """
    Extract text from every page of a PDF.
    """

    document = fitz.open(pdf_path)

    total_pages = len(document)

    extracted_text = []

    for page in document:
        extracted_text.append(page.get_text())

    document.close()

    final_text = "\n".join(extracted_text)

    return {
        "pages": total_pages,
        "characters": len(final_text),
        "text": final_text
    }