import PyPDF2
import docx
import os

def parse_cv(file_path: str) -> str:
    """PDF ya Word CV se text extract karta hai"""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        return parse_docx(file_path)
    else:
        raise ValueError("Sirf PDF ya Word file upload karo!")

def parse_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text.strip()

def parse_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text.strip()
