import streamlit as st
import sys
import os
import tempfile

sys.path.append(
    os.path.join(os.path.dirname(__file__), "backend")
)

from resume_parser import parse_resume
from recommender import get_recommendations, get_skill_gaps
from llm_layer import get_career_explanation
from vector_db import ensure_jobs_loaded

# -----------------------------
# Setup
# -----------------------------
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🚀",
    layout="wide"
)

ensure_jobs_loaded()

# -----------------------------
# Session State
# -----------------------------
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

if "student_skills" not in st.session_state:
    st.session_state.student_skills = ""

# -----------------------------
# Header
# -----------------------------
st.title("🚀 AI Career Assistant")
st.subheader(
    "Upload your resume and get personalized career recommendations!"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("📄 Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload your PDF resume",
    type=["pdf"]
)

skills_input = st.sidebar.text_area(
    "Or enter your skills manually:",
    placeholder="Python, Machine Learning, SQL, TensorFlow..."
)

# -----------------------------
# Get Recommendations
# -----------------------------
if st.sidebar.button("🔍 Get Recommendations"):

    student_skills = ""

    try:

        if uploaded_file:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp:

                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            resume_data = parse_resume(tmp_path)

            student_skills = resume_data["skills_text"]

            st.success(
                f"Skills found: {student_skills}"
            )

        elif skills_input:

            student_skills = skills_input

        else:

            st.warning(
                "Please upload a resume or enter skills."
            )

        if student_skills:

            with st.spinner(
                "Finding best matches..."
            ):

                recommendations = (
                    get_recommendations(
                        student_skills
                    )
                )

            st.session_state.student_skills = (
                student_skills
            )

            st.session_state.recommendations = (
                recommendations
            )

    except Exception as e:

        st.error(f"Error: {e}")

# -----------------------------
# Show Recommendations
# -----------------------------
if st.session_state.recommendations:

    recommendations = (
        st.session_state.recommendations
    )

    student_skills = (
        st.session_state.student_skills
    )

    st.header("🎯 Top Job Recommendations")

    for i, job in enumerate(recommendations):

        gaps = get_skill_gaps(
            student_skills,
            job["skills_required"]
        )

        with st.expander(
            f"#{i+1} {job['title']} at "
            f"{job['company']} — "
            f"{job['match_score']}% match"
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Match Score",
                    f"{job['match_score']}%"
                )

                st.metric(
                    "Salary",
                    f"{job['salary']} LPA"
                )

            with col2:

                st.write(
                    "### Skills to Learn"
                )

                if gaps:

                    for gap in gaps:
                        st.write(f"• {gap}")

                else:
                    st.success(
                        "No major skill gaps"
                    )

            # ------------------
            # AI Advice
            # ------------------
            if st.button(
                f"🤖 Get AI Advice for {job['title']}",
                key=f"ai_btn_{i}"
            ):

                with st.spinner(
                    "Generating AI advice..."
                ):

                    explanation = (
                        get_career_explanation(
                            student_skills,
                            job,
                            gaps
                        )
                    )

                    st.markdown(explanation)