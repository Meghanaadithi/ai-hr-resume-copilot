# AI HR Resume Copilot

An AI-powered HR Copilot designed to assist recruiters by analyzing resumes, extracting job requirements, scoring candidate–job fit, and answering recruiter-style follow-up questions using agentic Large Language Model (LLM) workflows.

The system focuses on explainability and decision support rather than acting as a generic chatbot.

---

## Live Demo

https://ai-hr-resume-copilot-fzzk9uwgpfwupje6w4j88d.streamlit.app

Recruiters can upload a resume (PDF or text), paste a job description, view explainable match scores, identify strengths and gaps, and ask contextual recruiter-style questions.

---

## Features

- Resume parsing from PDF or text input
- Job description analysis and requirement extraction
- Explainable candidate–job match scoring
- Identification of strengths, gaps, and risks
- Interview question generation based on gaps
- Recruiter Q&A copilot with grounded responses
- Structured JSON outputs for reliability and interpretability

---

## Architecture Overview

The application is built using an agent-based design where each LLM call has a clearly defined responsibility.

**Agent Workflow:**
1. Resume Agent → extracts structured candidate information
2. Job Description Agent → extracts structured job requirements
3. Matching Agent → compares candidate and job data to generate a match score and reasoning
4. Recruiter Q&A Agent → answers recruiter questions using only provided context

This modular design improves clarity, debuggability, and extensibility.

---

## Large Language Model (LLM) Usage

This application is powered by OpenAI’s `gpt-4o-mini`, a lightweight, production-optimized Large Language Model (LLM) designed for low-latency and cost-efficient inference.

The LLM is used as a reasoning engine rather than a conversational chatbot. Each interaction is constrained to return structured JSON outputs, enabling deterministic behavior and reliable downstream processing.

The model is leveraged through multiple specialized agents:
- Resume Agent: extracts structured candidate information from unstructured resume text
- Job Description Agent: parses and categorizes job requirements from raw job descriptions
- Matching Agent: performs comparative reasoning between candidate profiles and job requirements to generate explainable match scores
- Recruiter Q&A Agent: answers recruiter-style questions using only the provided candidate and job context

This agent-based design improves explainability, modularity, and reliability, making the system suitable for real-world decision-support workflows.

---

## Tech Stack

- Programming Language: Python
- Frontend: Streamlit
- AI / NLP: OpenAI API (`gpt-4o-mini`)
- Environment Management: python-dotenv
- Document Parsing: pypdf
- Deployment: Streamlit Cloud

---

## Design Rationale

The system is intentionally designed as a copilot rather than a fully autonomous decision-maker. All outputs are explainable, structured, and intended to support human judgment rather than replace it.

This design aligns with how AI systems are realistically adopted in production HR and recruiting workflows.

---

## Security and Configuration

- API keys are not stored in the repository
- Sensitive credentials are managed using Streamlit Secrets
- Environment variables are excluded via `.gitignore`

---

## Future Enhancements

- Multi-resume comparison
- Role-based weighting of skills
- Exportable recruiter reports
- Support for additional LLM providers or local models

---

Built by **Meghana Adithi**
