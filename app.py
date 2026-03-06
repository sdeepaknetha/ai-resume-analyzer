from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from resume_parser import match_resume
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# -----------------------------
# DATABASE CONFIG
# -----------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resume_data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -----------------------------
# DATABASE MODEL
# -----------------------------
class ResumeResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    best_role = db.Column(db.String(100))
    match_score = db.Column(db.Float)
    missing_skills = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        resume_file = request.files.get("resume")

        if not resume_file:
            return render_template("index.html", error="Please upload a resume")

        try:
            resume_text = resume_file.read().decode("utf-8", errors="ignore")

            best_role, score, missing = match_resume(resume_text)

            # save to database
            result = ResumeResult(
                best_role=best_role,
                match_score=score,
                missing_skills=", ".join(missing)
            )

            db.session.add(result)
            db.session.commit()

            return render_template(
                "index.html",
                role=best_role,
                score=score,
                missing=missing
            )

        except Exception as e:
            return f"Upload Error: {str(e)}"

    return render_template("index.html")


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
@app.route("/admin")
def admin():

    results = ResumeResult.query.order_by(ResumeResult.id.desc()).all()

    return render_template(
        "admin.html",
        results=results
    )


# -----------------------------
# PDF DOWNLOAD
# -----------------------------
@app.route("/download/<int:id>")
def download(id):

    result = ResumeResult.query.get(id)

    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.drawString(100, 750, "AI Resume Analysis Report")
    pdf.drawString(100, 720, f"Best Role: {result.best_role}")
    pdf.drawString(100, 700, f"Match Score: {result.match_score}%")
    pdf.drawString(100, 680, f"Date: {result.created_at}")

    pdf.drawString(100, 650, "Missing Skills:")

    skills = result.missing_skills.split(",")

    y = 630

    for skill in skills:
        pdf.drawString(120, y, skill.strip())
        y -= 20

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="resume_report.pdf",
        mimetype="application/pdf"
    )


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
