from flask import Flask, render_template, request
import json

from resume_parser import extract_text_from_resume
from model import predict_role
from keyword_extractor import extract_keywords
from resume_feedback import generate_feedback

app = Flask(__name__)

# Load job roles
with open("job_roles.json") as f:
    job_roles = json.load(f)


# Suggestion generator
def generate_suggestion(skill):

    suggestions = {
        "node": "Learn Node.js for backend development",
        "django": "Learn Django framework",
        "machine learning": "Study Machine Learning basics",
        "data analysis": "Learn Pandas and NumPy",
        "git": "Learn Git and GitHub",
        "bootstrap": "Learn Bootstrap for responsive design"
    }

    return suggestions.get(skill.lower(), f"Consider learning {skill}")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]

    text = extract_text_from_resume(file)

    role_scores = []

    for role in job_roles:

        skills = job_roles[role]

        matches = [skill for skill in skills if skill.lower() in text]

        score = len(matches)

        total_skills = len(skills)

        percent = int((score / total_skills) * 100)

        missing = [s for s in skills if s not in matches]

        role_scores.append((role, percent, matches, missing))

    role_scores.sort(key=lambda x: x[1], reverse=True)

    best_role, match_score, matched_skills, missing_skills = role_scores[0]

    top_roles = role_scores[:3]

    ats_score = match_score + 10

    if ats_score > 100:
        ats_score = 100

    suggestions = [generate_suggestion(s) for s in missing_skills]

    # Machine Learning prediction
    ai_prediction = predict_role(text)

    # Keyword extraction
    keywords = extract_keywords(text)

    # Resume feedback
    feedback = generate_feedback(missing_skills)

    return render_template(
        "result.html",
        role=best_role,
        score=match_score,
        ats_score=ats_score,
        matched=matched_skills,
        missing=missing_skills,
        suggestions=suggestions,
        top_roles=top_roles,
        ai_prediction=ai_prediction,
        keywords=keywords,
        feedback=feedback
    )


if __name__ == "__main__":
    app.run(debug=True)
