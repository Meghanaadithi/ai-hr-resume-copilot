from pypdf import PdfReader

def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text_parts = []
    for page in reader.pages:
        text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts).strip()

