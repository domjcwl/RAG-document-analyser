from pypdf import PdfReader
import os



#CREATING A FUNCTION TO CHOOSE WHICH FILE TO LOAD (.pdf/.txt)
def load_document(file_path: str) -> str:
    #stores the ending(.pdf or .txt) into ext to handle files that are supported/unsupported
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return load_txt(file_path)
    elif ext == ".pdf":
        return load_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


#CREATING FUNCTION FOR LOADING PDF FILE
def load_pdf(file_path: str) -> str:  #creating function to read .pdf file
    #creating a reader object that contains the pdf information
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() #extracting readable text out of each page in the page object
        if page_text: #handles situations where page_text contains empty string. returns False. for e.g., sometimes, extract_text returns None. hence page_txt = None.
            text += page_text + "\n"
    print(text)




#CREATING FUNCTION FOR LOADING TXT FILE
def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    print(text)



#RUN load_txt FUNCTION WHEN loaders.py IS RUN
if __name__ == "__main__":
    file_path = input("File Path: ")
    file_path = file_path.strip().replace('"', '').replace("'", "")
    load_document(file_path)


