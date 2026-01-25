from pypdf import PdfReader
import os


def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def load_document(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return load_txt(file_path)
    elif ext == ".pdf":
        return load_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")



