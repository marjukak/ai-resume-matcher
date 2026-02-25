import PyPDF2
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import string
from sentence_transformers import SentenceTransformer
import numpy as np

# Load the embedding model only once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_resume(file):
    """
    Extracts text from PDF or DOCX resumes (Streamlit uploaded files).
    """
    text = ""
    if hasattr(file, "type"):
        if file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"
    return text


def extract_text_from_pdf(file_path):
    """
    Extracts all text from a multi-page PDF file (path-based).
    """
    text = ""
    with open(file_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def clean_text(text):
    """
    Cleans input text: lowercase, remove punctuation, remove extra spaces.
    """
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def generate_embedding(text):
    """
    Generates embedding for a given text using all-MiniLM-L6-v2.
    """
    return embedding_model.encode(text)


def compute_similarity(emb1, emb2):
    """
    Computes cosine similarity between two embeddings and converts to percentage.
    """
    sim = cosine_similarity([emb1], [emb2])[0][0]
    return float(sim * 100)


def extract_keywords(text, top_n=15):
    """
    Extracts top N keywords from text using TF-IDF.
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    word_score_pairs = list(zip(feature_names, scores))
    sorted_words = sorted(word_score_pairs, key=lambda x: x[1], reverse=True)
    top_keywords = [word for word, score in sorted_words[:top_n]]
    return top_keywords


def missing_keywords(resume_text, keywords):
    """
    Returns a list of keywords that are missing in the resume text.
    """
    cleaned_resume = clean_text(resume_text)
    missing = [kw for kw in keywords if kw.lower() not in cleaned_resume]
    return missing


def analyze_resume(resume_file, job_description):
    """
    Analyzes a resume against a job description:
    - Extracts and cleans text
    - Generates embeddings
    - Computes similarity score
    - Extracts top keywords
    - Highlights keywords in resume text
    - Returns structured results
    """
    # Extract resume text
    if isinstance(resume_file, str):
        resume_text = extract_text_from_pdf(resume_file)
        filename = resume_file.split("\\")[-1]  # filename from path
    else:
        resume_text = extract_text_from_resume(resume_file)
        filename = resume_file.name

    # Clean text
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_description)

    # Generate embeddings
    resume_emb = generate_embedding(resume_clean)
    job_emb = generate_embedding(job_clean)

    # Compute similarity
    similarity = compute_similarity(resume_emb, job_emb)

    # Extract top keywords
    top_keywords = extract_keywords(job_clean)

    # Determine missing keywords
    resume_words = set(resume_clean.split())
    missing = [kw for kw in top_keywords if kw not in resume_words]

    # Highlight keywords in resume text
    highlighted_text = resume_text
    for kw in top_keywords:
        color = "green" if kw.lower() not in [m.lower() for m in missing] else "yellow"
        highlighted_text = re.sub(
            rf"\b({re.escape(kw)})\b",
            fr"<span style='background-color:{color}'>{kw}</span>",
            highlighted_text,
            flags=re.IGNORECASE
        )

    return {
        "file": filename,
        "similarity": similarity,
        "top_keywords": top_keywords,
        "missing_keywords": missing,
        "highlighted_text": highlighted_text
    }
