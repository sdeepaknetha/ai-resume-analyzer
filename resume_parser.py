import json
import nltk
from nltk.tokenize import word_tokenize

# Download tokenizer safely
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load job roles
with open("job_roles.json") as f:
    JOB_ROLES = json.load(f)


def analyze_resume(text):

    tokens = word_tokenize(text.lower())

    best_role = None
    best_score = 0
    best_skills = []
    missing_skills = []

    for role, skills in JOB_ROLES.items():

        found = []

        for skill in skills:
            if skill.lower() in tokens:
                found.append(skill)

        score = int((len(found) / len(skills)) * 100)

        if score > best_score:
            best_score = score
            best_role = role
            best_skills = found
            missing_skills = list(set(skills) - set(found))

    return {
        "score": best_score,
        "role": best_role,
        "skills": best_skills,
        "missing": missing_skills
    }
