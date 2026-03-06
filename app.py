from flask import Flask, render_template, request
from resume_parser import extract_text_from_resume
import json
import os

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
        return "No selected file"

    text = extract_text_from_resume(file)

    best_role = None
    best_score = 0
    missing_skills = []

    for role, skills in job_roles.items():

        matched = []

        for skill in skills:
            if skill.lower() in text.lower():
                matched.append(skill)

        score = int((len(matched) / len(skills)) * 100)

        if score > best_score:
            best_score = score
            best_role = role
            missing_skills = list(set(skills) - set(matched))

    if best_role is None:
        best_role = "No Match Found"

    return render_template(
        "result.html",
        role=best_role,
        score=best_score,
        missing=missing_skills
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
