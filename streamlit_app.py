import streamlit as st
import pandas as pd
import plotly.express as px
from parser import extract_text_from_bytes
from matcher import rank_resumes

st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

st.title("AI Resume Screener")
st.caption("Upload a job description and multiple resumes. Get instant match scores and skill analysis.")

st.divider()

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Job Description")
    jd_input_mode = st.radio("Input mode", ["Paste text", "Upload file"], horizontal=True)
    jd_text = ""
    if jd_input_mode == "Paste text":
        jd_text = st.text_area("Paste the job description here", height=300, placeholder="We are looking for a Python developer with experience in machine learning...")
    else:
        jd_file = st.file_uploader("Upload JD (PDF or DOCX)", type=["pdf", "docx"])
        if jd_file:
            jd_text = extract_text_from_bytes(jd_file.read(), jd_file.name)
            st.success("Job description loaded.")
            with st.expander("Preview extracted text"):
                st.text(jd_text[:1000] + "...")

with col2:
    st.subheader("Resumes")
    resume_files = st.file_uploader(
        "Upload resumes (PDF or DOCX) — multiple allowed",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

st.divider()

if st.button("Screen Resumes", type="primary", disabled=(not jd_text or not resume_files)):
    resumes = []
    with st.spinner("Parsing resumes..."):
        for f in resume_files:
            try:
                text = extract_text_from_bytes(f.read(), f.name)
                resumes.append({"name": f.name, "text": text})
            except Exception as e:
                st.warning(f"Could not parse {f.name}: {e}")

    if not resumes:
        st.error("No resumes could be parsed. Please check your files.")
        st.stop()

    with st.spinner("Analysing and ranking..."):
        results = rank_resumes(jd_text, resumes)

    st.success(f"Screened {len(results)} resume(s) successfully!")

    top = results[0]
    m1, m2, m3 = st.columns(3)
    m1.metric("Top candidate", top["Candidate"].replace(".pdf","").replace(".docx",""))
    m2.metric("Top match score", f"{top['score']}%")
    m3.metric("Resumes screened", len(results))

    st.divider()

    st.subheader("Ranked candidates")
    df = pd.DataFrame(results)[["Rank", "Candidate", "score", "skill_score", "cosine_score"]]
    df.columns = ["Rank", "Candidate", "Overall Score (%)", "Skill Match (%)", "Content Match (%)"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("Score comparison")
    fig = px.bar(
        df.sort_values("Overall Score (%)"),
        x="Overall Score (%)",
        y="Candidate",
        orientation="h",
        color="Overall Score (%)",
        color_continuous_scale="teal",
        text="Overall Score (%)"
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False, plot_bgcolor="rgba(0,0,0,0)")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Candidate skill breakdown")
    for r in results:
        with st.expander(f"#{r['Rank']} — {r['Candidate']}  |  Score: {r['score']}%"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Matched skills**")
                if r["matched_skills"]:
                    for s in r["matched_skills"]:
                        st.success(f"✓ {s}")
                else:
                    st.info("No skills matched.")
            with c2:
                st.markdown("**Missing skills**")
                if r["missing_skills"]:
                    for s in r["missing_skills"]:
                        st.error(f"✗ {s}")
                else:
                    st.info("All required skills present!")

    st.divider()
    export_df = pd.DataFrame(results).drop(columns=["jd_skills", "resume_skills"])
    csv = export_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download results as CSV", csv, "screening_results.csv", "text/csv")