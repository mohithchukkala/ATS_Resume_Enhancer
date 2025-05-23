import fitz  # PyMuPDF
import docx
# AIzaSyCU6AUNuasUZiiwT6PAjLbnflrnfYfNjWM

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])



