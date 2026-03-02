import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------- Load Job Roles --------
def load_job_roles():
    with open("job_roles.json", "r") as file:
        return json.load(file)


# -------- Match Resume --------
def match_resume(resume_text):
    job_roles = load_job_roles()

    roles = list(job_roles.keys())
    descriptions = list(job_roles.values())

    documents = descriptions + [resume_text]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    best_match_index = similarity.argmax()
    best_match_role = roles[best_match_index]
    match_score = round(similarity[0][best_match_index] * 100, 2)

    # -------- Professional Skill Matching --------
    skill_keywords = [
        "python",
        "flask",
        "django",
        "sql",
        "sqlite",
        "machine learning",
        "api",
        "object oriented programming"
    ]

    resume_text_lower = resume_text.lower()

    missing_skills = [
        skill for skill in skill_keywords
        if skill in descriptions[best_match_index].lower()
        and skill not in resume_text_lower
    ]

    return best_match_role, match_score, missing_skills