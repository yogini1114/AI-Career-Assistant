import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

# -----------------------------
# API KEY
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
# AI Career Explanation
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
{', '.join(skill_gaps)}

Provide:

1. Why this role is recommended (2-3 lines)

2. 30-60-90 Day Learning Roadmap
   - First 30 Days
   - Next 30 Days
   - Final 30 Days

3. Top 3 Interview Tips

Use simple English.
Keep response concise and practical.
"""

    # Retry 3 times if Gemini is busy
    for attempt in range(3):
        try:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            if hasattr(response, "text") and response.text:
                return response.text

            return "No response generated."

        except Exception as e:

            error_msg = str(e)

            # Gemini overloaded
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                time.sleep(5)
                continue

            # Quota exceeded
            if "429" in error_msg:
                return (
                    "⚠️ Gemini API quota exceeded. "
                    "Please try again later."
                )

            return f"⚠️ AI Error: {error_msg}"

    return (
        "⚠️ Gemini service is currently busy. "
        "Please try again after a few minutes."
    )


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
        "Python, TensorFlow, Machine Learning"
    )

    sample_gaps = [
        "MLOps",
        "Docker",
        "Kubernetes"
    ]

    result = get_career_explanation(
        sample_skills,
        sample_job,
        sample_gaps
    )

    print(result)