import re
from cv_agent.services.llm import ask_ai


def analyze_cv(cv_text: str, job_description: str, rag_context: str = "") -> str:
    context_block = ""
    if rag_context:
        context_block = f"""
---
Reference Candidates from Database (for context only):
{rag_context}
"""

    prompt = f"""Analyze the following CV against the Job Description and provide a detailed report.
{context_block}
---
CV:
{cv_text}

---
Job Description:
{job_description}

---
Your report must include exactly these sections:

1. Match Score: A percentage (0-100%) showing how well the CV matches the job.

2. Skills Found: List the relevant skills the candidate already has.

3. Missing Skills: List the important skills required by the job but missing from the CV.

4. Strengths: What makes this candidate stand out for this role.

5. Weaknesses: Areas where the candidate falls short.

6. Recommendations: Specific advice to improve the CV for this job.

7. Interview Questions: 5 questions the interviewer might ask this candidate based on their CV and the job.

Be clear, structured, and professional.
"""
    return ask_ai(prompt)


def generate_interview_questions(
    cv_text: str,
    job_description: str,
    num_questions: int = 10,
) -> str:
    prompt = f"""Based on the CV and Job Description below, generate {num_questions} targeted interview questions.

CV:
{cv_text}

Job Description:
{job_description}

Organise the questions into these categories:
- Technical Skills (3-4 questions): Test specific tools, languages, or frameworks required.
- Experience & Background (2-3 questions): Explore past projects and accomplishments.
- Behavioral (2-3 questions): Assess soft skills using the STAR method.
- Culture Fit (1-2 questions): Gauge alignment with company values.

Make every question specific to this candidate's background and the job requirements.
"""
    return ask_ai(prompt)


def get_match_score(analysis_report: str) -> int:
    """Extract the numeric match score from an analysis report."""
    match = re.search(r'Match Score[:\s]+(\d{1,3})', analysis_report, re.IGNORECASE)
    if match:
        return min(int(match.group(1)), 100)
    return 0


def summarize_cv(cv_text: str) -> str:
    prompt = f"""Summarize the following CV in 3-5 bullet points highlighting the candidate's key qualifications, experience, and skills.

CV:
{cv_text}

Keep the summary concise and professional.
"""
    return ask_ai(prompt)
