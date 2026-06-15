import fitz
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(text):
    tech_skills = [
        "python", "java", "javascript", "typescript", "c++", "c#",
        "html", "css", "react", "angular", "vue", "nodejs",
        "django", "flask", "fastapi",
        "sql", "mysql", "postgresql", "mongodb", "redis",
        "machine learning", "deep learning", "nlp",
        "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
        "aws", "azure", "gcp", "docker", "kubernetes", "git",
        "data science", "data analysis", "power bi", "tableau",
        "android", "ios", "flutter", "devops", "mlops"
    ]
    text_lower = text.lower()
    found_skills = []
    for skill in tech_skills:
        if skill in text_lower:
            found_skills.append(skill)
    return list(set(found_skills))

def extract_education(text):
    education_keywords = [
        "b.tech", "btech", "bachelor", "m.tech", "mca", "mba",
        "bca", "bsc", "msc", "phd", "computer science"
    ]
    text_lower = text.lower()
    found_education = []
    for edu in education_keywords:
        if edu in text_lower:
            found_education.append(edu)
    return found_education

def extract_experience_years(text):
    patterns = [
        r'(\d+)\+?\s*years?\s*of\s*experience',
        r'(\d+)\+?\s*years?\s*experience',
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    return 0

def parse_resume(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    skills = extract_skills(raw_text)
    education = extract_education(raw_text)
    experience = extract_experience_years(raw_text)
    result = {
        "raw_text": raw_text,
        "skills": skills,
        "education": education,
        "experience_years": experience,
        "skills_text": ", ".join(skills)
    }
    return result

if __name__ == "__main__":
    print("Resume Parser ready!")