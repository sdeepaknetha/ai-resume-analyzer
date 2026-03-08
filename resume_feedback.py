def generate_feedback(missing_skills):

    feedback = []

    for skill in missing_skills:
        feedback.append(f"Consider adding {skill} to improve your resume.")

    if len(missing_skills) == 0:
        feedback.append("Great! Your resume already matches most required skills.")

    return feedback
