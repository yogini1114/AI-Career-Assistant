import streamlit as st
import sys
import os
import tempfile

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "backend"
    )
)

from resume_parser import parse_resume
from recommender import (
    get_recommendations,
    get_skill_gaps
)
from llm_layer import get_career_explanation
from vector_db import ensure_jobs_loaded

# -----------------------------
# Load Chroma Data
# -----------------------------
ensure_jobs_loaded()

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🚀",
    layout="wide"
)

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
# Button
# -----------------------------
if st.sidebar.button("🔍 Get Recommendations"):

    student_skills = ""

    # -------------------------
    # Resume Upload
    # -------------------------
    if uploaded_file:

        with st.spinner("Parsing resume..."):

            try:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp:

                    tmp.write(
                        uploaded_file.read()
                    )

                    tmp_path = tmp.name

                resume_data = parse_resume(
                    tmp_path
                )

                student_skills = (
                    resume_data["skills_text"]
                )

                st.success(
                    f"Skills found: {student_skills}"
                )

            except Exception as e:

                st.error(
                    f"Resume Parsing Error: {e}"
                )

    # -------------------------
    # Manual Skills
    # -------------------------
    elif skills_input:

        student_skills = skills_input

    else:

        st.warning(
            "Please upload a resume or enter skills."
        )

    # -------------------------
    # Recommendations
    # -------------------------
    if student_skills:

        with st.spinner(
            "Finding best career matches..."
        ):

            try:

                recommendations = (
                    get_recommendations(
                        student_skills
                    )
                )

            except Exception as e:

                st.error(
                    f"Recommendation Error: {e}"
                )

                recommendations = []

        st.header(
            "🎯 Top Career Recommendations"
        )

        if not recommendations:

            st.warning(
                "No recommendations found."
            )

        else:

            for i, job in enumerate(
                recommendations
            ):

                title = job.get(
                    "title",
                    "Unknown Role"
                )

                company = job.get(
                    "company",
                    "Unknown Company"
                )

                score = job.get(
                    "match_score",
                    0
                )

                salary = job.get(
                    "salary",
                    "N/A"
                )

                with st.expander(
                    f"#{i+1} {title} at {company} — {score}% match"
                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Match Score",
                            f"{score}%"
                        )

                        st.metric(
                            "Salary",
                            f"{salary} LPA"
                        )

                    with col2:

                        gaps = get_skill_gaps(
                            student_skills,
                            job["skills_required"]
                        )

                        st.write(
                            "**Skills to Learn:**"
                        )

                        if gaps:

                            for gap in gaps:
                                st.write(
                                    f"• {gap}"
                                )

                        else:

                            st.success(
                                "No major skill gaps found."
                            )

                    # -----------------
                    # AI Advice Button
                    # -----------------
                    if st.button(
                        f"🤖 Get AI Advice for {title}",
                        key=f"btn_{i}"
                    ):

                        with st.spinner(
                            "Generating AI advice..."
                        ):

                            try:

                                explanation = (
                                    get_career_explanation(
                                        student_skills,
                                        job,
                                        gaps
                                    )
                                )

                                st.success(
                                    "AI Advice Generated"
                                )

                                st.markdown(
                                    explanation
                                )

                            except Exception as e:

                                st.error(
                                    f"AI Error: {e}"
                                )