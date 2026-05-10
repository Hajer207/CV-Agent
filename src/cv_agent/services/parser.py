import re
import pypdf
from docx import Document


def _clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def parse_pdf(file_path: str) -> str:
    reader = pypdf.PdfReader(file_path)
    text = " ".join(page.extract_text() or "" for page in reader.pages)
    return _clean_text(text)


def parse_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = " ".join(para.text for para in doc.paragraphs)
    return _clean_text(text)


def parse_cv(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.endswith(".docx"):
        return parse_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
