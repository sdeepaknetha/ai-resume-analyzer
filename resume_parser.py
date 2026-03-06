import pdfplumber
import docx


def extract_text_from_resume(file):

    text = ""

    if file.filename.endswith(".pdf"):

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text()

    elif file.filename.endswith(".docx"):

        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text

    return text.lower()
