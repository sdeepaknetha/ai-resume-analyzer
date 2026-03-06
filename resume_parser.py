def extract_text_from_resume(file):

    try:
        file_content = file.read()

        # Try UTF-8 decoding
        try:
            text = file_content.decode("utf-8")
        except:
            text = file_content.decode("latin-1")

        return text.lower()

    except Exception as e:
        print("Error reading resume:", e)
        return ""
