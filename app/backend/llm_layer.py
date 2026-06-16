import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# -----------------------------
# Load API Key
# -----------------------------
api_key = None

try:
    import streamlit as st

    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]

except Exception:
    pass

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in Streamlit Secrets or .env"
    )

# -----------------------------
# Configure Gemini
# -----------------------------
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-1.5-flash-8b"
)

# -----------------------------
# Career Explanation Function
# -----------------------------
def get_career_explanation(
    student_skills,
    recommended_job,
    skill_gaps
):
    prompt = f"""
You are an expert career counselor for Indian tech students.

Student Skills:
{student_skills}

Recommended Job:
{recommended_job['title']} at {recommended_job['company']}

Match Score:
{recommended_job['match_score']}%

Missing Skills:
{skill_gaps}

Provide:

1. Why this role is suitable (2-3 lines)

2. 30-60-90 day learning roadmap:
   - First 30 Days
   - Next 30 Days
   - Final 30 Days

3. Top 3 interview preparation tips

Keep the response practical, concise and beginner-friendly.
"""

    response = model.generate_content(prompt)

    if not response:
        return "No response received from Gemini."

    if hasattr(response, "text") and response.text:
        return response.text

    return str(response)


# -----------------------------
# Local Testing
# -----------------------------
if __name__ == "__main__":

    sample_job = {
        "title": "Machine Learning Engineer",
        "company": "BSNL",
        "match_score": 50.0
    }

    sample_skills = (
        "Python, TensorFlow, Machine Learning"
    )

    sample_gaps = [
        "PyTorch",
        "MLOps"
    ]

    print("Testing Gemini...\n")

    result = get_career_explanation(
        sample_skills,
        sample_job,
        sample_gaps
    )

    print(result)
