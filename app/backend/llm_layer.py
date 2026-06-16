import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# -----------------------------
# Load Gemini API Key
# -----------------------------
try:
    import streamlit as st
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in Streamlit Secrets or .env"
    )

# -----------------------------
# Gemini Client
# -----------------------------
client = genai.Client(api_key=api_key)


# -----------------------------
# Career Recommendation
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

Skills To Learn:
{', '.join(skill_gaps)}

Provide:

1. Why this role is suitable (2-3 lines)

2. 30-60-90 Day Learning Roadmap
   - First 30 Days
   - Next 30 Days
   - Final 30 Days

3. Top 3 Interview Tips

Use simple English.
Keep response practical and concise.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text

        return "No response generated."

    except Exception as e:
        return f"AI Error: {str(e)}"


# -----------------------------
# Local Test
# -----------------------------
if __name__ == "__main__":

    sample_job = {
        "title": "Machine Learning Engineer",
        "company": "Google",
        "match_score": 82
    }

    sample_skills = (
        "Python, Machine Learning, TensorFlow"
    )

    sample_gaps = [
        "MLOps",
        "Docker",
        "Kubernetes"
    ]

    print(
        get_career_explanation(
            sample_skills,
            sample_job,
            sample_gaps
        )
    )