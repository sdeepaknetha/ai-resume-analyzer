from flask import Flask, render_template, request
import json
from resume_parser import extract_text_from_resume
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

    text = extract_text_from_resume(file).lower()

    best_role = "None"
    best_score = 0
    best_missing = []
    role_scores = {}

    for role, skills in job_roles.items():

        matched = 0

        for skill in skills:
            if skill.lower() in text:
                matched += 1

        score = int((matched / len(skills)) * 100)

        role_scores[role] = score

        if score > best_score:
            best_score = score
            best_role = role
            best_missing = [s for s in skills if s.lower() not in text]

    # Sort roles for recommendation
    sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)

    recommendations = [r[0] for r in sorted_roles[1:3]]

    return render_template(
        "result.html",
        role=best_role,
        score=best_score,
        missing=best_missing,
        recommendations=recommendations
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
