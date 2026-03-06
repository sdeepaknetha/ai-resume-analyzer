import json
import re
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# -------------------------------
# DOWNLOAD NLTK DATA (Cloud Safe)
# -------------------------------

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# -------------------------------
# LOAD JOB ROLES FROM JSON
# -------------------------------

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
json_path = os.path.join(BASE_DIR, "job_roles.json")

with open(json_path, "r", encoding="utf-8") as file:
    JOB_ROLES = json.load(file)

# -------------------------------
# CLEAN TEXT FUNCTION
# -------------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered = [word for word in tokens if word not in stop_words]
    return filtered

# -------------------------------
# MATCH RESUME FUNCTION
# -------------------------------

def match_resume(resume_text):
    tokens = clean_text(resume_text)
    resume_words = set(tokens)

    best_role = None
    best_score = 0
    missing_skills = []

    for role, skills in JOB_ROLES.items():
        skills_set = set(skill.lower() for skill in skills)

        matched = resume_words.intersection(skills_set)
        score = (len(matched) / len(skills_set)) * 100

        if score > best_score:
            best_score = score
            best_role = role
            missing_skills = list(skills_set - matched)

    best_score = round(best_score, 2)

    # If no missing skills
    if len(missing_skills) == 0:
        missing_skills = ["🎉 No missing skills! Excellent match."]

    return best_role, best_score, missing_skills
