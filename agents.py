import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_JSON_ONLY = (
    "You are a helpful assistant. "
    "Return ONLY valid JSON. "
    "Do not include markdown, explanations, or extra text."
)

def resume_agent(resume_text: str) -> dict:
    prompt = f"""
Extract a structured candidate profile from the resume text.

Include:
- name (string or null)
- email (string or null)
- core_skills (list of strings)
- tools (list of strings)
- domains (list of strings)
- years_experience (number or null)
- recent_titles (list of strings)
- summary (2–3 lines)

RESUME_TEXT:
{resume_text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_JSON_ONLY},
            {"role": "user", "content": prompt},
        ],
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON:\n{content}")

def jd_agent(jd_text: str) -> dict:
    prompt = f"""
Extract structured job requirements from the job description.

Include:
- role_title
- must_have_skills (list)
- nice_to_have_skills (list)
- responsibilities (list)
- seniority_level (Junior / Mid / Senior / Unknown)

JOB_DESCRIPTION:
{jd_text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_JSON_ONLY},
            {"role": "user", "content": prompt},
        ],
    )

    content = response.choices[0].message.content.strip()
    return json.loads(content)


def matching_agent(candidate: dict, job: dict) -> dict:
    prompt = f"""
Compare the candidate profile and job requirements.

Return:
- match_score (0–100)
- decision (Strong Yes / Yes / Maybe / No)
- strengths (list)
- gaps (list)
- interview_questions (list)

CANDIDATE_PROFILE:
{json.dumps(candidate)}

JOB_REQUIREMENTS:
{json.dumps(job)}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_JSON_ONLY},
            {"role": "user", "content": prompt},
        ],
    )

    content = response.choices[0].message.content.strip()
    return json.loads(content)

def qa_agent(question: str, candidate: dict, job: dict) -> dict:
    prompt = f"""
You are an HR Copilot.

Answer the recruiter question using ONLY the candidate profile and job requirements.
If information is missing, say so clearly.

Return:
- answer
- confidence (Low / Medium / High)
- evidence (list)

QUESTION:
{question}

CANDIDATE_PROFILE:
{json.dumps(candidate)}

JOB_REQUIREMENTS:
{json.dumps(job)}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_JSON_ONLY},
            {"role": "user", "content": prompt},
        ],
    )

    content = response.choices[0].message.content.strip()
    return json.loads(content)

