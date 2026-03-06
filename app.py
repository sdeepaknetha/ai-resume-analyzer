from flask import Flask, render_template, request
from resume_parser import extract_text_from_resume
import json

app = Flask(__name__)

with open("job_roles.json") as f:
    job_roles = json.load(f)

def generate_suggestion(skill):
    suggestions = {
        "node": "Learn Node.js for backend development",
        "django": "Learn Django for Python web development",
        "machine learning": "Study Machine Learning using Scikit-Learn",
        "data analysis": "Learn Pandas and NumPy for data analysis",
        "git": "Learn Git and GitHub for version control",
        "docker": "Learn Docker for containerization"
    }

    return suggestions.get(skill.lower(), f"Consider learning {skill}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]

    text = extract_text_from_resume(file)

    best_role = "Unknown"
    best_score = 0
    missing_skills = []

    for role in job_roles:

        skills = job_roles[role]

        score = sum(1 for skill in skills if skill.lower() in text.lower())

        if score > best_score:
            best_score = score
            best_role = role
            missing_skills = [s for s in skills if s.lower() not in text.lower()]

    match_score = int((best_score / len(job_roles[best_role])) * 100)

    suggestions = [generate_suggestion(skill) for skill in missing_skills]

    return render_template(
        "result.html",
        role=best_role,
        score=match_score,
        missing=missing_skills,
        suggestions=suggestions
    )

if __name__ == "__main__":
    app.run(debug=True)
