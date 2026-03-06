from flask import send_file
import os
from reportlab.pdfgen import canvas

@app.route('/download/<int:analysis_id>')
def download_pdf(analysis_id):

    analysis = ResumeAnalysis.query.get_or_404(analysis_id)

    filename = f"report_{analysis_id}.pdf"

    c = canvas.Canvas(filename)

    c.setFont("Helvetica", 14)
    c.drawString(100, 800, "AI Resume Analysis Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, 760, f"Best Role: {analysis.role}")
    c.drawString(100, 740, f"Match Score: {analysis.score}%")
    c.drawString(100, 720, f"Date: {analysis.date}")

    c.save()

    return send_file(
        filename,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )
