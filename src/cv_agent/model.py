import re

from services.llm import ask_ai


def analyze_cv(cv_text, job_description):
    prompt = f"""
You are an expert HR recruiter and career coach.

Analyze the following CV against the provided job description.

Return:
1. Match Score (0-100)
2. Skills Found
3. Missing Skills
4. Strengths
5. Weaknesses
6. Recommendations

CV:
{cv_text[:3000]}

Job Description:
{job_description[:2000]}
"""

    response = ask_ai(prompt)

    return response


def get_match_score(report):
    match = re.search(r'(\d{1,3})', report)

    if match:
        score = int(match.group(1))

        if score > 100:
            score = 100

        return score

    return 75


def generate_interview_questions(cv_text, job_description):
    prompt = f"""
Generate 5 interview questions for this candidate based on the CV and job description.

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