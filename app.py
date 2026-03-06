from flask import Flask, render_template, request
import pdfplumber
import docx

app = Flask(__name__)

roles = {
    "Web Developer": ["html","css","javascript","react","node","git","bootstrap"],
    "Data Scientist": ["python","pandas","numpy","machine learning","statistics","deep learning","data visualization"]
}

def extract_text(file):
    text = ""

    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()

    elif file.filename.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text

    return text.lower()


def analyze_resume(text):

    best_role = ""
    best_score = 0
    missing_skills = []

    for role, skills in roles.items():

        found = [skill for skill in skills if skill in text]
        score = int((len(found) / len(skills)) * 100)

        if score > best_score:
            best_score = score
            best_role = role
            missing_skills = list(set(skills) - set(found))

    suggestions = []
    for skill in missing_skills:
        suggestions.append(f"Learn {skill} to improve your profile")

    return best_role, best_score, missing_skills, suggestions


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]

    text = extract_text(file)

    role, score, missing, suggestions = analyze_resume(text)

    return render_template(
        "result.html",
        role=role,
        score=score,
        missing=missing,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)
