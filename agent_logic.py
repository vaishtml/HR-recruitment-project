import spacy
# spacy is an NLP lib in Python
# helps computers to understand, process and analyze human language text
# think of it as a tool that can read and make sense of text data: tokenization
# named entity recognition (detects entities like python:language, ML: field)
# part-of-speech tagging, dependency parsing

from pypdf import PdfReader
# pypdf is a library for reading PDF files
# it allows you to extract text, images, and metadata from PDF documents
import io
# io is a module in Python that provides the Python interfaces to stream handling
# it allows you to work with streams (like files) in a consistent way
# to handle PDF files uploaded as bytes (in memory file objects)


# Load the spaCy model 
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    spacy.cli.download("en_core_web_sm")
    # In spacy, spacy.cli is a module that contains functions
    # for downloading and managing language models
    # After downloading, we load the model and use it for NLP tasks
    nlp = spacy.load("en_core_web_sm")
    # Loads the NLP model again after downloading so we can use it immediately


# PDF parsing agent
def parse_resume_pdf_agent(pdf_file):
    try:
        pdf_reader = PdfReader(io.BytesIO(pdf_file.read()))
        # Extract text from each page of the PDF
        # pdf_file is a file-like object containing the PDF data
        # pdf_file.read(..) reads the entire content of the PDF file into bytes
        # io.BytesIO(..) converts the bytes into an in-memory binary stream
        # PDFReader(..) creates a PDF reader object from the in-memory binary stream
        text = ""
        # Initializes an empty string to store the extracted text
        for page in pdf_reader.pages:
            # Loops through each page of the PDF
            text += page.extract_text() or ""
            # page.extract_text() extracts the text content from the PDF page
            # or "" ensures that if extraction fails, adds an empty string so we don't get None
            # text+= ... -> appends the extracted text to the existing text
        return text
        # Returns the extracted text from the PDF
    except Exception as e:
        print(f"Error processing PDF: {e}")

# Text file parsing agent
def parse_resume_text_agent(txt_file):
    # Extract text from the uploaded text file
    return txt_file.getValue().decode("utf-8")
    # txt_file.getValue() retrieves the content of the text file
    # .decode("utf-8") converts the bytes to a string using UTF-8 encoding
    # Returns the decoded text content
    

# Skill extraction agent
def extract_skills_agent(text):
    skills_list=[
        "python","r", "machine learning", "data analysis", "pandas", "numpy", "scikit-learn",
        "deep learning", "data visualization", "sql", "tableau", "powerbi", "statistics",
        "data engineering", "big data", "spark", "hadoop", "aws", "azure", "docker", "kubernetes",
        "web development", "html", "css", "javascript", "react", "node.js", "django","git",
        "flask","fastapi","java","nlp", "data cleaning","backend","devops"
    ]
    # A list of skills to extract from the text

    doc = nlp(text.lower())
    # Converts the text to lowercase 
    # Passes into spaCy's NLP pipeline for processing
    found_skills = {token.text for token in doc if token.text in skills_list}
    # Creates a set of found skills by checking each token against the skills list
    return found_skills
    # Returns the set of found skills

# Candidate name extraction agent
def get_candidate_name_agent(resume_txt):
    # Extracts the candidate's name from the resume text
    lines = resume_txt.strip().split("\n")
    # Splits the resume text into lines
    if lines:
        # Checks if there are any lines
        return lines[0].strip()
    return "Name not found"

# Resume scoring agent
def calculate_score_agent(resume_skills,job_skills):
    # Calculates the score based on the number of matching skills
    if not job_skills:
        return 0.0
        # If there are no job skills, the score is 0

    # Finds the matching skills between resume and job description
    matching_skills = resume_skills.intersection(job_skills)
    # Calculates the score as percentage match
    score = (len(matching_skills) / len(job_skills)) * 100
    # Returns the final score rounded to two decimal places
    return round(score, 2)

# Summary
# This code defines several agents for processing resumes, including parsing PDF and text files,
# extracting skills and candidate names, and calculating a resume score based on job requirements.