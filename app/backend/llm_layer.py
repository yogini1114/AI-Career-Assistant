import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

try:
    import streamlit as st
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def get_career_explanation(student_skills, recommended_job, skill_gaps):

    prompt = f"""
You are a career counselor for Indian tech students.

Student Skills:
{student_skills}

Recommended Job:
{recommended_job['title']} at {recommended_job['company']}

Match Score:
{recommended_job['match_score']}%

Skills to Learn:
{skill_gaps}

Provide:

1. Why this role is recommended (2-3 lines)

2. 30-60-90 day roadmap

3. Top 3 interview tips

Keep response concise.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI Error: {str(e)}"