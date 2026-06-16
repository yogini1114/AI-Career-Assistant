import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Local pe .env se, Streamlit Cloud pe st.secrets se
try:
    import streamlit as st
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash-lite')

def get_career_explanation(student_skills, recommended_job, skill_gaps):
    prompt = f"""
    You are a career counselor for Indian tech students.

    Student Skills: {student_skills}
    Recommended Job: {recommended_job['title']} at {recommended_job['company']}
    Match Score: {recommended_job['match_score']}%
    Skills to Learn: {skill_gaps}

    Please provide in simple English:
    1. Why this job is recommended (2-3 lines)
    2. 30-60-90 day learning roadmap for missing skills
    3. Top 3 interview tips for this role
    
    Keep it concise and practical.
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    test_job = {
        'title': 'Machine Learning Engineer',
        'company': 'BSNL',
        'match_score': 50.0
    }
    test_skills = "Python, TensorFlow, Machine Learning"
    test_gaps = ['pytorch', 'mlops']

    print("Getting AI explanation...")
    explanation = get_career_explanation(
        test_skills,
        test_job,
        test_gaps
    )
    print(explanation)