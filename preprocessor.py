import spacy
import re

nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\+\#]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess(text: str) -> str:
    cleaned = clean_text(text)
    doc = nlp(cleaned)
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and len(token.text) > 1
    ]
    return " ".join(tokens)

def extract_skills(text: str, skills_list: list) -> list:
    text_lower = text.lower()
    found = []
    for skill in skills_list:
        if skill.lower() in text_lower:
            found.append(skill)
    return found