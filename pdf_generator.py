from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf(role, ai_prediction, ats_score, matched, missing, suggestions):

    file_path = "resume_report.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)

    y = 750

    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, y, "AI Resume Analysis Report")

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

    c.save()

    return file_path
