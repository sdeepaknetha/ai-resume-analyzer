from flask import Flask, render_template, request
from resume_parser import extract_text_from_resume
import json

app = Flask(__name__)

with open("job_roles.json") as f:
    job_roles = json.load(f)


def generate_suggestion(skill):

    suggestions = {
        "node": "Learn Node.js for backend development",
        "django": "Learn Django framework",
        "machine learning": "Study Machine Learning",
        "data analysis": "Learn Pandas and NumPy",
        "git": "Learn Git and GitHub"
    }

    return suggestions.get(skill.lower(), f"Consider learning {skill}")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]

    text = extract_text_from_resume(file)

    best_role = ""
    best_score = 0
    missing_skills = []
    matched_skills = []

    for role in job_roles:

        skills = job_roles[role]

        matches = [skill for skill in skills if skill.lower() in text]

        score = len(matches)

        if score > best_score:
            best_score = score
            best_role = role
            matched_skills = matches
            missing_skills = [s for s in skills if s not in matches]

    total = len(job_roles[best_role])

    match_score = int((best_score / total) * 100)

    ats_score = match_score + 10

    if ats_score > 100:
    ats_score = 100

    suggestions = [generate_suggestion(s) for s in missing_skills]

    return render_template(
    "result.html",
    role=best_role,
    score=match_score,
    ats_score=ats_score,
    matched=matched_skills,
    missing=missing_skills,
    suggestions=suggestions
    )
    


if __name__ == "__main__":
    app.run()


