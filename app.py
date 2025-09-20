import streamlit as st
import pandas as pd
# Importing the functions we wrote earlier in agent_logic.py
from agent_logic import (
    parse_resume_pdf_agent,
    parse_resume_text_agent,
    extract_skills_agent,
    get_candidate_name_agent,
    calculate_score_agent)

st.set_page_config(page_title="Resume Screening App", page_icon="🔎", layout="centered")
# Setting the page configuration for the Streamlit app
# This includes the title, icon, and layout settings

st.title("🔎 Resume Screening Application")
st.subheader("Upload your resume for screening")

# User input for job description
job_description = st.text_area(
    "Job Description",                                  # Label for the text area
    height=200,                                         # Height of the text area
    placeholder="Enter the job description here...")    # Placeholder text for the text area


uploaded_resumes = st.file_uploader(   # File uploader for resumes
    "Upload Resumes",           # Label for the file uploader
    type=["pdf", "docx"],       # Accepted file types
    accept_multiple_files=True  # Allow multiple file uploads
)


# Resume screening button and Results display
if st.button("Screen Resumes", use_container_width=True): # Button to trigger resume screening
    if job_description and uploaded_resumes:              # Check if both job description and resumes are provided
        with st.spinner("Screening Resumes..."):          # Show a spinner while processing
            job_skills = extract_skills_agent(job_description) # Extract skills from job description

            candidate_results = []
            for resume_file in uploaded_resumes:
                file_extension = resume_file.name.split(".")[-1].lower()
                if file_extension == "pdf": # Check if the file is a PDF
                    resume_text = parse_resume_pdf_agent(resume_file)
                elif file_extension == "txt": # Check if the file is a TXT
                    resume_text = parse_resume_text_agent(resume_file)
                else: # Unsupported file type
                    st.warning(f"Unsupported file type: {file_extension}")
                    continue
                

                resume_skills = extract_skills_agent(resume_text)
                score = calculate_score_agent(resume_skills, job_skills)

                candidate_results.append({
                    "Candidate Name": get_candidate_name_agent(resume_text),
                    "Match Score": score,
                    "File Name": resume_file.name,
                    "Matching Skills": ", ".join(resume_skills.intersection(job_skills)),
                })

            candidate_results = sorted(candidate_results, key=lambda x: x["Match Score"], reverse=True)

            st.success("Screening Complete!")
            st.markdown("---")
            st.header("Ranking of Candidates")

            df = pd.DataFrame(candidate_results)
            st.dataframe(df, use_container_width=True)


            st.markdown("---")
            st.header("Detailed Candidate Analysis")
            
            for candidate in candidate_results:
                st.subheader(f"Analysis for: {candidate['Candidate Name']}")
                st.metric("Match Score", f"{candidate['Match Score']}%")
                
                st.markdown("**Matching Skills:**")
                if candidate['Matching Skills']:
                    st.code(candidate['Matching Skills'])
                else:
                    st.warning("No matching skills found.")

    else:
        st.warning("Please provide both job description and resumes for screening.")
