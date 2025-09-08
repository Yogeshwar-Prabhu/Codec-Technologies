# Automated Resume Parser (Flask)

This project extracts key details (Name, Email, Skills, Education) from resumes in PDF format.

## Features
- Upload resume (PDF)
- Extracts details using NLP (spaCy)
- Skill matching from predefined list (CSV)

## Run Locally
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py