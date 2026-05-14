import re
from cv_agent.services.llm import ask_ai


def analyze_cv(cv_text, job_description):
    prompt = f"""
You are an expert HR recruiter and career coach.

Analyze the following CV against the provided job description.

IMPORTANT:
Start your answer exactly with:
Match Score: X%

Then continue with:
Skills Found:
Missing Skills:
Strengths:
Weaknesses:
Recommendations:

CV:
{cv_text[:3000]}

Job Description:
{job_description[:2000]}
"""

    response = ask_ai(prompt)
    return response


def get_match_score(report):
    match = re.search(r"Match Score:\s*(\d{1,3})\s*%", report, re.IGNORECASE)

    if match:
        score = int(match.group(1))
        return min(score, 100)

    return 75


def generate_interview_questions(cv_text, job_description):
    prompt = f"""
Generate 5 interview questions for this candidate based on the CV and job description.
Return the questions as a clean numbered list only.

CV:
{cv_text[:2500]}

Job Description:
{job_description[:1500]}
"""

    response = ask_ai(prompt)
    return response


def summarize_cv(cv_text):
    prompt = f"""
Summarize this CV professionally in short bullet points.

CV:
{cv_text[:2500]}
"""

    response = ask_ai(prompt)
    return response