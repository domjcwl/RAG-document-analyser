from pypdf import PdfReader #use this library to extract text from pdf files
import os


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text: #only add text if it's value is not None
            text += page_text + "\n"

    return text


def load_document(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower() #get file extension in lowercase .pdf, .txt, .docx etc

    if ext == ".pdf":
        return load_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")



