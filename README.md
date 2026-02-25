# AI Resume–Job Matching System

## Project Overview

The **AI Resume–Job Matching System** is a web-based application that analyzes a candidate’s resume against a job description and calculates a compatibility score using Natural Language Processing (NLP).

The system extracts and compares relevant keywords, computes similarity scores, and provides structured feedback to help candidates optimize their resumes for specific roles.

Built with Streamlit, this tool demonstrates practical AI application in recruitment technology.

---

## Features

* 📄 Upload Resume (PDF format)
* 📝 Paste Job Description
* 🧠 NLP-based Text Processing
* 🔍 Keyword Extraction & Matching
* 📊 Cosine Similarity Score Calculation
* 🎨 Color-Coded Match Score (Green = High, Red = Low)
* 📈 Visual Progress Bar for Match Percentage
* 📑 Downloadable PDF Report
* ⚡ Clean, Interactive Streamlit UI

---

## Tech Stack

**Programming Language**

* Python 3.x

**Libraries & Frameworks**

* Streamlit (Frontend Web App)
* Scikit-learn (TF-IDF Vectorization & Cosine Similarity)
* NLTK (Text preprocessing)
* PyPDF2 (Resume PDF extraction)
* ReportLab (PDF report generation)
* Pandas (Data handling)

---

## ⚙ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/resume-ai-analyzer.git
cd resume-ai-analyzer
```

### 2️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If `reportlab` is missing:

```bash
pip install reportlab
```

---

## ▶ How to Run

```bash
streamlit run app.py
```

Then open your browser at:

```
http://localhost:8501
```

---

## 📊 Example Output

**Match Score: 78%**

🟢 High Compatibility

**Matched Keywords:**

* Python
* Machine Learning
* Data Analysis
* SQL

**Missing Keywords:**

* Docker
* AWS
* CI/CD

The system also generates a downloadable PDF report summarizing:

* Match percentage
* Matched keywords
* Missing keywords
* Recommendations

---

## 📈 How It Works

1. Extracts text from uploaded PDF resume
2. Cleans and preprocesses text (tokenization, stopword removal)
3. Converts resume and job description into TF-IDF vectors
4. Computes cosine similarity
5. Displays results with visual feedback

---

## 🎯 Future Improvements

* BERT-based semantic similarity
* Skill categorization (technical vs soft skills)
* Resume improvement suggestions
* Multi-job comparison
* Database integration
* Deployment on Streamlit Cloud / AWS

---

## Author

Marjuk

Computer Science Student

Passionate about AI, Machine Learning & Software Engineering
