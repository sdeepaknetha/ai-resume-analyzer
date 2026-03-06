from flask import Flask, render_template, request
from resume_parser import extract_text_from_resume
import json

app = Flask(__name__)

# Load job roles
with open("job_roles.json") as f:
    job_roles = json.load(f)


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

    # Extract resume text
    text = extract_text_from_resume(file)

    best_role = None
    best_score = 0
    missing_skills = []

    for role in job_roles:

        skills = job_roles[role]

        found = 0
        missing = []

        for skill in skills:

            if skill.lower() in text.lower():
                found += 1
            else:
                missing.append(skill)

        score = int((found / len(skills)) * 100)

        if score > best_score:
            best_score = score
            best_role = role
            missing_skills = missing

    return render_template(
        "result.html",
        role=best_role,
        score=best_score,
        missing=missing_skills
    )


if __name__ == "__main__":
    app.run(debug=True)
