import pdfplumber
import docx

def extract_text_from_resume(file):

    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text

    elif filename.endswith(".docx"):
        doc = docx.Document(file)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text

    else:
        return file.read().decode("utf-8")
