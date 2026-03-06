import io

def extract_text_from_resume(file):

    try:
        text = file.read().decode("utf-8")
        return text

    except:
        return ""
