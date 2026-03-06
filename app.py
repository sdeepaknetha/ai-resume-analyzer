from flask import Flask, render_template, request
import os
import json
import pdfplumber
import docx

app = Flask(__name__)

# Load job roles
with open("job_roles.json") as f:
    job_roles = json.load(f)


# Extract text from resume
def extract_text(file):

    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif filename.endswith(".docx"):
        doc = docx.Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text
        return text

    else:
        return ""


# AI suggestions
def generate_suggestions(missing_skills):

    suggestions = []

    for skill in missing_skills:

        if skill == "node":
            suggestions.append("Learn Node.js for backend development")

        elif skill == "javascript":
            suggestions.append("Practice JavaScript projects")

        elif skill == "git":
            suggestions.append("Learn Git and upload projects to GitHub")

        elif skill == "machine learning":
            suggestions.append("Study Machine Learning using Python")

        elif skill == "pandas":
            suggestions.append("Learn Pandas for data analysis")

        elif skill == "numpy":
            suggestions.append("Learn NumPy for numerical computing")

        elif skill == "data visualization":
            suggestions.append("Learn Matplotlib or Seaborn")

        elif skill == "statistics":
            suggestions.append("Study Statistics for data science")

        else:
            suggestions.append(f"Learn {skill}")

    return suggestions


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "No file selected"

    text = extract_text(file).lower()

    best_role = "None"
    best_score = 0
    missing_skills = []

    for role in job_roles:

        skills = job_roles[role]

        score = sum(1 for skill in skills if skill.lower() in text)

        if score > best_score:
            best_score = score
            best_role = role
            missing_skills = [s for s in skills if s.lower() not in text]

    match_score = int((best_score / len(job_roles[best_role])) * 100) if best_role != "None" else 0

    suggestions = generate_suggestions(missing_skills)

    return render_template(
        "result.html",
        role=best_role,
        score=match_score,
        missing=missing_skills,
        suggestions=suggestions
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
