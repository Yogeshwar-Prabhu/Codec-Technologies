from flask import Flask, render_template, request
import pandas as pd
import pdfplumber
import docx2txt
import re
import os

app = Flask(__name__)

# --- Load Skills from CSV ---
skills_df = pd.read_csv("data/skills.csv")
skills_list = [s.strip().lower() for s in skills_df["skill"].tolist()]

# --- Helper function to extract text from resume ---
def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    elif file_path.endswith(".docx"):
        text = docx2txt.process(file_path)
    return text.lower()

# --- Helper function to find skills ---
def extract_skills(resume_text):
    found_skills = []
    for skill in skills_list:
        if re.search(rf"\b{skill}\b", resume_text):
            found_skills.append(skill)
    return found_skills

@app.route("/")
def upload_page():
    return render_template("upload.html")

@app.route("/parse", methods=["POST"])
def parse_resume():
    if "resume" not in request.files:
        return "No file uploaded!"

    file = request.files["resume"]
    if file.filename == "":
        return "No file selected!"

    upload_path = os.path.join("data", file.filename)
    file.save(upload_path)

    resume_text = extract_text(upload_path)
    skills_found = extract_skills(resume_text)

    return render_template("results.html", skills=skills_found, filename=file.filename)

if __name__ == "__main__":
    app.run(debug=True)