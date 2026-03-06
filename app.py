from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from reportlab.pdfgen import canvas
import io
import os
from resume_parser import match_resume

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resume_data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------------- DATABASE MODEL ---------------- #

class ResumeResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    best_role = db.Column(db.String(100))
    match_score = db.Column(db.Float)
    missing_skills = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- HOME PAGE ---------------- #

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        try:
            resume_file = request.files["resume"]

            if resume_file:

                resume_text = resume_file.read().decode("utf-8", errors="ignore")

                best_role, score, missing = match_resume(resume_text)

                # Save to DB
                result = ResumeResult(
                    best_role=best_role,
                    match_score=score,
                    missing_skills=", ".join(missing)
                )

                db.session.add(result)
                db.session.commit()

                return render_template(
                    "result.html",
                    role=best_role,
                    score=score,
                    missing=missing,
                    result_id=result.id
                )

        except Exception as e:
            return f"Upload Error: {str(e)}"

    return render_template("index.html")


# ---------------- ADMIN DASHBOARD ---------------- #

@app.route("/admin")
def admin():

    data = ResumeResult.query.order_by(ResumeResult.created_at.desc()).all()

    return render_template("admin.html", data=data)


# ---------------- PDF DOWNLOAD ---------------- #

@app.route("/download/<int:result_id>")
def download(result_id):

    result = ResumeResult.query.get(result_id)

    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setFont("Helvetica", 14)

    pdf.drawString(100, 800, "AI Resume Analysis Report")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(100, 760, f"Best Role: {result.best_role}")
    pdf.drawString(100, 740, f"Match Score: {result.match_score}%")
    pdf.drawString(100, 720, f"Missing Skills: {result.missing_skills}")

    pdf.drawString(100, 700, f"Date: {result.created_at}")

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="resume_report.pdf",
        mimetype="application/pdf"
    )


# ---------------- START SERVER ---------------- #

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
