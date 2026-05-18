# AI Resume Screener

An NLP-powered web app that ranks resumes against a job description
using TF-IDF cosine similarity and skill extraction.

## Live Demo
🔗 https://huggingface.co/spaces/Annadha/resume_screener

## Features
- Upload multiple PDF or DOCX resumes
- Paste or upload job descriptions
- Instant match score (0 to 100 percent)
- Skill gap analysis per candidate — matched and missing skills
- Score comparison bar chart
- CSV export of results

## Tech Stack
- Python
- spaCy — NLP preprocessing
- scikit-learn — TF-IDF and cosine similarity
- Streamlit — web app UI
- PyPDF2 — PDF parsing
- Plotly — data visualization

## How it works
1. User pastes or uploads a job description
2. User uploads one or more resumes in PDF or DOCX format
3. App extracts skills and preprocesses text using spaCy
4. TF-IDF cosine similarity scores content match
5. Skill matching checks required skills present in resume
6. Final score = 60% content match + 40% skill match
7. Candidates are ranked by final score

## Setup locally
pip install -r requirements.txt
streamlit run streamlit_app.py

## Project Structure
- streamlit_app.py — main UI
- matcher.py — scoring engine
- parser.py — PDF and DOCX text extraction
- preprocessor.py — NLP pipeline
- skills_db.py — skills keyword database
- requirements.txt — dependencies
- Dockerfile — for deployment
