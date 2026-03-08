from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from chart_generator import create_skill_chart


def create_pdf(role, ai_prediction, ats_score, matched, missing, suggestions):

    chart_path = create_skill_chart(matched, missing)

    file_path = "resume_report.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)

    y = 750

    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, y, "AI Resume Analysis Report")

    y -= 50

    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Best Matched Role: {role}")
    y -= 25

    c.drawString(50, y, f"AI Model Prediction: {ai_prediction}")
    y -= 25

    c.drawString(50, y, f"ATS Resume Score: {ats_score}%")
    y -= 40

    c.drawString(50, y, "Matched Skills:")
    y -= 20

    for skill in matched:
        c.drawString(70, y, f"- {skill}")
        y -= 15

    y -= 20
    c.drawString(50, y, "Missing Skills:")
    y -= 20

    for skill in missing:
        c.drawString(70, y, f"- {skill}")
        y -= 15

    y -= 20
    c.drawString(50, y, "Suggestions:")
    y -= 20

    for s in suggestions:
        c.drawString(70, y, f"- {s}")
        y -= 15

    y -= 40

    # Insert chart image
    c.drawImage(chart_path, 150, y - 200, width=300, height=200)

    c.save()

    return file_path
