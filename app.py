from flask import Flask, render_template, request
from resume_parser import analyze_resume

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():

    if 'resume' not in request.files:
        return "No file uploaded"

    file = request.files['resume']

    if file.filename == '':
        return "No selected file"

    resume_text = file.read().decode('utf-8')

    result = analyze_resume(resume_text)

    return render_template(
        "result.html",
        score=result["score"],
        role=result["role"],
        skills=result["skills"],
        missing=result["missing"]
    )


@app.route('/admin')
def admin():
    return render_template("admin.html")


if __name__ == '__main__':
    app.run(debug=True)
