from flask import Flask, request, jsonify, send_file
import os
import re
import nltk
from nltk.corpus import stopwords
from pdfminer.high_level import extract_text
from werkzeug.utils import secure_filename
from flask_cors import CORS

nltk.download("punkt")
nltk.download("stopwords")

app = Flask(__name__)
CORS(app)

latest_result = None  # Only one resume

@app.route("/analyze-pdf", methods=["POST"])
def analyze_single_pdf():
    global latest_result
    files = request.files.getlist("resumes")
    job_keywords = request.form.get("job_keywords")

    if not files or not job_keywords:
        return jsonify({"error": "Missing files or keywords"}), 400

    file = files[0]  # Only process the first file
    filename = secure_filename(file.filename)
    temp_path = f"temp_{filename}"
    file.save(temp_path)

    try:
        resume_text = extract_text(temp_path)
    except Exception as e:
        os.remove(temp_path)
        return jsonify({"error": f"Error extracting text from {filename}: {str(e)}"}), 500

    os.remove(temp_path)

    jd_keywords = {kw.strip().lower() for kw in job_keywords.split(",") if kw.strip()}
    resume_text_clean = re.sub(r"[^\w\s]", " ", resume_text.lower())
    resume_text_clean = re.sub(r"\s+", " ", resume_text_clean)

    matched = {kw for kw in jd_keywords if re.search(r"\b" + re.escape(kw) + r"\b", resume_text_clean)}
    missing = jd_keywords - matched
    score = round((len(matched) / len(jd_keywords)) * 100, 2) if jd_keywords else 0

    suggestions = []
    if "objective" not in resume_text.lower():
        suggestions.append("Add an 'Objective' section.")
    if "github" not in resume_text.lower():
        suggestions.append("Include a GitHub link.")
    if "experience" not in resume_text.lower():
        suggestions.append("Mention relevant work experience.")
    if "python" not in resume_text.lower() and "java" not in resume_text.lower():
        suggestions.append("Consider adding programming skills like Python or Java.")
    if "linkedin" not in resume_text.lower():
        suggestions.append("Add a LinkedIn profile link.")

    latest_result = {
        "filename": filename,
        "match_score": score,
        "matched_keywords": sorted(list(matched)),
        "missing_keywords": sorted(list(missing)),
        "suggestions": suggestions
    }

    return jsonify({"results": [latest_result]})


@app.route("/download-report", methods=["GET"])
def download_report():
    global latest_result
    if not latest_result:
        return jsonify({"error": "No data to download"}), 400

    txt_path = "resume_report.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        res = latest_result
        f.write(f"Filename: {res['filename']}\n")
        f.write(f"Match Score: {res['match_score']}%\n")
        f.write(f"Matched Keywords: {', '.join(res['matched_keywords']) or 'None'}\n")
        f.write(f"Missing Keywords: {', '.join(res['missing_keywords']) or 'None'}\n")
        f.write(f"Suggestions: {' '.join(res['suggestions']) or 'None'}\n")

    return send_file(txt_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
    

