import streamlit as st
import pandas as pd

from src.parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from src.preprocess import preprocess_text

from src.matcher import calculate_similarity

from src.skill_extractor import extract_skills

from src.ranker import rank_candidates

from utils.helpers import format_percentage


st.set_page_config(page_title="AI Resume Screening System")

st.title("AI-Based Resume Screening System")


job_description = st.text_area(
    "Enter Job Description"
)

uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


if st.button("Screen Resumes"):

    results = []

    for uploaded_file in uploaded_files:

        file_name = uploaded_file.name

        if file_name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)

        elif file_name.endswith(".docx"):
            resume_text = extract_text_from_docx(uploaded_file)

        else:
            resume_text = ""

        processed_resume = preprocess_text(resume_text)

        processed_jd = preprocess_text(job_description)

        similarity_score = calculate_similarity(
            processed_resume,
            processed_jd
        )

        formatted_score = format_percentage(similarity_score)

        skills = extract_skills(resume_text)

        results.append({
            "Candidate": file_name,
            "Match Score": formatted_score,
            "Skills": ", ".join(skills)
        })

    df = rank_candidates(results)

    st.subheader("Screening Results")

    st.dataframe(df)