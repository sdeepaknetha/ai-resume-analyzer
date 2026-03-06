def extract_text_from_resume(file):

    try:
        content = file.read()

        try:
            text = content.decode("utf-8")
        except:
            text = content.decode("latin-1")

        return text.lower()

    except Exception as e:
        print("Error reading file:", e)
        return ""
