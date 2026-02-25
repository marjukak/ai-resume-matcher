# AI Resume–Job Matching System

This project matches resumes to job descriptions using AI/NLP techniques.

## Features
- Upload multiple resumes (PDF/DOCX)
- Input a job description
- Computes similarity scores for each resume
- Ranks resumes based on relevance

## Setup Instructions
1. Clone the repository
2. Create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

## Future Improvements
- Use OpenAI embeddings for better semantic matching
- Extract structured information: skills, education, experience
- Add downloadable reports for top candidates
