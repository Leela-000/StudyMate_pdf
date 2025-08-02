import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file,max_chars=3000):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
        if len(text) > max_chars:
            break
    return text[:max_chars]
