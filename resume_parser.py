import pdfplumber
import docx


def extract_text_from_resume(file):

    filename = file.filename.lower()

    if filename.endswith(".pdf"):

        text = ""

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        return text


    elif filename.endswith(".docx"):

        doc = docx.Document(file)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text


    elif filename.endswith(".txt"):

        return file.read().decode("utf-8")


    else:
        return ""
