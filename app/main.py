import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from resume_parser import parse_resume
from recommender import get_recommendations, get_skill_gaps
from llm_layer import get_career_explanation

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Career Assistant")
st.subheader("Upload your resume and get personalized career recommendations!")

st.sidebar.header("📄 Upload Resume")
uploaded_file = st.sidebar.file_uploader(
    "Upload your PDF resume",
    type=['pdf']
)

skills_input = st.sidebar.text_area(
    "Or enter your skills manually:",
    placeholder="Python, Machine Learning, SQL, TensorFlow..."
)

if st.sidebar.button("🔍 Get Recommendations"):
    student_skills = ""
    if uploaded_file:
        with st.spinner("Parsing resume..."):
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            resume_data = parse_resume(tmp_path)
            student_skills = resume_data['skills_text']
            st.success(f"Skills found: {student_skills}")
    elif skills_input:
        student_skills = skills_input
    else:
        st.error("Please upload a resume or enter skills!")

    if student_skills:
        with st.spinner("Finding best matches..."):
            recommendations = get_recommendations(student_skills)
        
        st.header("🎯 Top Job Recommendations")
        
        for i, job in enumerate(recommendations):
            with st.expander(f"#{i+1} {job['title']} at {job['company']} — {job['match_score']}% match"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Match Score", f"{job['match_score']}%")
                    st.metric("Salary", f"{job['salary']} LPA")
                with col2:
                    gaps = get_skill_gaps(student_skills, job['skills_required'])
                    st.write("**Skills to Learn:**")
                    for gap in gaps:
                        st.write(f"• {gap}")
                if st.button(f"Get AI Advice for {job['title']}", key=f"btn_{i}"):
                    with st.spinner("Getting AI advice..."):
                        try:
                            explanation = get_career_explanation(
                                student_skills, job, gaps
                            )
                            st.write(explanation)
                        except:
                            st.warning("AI advice unavailable right now!")