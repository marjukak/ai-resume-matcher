import streamlit as st
from utils import analyze_resume
import pandas as pd
import altair as alt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO

# ----------------------
# Page Config
# ----------------------
st.set_page_config(page_title="AI Resume–Job Match Analyzer", layout="wide")

# ----------------------
# Sidebar
# ----------------------
st.sidebar.title("Filters & Controls")

min_similarity = st.sidebar.slider(
    "Minimum Similarity Threshold (%)",
    0, 100, 0
)

strong_only = st.sidebar.checkbox("Show Only Strong Matches (≥70%)")

with st.sidebar.expander("What is ATS Scoring?"):
    st.write("""
    Applicant Tracking Systems (ATS) scan resumes for keyword relevance and contextual similarity.

    This analyzer uses:
    • Sentence embeddings (semantic similarity)
    • TF-IDF keyword extraction
    • Keyword coverage percentage

    High score = strong contextual + keyword alignment.
    """)

# ----------------------
# Styling
# ----------------------
st.markdown("""
<style>
.block-container { padding-top: 2rem; }
h1 { text-align: center; }
.section-box {
    padding: 20px;
    border-radius: 10px;
    background-color: #f9f9f9;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Resume–Job Match Analyzer")
st.caption("Compare resumes against job descriptions using embeddings and keyword analysis.")
st.divider()

# ----------------------
# Upload Section
# ----------------------
uploaded_files = st.file_uploader(
    "Upload Resume(s) (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

job_descriptions_input = st.text_area(
    "Enter Job Description(s) (Separate multiple jobs with --- on a new line)",
    height=250
)

st.divider()

# ----------------------
# Analyze
# ----------------------
if st.button("Analyze Resumes"):

    if not uploaded_files:
        st.warning("Please upload at least one resume file.")
    elif not job_descriptions_input.strip():
        st.warning("Please enter at least one job description.")
    else:

        job_descriptions = [jd.strip() for jd in job_descriptions_input.split('---') if jd.strip()]

        for jd_index, job_description in enumerate(job_descriptions, start=1):

            st.header(f"Job Description {jd_index}")
            st.write(job_description)
            st.divider()

            results = []
            progress_bar = st.progress(0)
            total_files = len(uploaded_files)

            for i, file in enumerate(uploaded_files):
                res = analyze_resume(file, job_description)

                total_keywords = len(res["top_keywords"])
                present_keywords = total_keywords - len(res["missing_keywords"])
                coverage_percent = (present_keywords / total_keywords * 100) if total_keywords else 0
                res["coverage_percent"] = coverage_percent

                results.append(res)
                progress_bar.progress((i + 1) / total_files)

            progress_bar.empty()

            # ----------------------
            # Sidebar Filters
            # ----------------------
            if strong_only:
                results = [r for r in results if r["similarity"] >= 70]

            results = [r for r in results if r["similarity"] >= min_similarity]

            if not results:
                st.warning("No resumes match the selected filters.")
                continue

            # ----------------------
            # Show Job Description Keywords (RESTORED FEATURE)
            # ----------------------
            st.subheader("Job Description Keywords")
            jd_keywords = results[0]["top_keywords"]

            keyword_cols = st.columns(4)
            for idx, kw in enumerate(jd_keywords):
                keyword_cols[idx % 4].markdown(f"- {kw}")

            st.divider()

            # ----------------------
            # Best Match Section
            # ----------------------
            best_resume = max(results, key=lambda x: x["similarity"])

            st.subheader("Best Match Resume")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Similarity Score", f"{best_resume['similarity']:.2f}%")
                st.progress(best_resume["similarity"] / 100)

                if best_resume["similarity"] >= 70:
                    st.success("Strong Match")
                elif best_resume["similarity"] >= 40:
                    st.warning("Moderate Match")
                else:
                    st.error("Weak Match")

            with col2:
                st.metric("Keyword Coverage", f"{best_resume['coverage_percent']:.2f}%")
                st.progress(best_resume["coverage_percent"] / 100)

            st.markdown("### Resume Preview")
            st.markdown(best_resume["highlighted_text"].replace("\n", "<br>"), unsafe_allow_html=True)

            st.divider()

            # ----------------------
            # Summary Table
            # ----------------------
            df = pd.DataFrame([{
                "File Name": r["file"],
                "Similarity (%)": r["similarity"],
                "Keyword Coverage (%)": r["coverage_percent"],
                "Missing Keywords": ", ".join(r["missing_keywords"]) if r["missing_keywords"] else "None"
            } for r in results])

            st.subheader("Resume Comparison Summary")
            st.dataframe(df)

            # ----------------------
            # Chart
            # ----------------------
            def get_color(score):
                if score >= 70:
                    return "High Match"
                elif score >= 40:
                    return "Medium Match"
                else:
                    return "Low Match"

            df["Match Level"] = df["Similarity (%)"].apply(get_color)

            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("File Name:N", sort=None),
                y=alt.Y("Similarity (%):Q"),
                color=alt.Color(
                    "Match Level:N",
                    scale=alt.Scale(
                        domain=["High Match", "Medium Match", "Low Match"],
                        range=["green", "orange", "red"]
                    )
                ),
                tooltip=["File Name", "Similarity (%)"]
            )

            st.altair_chart(chart, use_container_width=True)

            st.divider()

            # ----------------------
            # Detailed Ranking
            # ----------------------
            st.subheader("Detailed Resume Analysis (Ranked)")

            for rank, r in enumerate(sorted(results, key=lambda x: x["similarity"], reverse=True), start=1):
                with st.expander(f"Rank #{rank} — {r['file']}"):
                    st.write(f"Similarity: {r['similarity']:.2f}%")
                    st.write(f"Keyword Coverage: {r['coverage_percent']:.2f}%")

                    if r["missing_keywords"]:
                        st.write("Missing Keywords:")
                        for kw in r["missing_keywords"]:
                            st.write(f"- {kw}")
                    else:
                        st.success("All top keywords present ✅")

            # ----------------------
            # PDF Export
            # ----------------------
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)
            elements = []

            styles = getSampleStyleSheet()
            elements.append(Paragraph(f"Resume Match Report - Job {jd_index}", styles["Heading1"]))
            elements.append(Spacer(1, 0.3 * inch))

            for r in results:
                elements.append(Paragraph(f"{r['file']} - {r['similarity']:.2f}%", styles["Normal"]))
                elements.append(Spacer(1, 0.2 * inch))

            doc.build(elements)
            pdf_value = buffer.getvalue()
            buffer.close()

            st.download_button(
                label="Download PDF Report",
                data=pdf_value,
                file_name=f"resume_report_job{jd_index}.pdf",
                mime="application/pdf"
            )

        st.success("All analyses complete!")
