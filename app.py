from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

# Load job roles
with open("job_roles.json", "r") as f:
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

    # Read resume text
    text = file.read().decode("utf-8")

    best_role = "None"
    best_score = 0
    missing_skills = []

    for role in job_roles:
        skills = job_roles[role]

        score = sum(1 for skill in skills if skill.lower() in text.lower())

        if score > best_score:
            best_score = score
            best_role = role
            missing_skills = [s for s in skills if s.lower() not in text.lower()]

    if best_role != "None":
        match_score = int((best_score / len(job_roles[best_role])) * 100)
    else:
        match_score = 0

    return render_template(
        "result.html",
        role=best_role,
        score=match_score,
        missing=missing_skills
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
