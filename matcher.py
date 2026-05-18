from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessor import preprocess, extract_skills
from skills_db import SKILLS

def compute_match(jd_text: str, resume_text: str) -> dict:
    jd_processed = preprocess(jd_text)
    resume_processed = preprocess(resume_text)

    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([jd_processed, resume_processed])
        cosine_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except Exception:
        cosine_score = 0.0

    jd_skills = set(extract_skills(jd_text, SKILLS))
    resume_skills = set(extract_skills(resume_text, SKILLS))
    matched_skills = jd_skills & resume_skills
    missing_skills = jd_skills - resume_skills
    skill_score = (len(matched_skills) / len(jd_skills)) if jd_skills else 0.0

    final_score = (cosine_score * 0.6) + (skill_score * 0.4)
    final_percentage = round(final_score * 100, 2)

    return {
        "score": final_percentage,
        "cosine_score": round(cosine_score * 100, 2),
        "skill_score": round(skill_score * 100, 2),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "jd_skills": sorted(jd_skills),
        "resume_skills": sorted(resume_skills),
    }

def rank_resumes(jd_text: str, resumes: list) -> list:
    results = []
    for resume in resumes:
        match = compute_match(jd_text, resume["text"])
        results.append({"Candidate": resume["name"], **match})
    results.sort(key=lambda x: x["score"], reverse=True)
    for i, r in enumerate(results):
        r["Rank"] = i + 1
    return results