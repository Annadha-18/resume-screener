import PyPDF2
import docx
import os

def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return _extract_from_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        return _extract_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def _extract_from_pdf(path: str) -> str:
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text.strip()

def _extract_from_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def extract_text_from_bytes(file_bytes, filename: str) -> str:
    import tempfile
    suffix = os.path.splitext(filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    text = extract_text(tmp_path)
    os.unlink(tmp_path)
    return text