import streamlit as st
from utils import extract_text_from_pdf
from agents import resume_agent, jd_agent, matching_agent, qa_agent

st.set_page_config(
    page_title="AI HR Resume Copilot",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI HR Resume Copilot")
st.caption("Upload a resume → get structured AI insights for recruiters.")

st.divider()

# Resume upload section
st.subheader("1️⃣ Upload Resume")

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

st.divider()

# Run Resume Agent
if st.button("🔍 Analyze Resume with AI", use_container_width=True, disabled=not resume_text):
    with st.spinner("Running Resume Agent..."):
        result = resume_agent(resume_text)

    st.success("Analysis complete!")

    st.subheader("🧾 Candidate Profile (Structured Output)")
    st.json(result)

st.divider()
st.subheader("2️⃣ Job Description")

jd_text = st.text_area(
    "Paste Job Description",
    height=220,
    placeholder="Paste the job description here..."
)

st.divider()

if st.button(
    "📊 Match Resume to Job",
    use_container_width=True,
    disabled=not (resume_text and jd_text.strip())
):
    with st.spinner("Analyzing resume and job description..."):
        candidate = resume_agent(resume_text)
        job = jd_agent(jd_text)
        match = matching_agent(candidate, job)

    st.success("Matching complete!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Candidate Profile")
        st.json(candidate)

    with col2:
        st.subheader("Job Requirements")
        st.json(job)

    with col3:
        st.subheader("Match Result")
        st.metric("Match Score", f"{match['match_score']} / 100")
        st.write("**Decision:**", match["decision"])

        st.write("**Strengths:**")
        for s in match["strengths"]:
            st.write("•", s)

        st.write("**Gaps:**")
        for g in match["gaps"]:
            st.write("•", g)

        st.write("**Interview Questions:**")
        for q in match["interview_questions"]:
            st.write("•", q)


st.divider()
st.subheader("3️⃣ Recruiter Q&A Copilot")

question = st.text_input(
    "Ask a recruiter-style question",
    placeholder="e.g. Is this candidate strong in backend systems?"
)

if st.button(
    "💬 Ask Copilot",
    disabled=not (question.strip() and resume_text and jd_text.strip())
):
    with st.spinner("Thinking like a recruiter..."):
        candidate = resume_agent(resume_text)
        job = jd_agent(jd_text)
        answer = qa_agent(question, candidate, job)

    st.success("Answer ready!")

    st.write("**Answer:**", answer["answer"])
    st.write("**Confidence:**", answer["confidence"])
    st.write("**Evidence:**")
    for e in answer["evidence"]:
        st.write("•", e)

