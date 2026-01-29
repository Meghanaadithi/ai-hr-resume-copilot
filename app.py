import streamlit as st
from utils import extract_text_from_pdf
from agents import resume_agent, jd_agent, matching_agent, qa_agent


if "candidate" not in st.session_state:
    st.session_state.candidate = None

if "job" not in st.session_state:
    st.session_state.job = None

if "match" not in st.session_state:
    st.session_state.match = None

st.set_page_config(
    page_title="AI HR Resume Copilot",
    layout="wide"
)

st.title("AI HR Resume Copilot")
st.caption("Upload a resume and job description to get structured, explainable recruiter insights.")

st.divider()


st.subheader("1. Upload Resume")

resume_file = st.file_uploader("Upload resume (PDF)", type=["pdf"])
resume_text_input = st.text_area(
    "Or paste resume text",
    height=200,
    placeholder="Paste resume text here..."
)

resume_text = ""

if resume_file:
    resume_text = extract_text_from_pdf(resume_file)
    st.success("Resume text extracted from PDF.")

elif resume_text_input.strip():
    resume_text = resume_text_input.strip()

if resume_text:
    with st.expander("Preview Resume Text"):
        st.write(resume_text[:3000])

if st.button(
    "Analyze Resume",
    use_container_width=True,
    disabled=not resume_text
):
    with st.spinner("Analyzing resume..."):
        st.session_state.candidate = resume_agent(resume_text)

    st.success("Resume analysis complete.")

if st.session_state.candidate:
    st.subheader("Candidate Profile")
    st.json(st.session_state.candidate)

st.divider()


st.subheader("2. Job Description")

jd_text = st.text_area(
    "Paste Job Description",
    height=220,
    placeholder="Paste the job description here..."
)

if st.button(
    "Match Resume to Job",
    use_container_width=True,
    disabled=not (resume_text and jd_text.strip())
):
    with st.spinner("Running matching analysis..."):

        if st.session_state.candidate is None:
            st.session_state.candidate = resume_agent(resume_text)

        if st.session_state.job is None:
            st.session_state.job = jd_agent(jd_text)

        st.session_state.match = matching_agent(
            st.session_state.candidate,
            st.session_state.job
        )

    st.success("Matching complete.")

if st.session_state.match:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Candidate")
        st.json(st.session_state.candidate)

    with col2:
        st.subheader("Job Requirements")
        st.json(st.session_state.job)

    with col3:
        st.subheader("Match Result")
        st.metric(
            "Match Score",
            f"{st.session_state.match['match_score']} / 100"
        )
        st.write("Decision:", st.session_state.match["decision"])

        st.write("Strengths:")
        for s in st.session_state.match["strengths"]:
            st.write("-", s)

        st.write("Gaps:")
        for g in st.session_state.match["gaps"]:
            st.write("-", g)

        st.write("Interview Questions:")
        for q in st.session_state.match["interview_questions"]:
            st.write("-", q)

st.divider()


st.subheader("3. Recruiter Q&A Copilot")

question = st.text_input(
    "Ask a recruiter-style question",
    placeholder="e.g. Is this candidate a good fit for backend-heavy roles?"
)

if st.button(
    "Ask Copilot",
    disabled=not (
        question.strip()
        and st.session_state.candidate
        and st.session_state.job
    )
):
    with st.spinner("Thinking like a recruiter..."):
        answer = qa_agent(
            question,
            st.session_state.candidate,
            st.session_state.job
        )

    st.success("Answer ready.")

    st.write("Answer:", answer["answer"])
    st.write("Confidence:", answer["confidence"])
    st.write("Evidence:")
    for e in answer["evidence"]:
        st.write("-", e)
