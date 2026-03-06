import pdfplumber
import docx


def extract_text_from_resume(file):

    filename = file.filename.lower()

    # PDF
    if filename.endswith(".pdf"):

        text = ""

        with pdfplumber.open(file) as pdf:

            for page in pdf.pages:
                text += page.extract_text()

        return text

    # DOCX
    elif filename.endswith(".docx"):

        doc = docx.Document(file)

        text = ""

        for para in doc.paragraphs:
            text += para.text

        return text

    else:
        return ""
