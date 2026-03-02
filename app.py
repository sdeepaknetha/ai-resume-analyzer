from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from resume_parser import match_resume
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

app = Flask(__name__)

# ---------------- DATABASE CONFIG ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resume_data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- DATABASE MODEL ----------------
class ResumeResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    best_role = db.Column(db.String(100))
    match_score = db.Column(db.Float)
    missing_skills = db.Column(db.Text)
    ai_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------- AI SUMMARY FUNCTION ----------------
def generate_summary(role, score, missing):
    if not missing:
        return f"Excellent match for {role}. Your resume covers all required skills."

    if score < 40:
        return f"Low match for {role}. Consider learning: {', '.join(missing)}."
    elif score < 60:
        return f"Good match for {role}, but you can improve by adding: {', '.join(missing)}."
    else:
        return f"Strong profile for {role}. Minor improvements possible in: {', '.join(missing)}."

# ---------------- HOME ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume_file = request.files.get("resume")

        if resume_file:
            resume_text = resume_file.read().decode("utf-8", errors="ignore")

            best_role, score, missing = match_resume(resume_text)
            score = round(score, 2)

            if score < 40:
                color = "red"
            elif score < 60:
                color = "orange"
            else:
                color = "green"

            summary = generate_summary(best_role, score, missing)

            result = ResumeResult(
                best_role=best_role,
                match_score=score,
                missing_skills=", ".join(missing),
                ai_summary=summary
            )

            db.session.add(result)
            db.session.commit()

            return render_template(
                "index.html",
                role=best_role,
                score=score,
                missing=missing,
                color=color,
                summary=summary
            )

    return render_template("index.html")

# ---------------- PROFESSIONAL PDF ROUTE ----------------
@app.route("/download/<int:result_id>")
def download_pdf(result_id):
    result = ResumeResult.query.get_or_404(result_id)

    filename = f"Resume_Report_{result.id}.pdf"
    filepath = os.path.join(os.getcwd(), filename)

    doc = SimpleDocTemplate(filepath)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<font size=18><b>AI Resume Analysis Report</b></font>", styles["Normal"]))
    elements.append(Spacer(1, 0.5 * inch))

    # Role
    elements.append(Paragraph(f"<b>Best Matched Role:</b> {result.best_role}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Score Color
    if result.match_score < 40:
        score_color = colors.red
    elif result.match_score < 60:
        score_color = colors.orange
    else:
        score_color = colors.green

    score_style = ParagraphStyle(
        'ScoreStyle',
        parent=styles['Normal'],
        textColor=score_color,
        fontSize=14
    )

    elements.append(Paragraph(f"<b>Match Score:</b> {result.match_score}%", score_style))
    elements.append(Spacer(1, 0.3 * inch))

    # AI Summary
    elements.append(Paragraph("<b>AI Evaluation Summary:</b>", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(result.ai_summary, styles["Normal"]))
    elements.append(Spacer(1, 0.5 * inch))

    # Missing Skills as bullets
    elements.append(Paragraph("<b>Missing Skills:</b>", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    if result.missing_skills:
        skills = result.missing_skills.split(", ")
        bullet_list = [ListItem(Paragraph(skill, styles["Normal"])) for skill in skills]
        elements.append(ListFlowable(bullet_list, bulletType='bullet'))
    else:
        elements.append(Paragraph("No missing skills. Excellent match!", styles["Normal"]))

    elements.append(Spacer(1, 0.5 * inch))

    # Date
    elements.append(Paragraph(f"<b>Generated On:</b> {result.created_at}", styles["Normal"]))

    doc.build(elements)

    return send_file(filepath, as_attachment=True)

# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    results = ResumeResult.query.order_by(ResumeResult.created_at.desc()).all()
    return render_template("admin.html", results=results)

# ---------------- RUN ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)