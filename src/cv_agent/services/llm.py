from openai import OpenAI

client = OpenAI(api_key="demo")


def ask_ai(prompt: str):
    return """
Match Score: 87%

Skills Found:
- Python
- SQL
- Power BI
- Data Analysis

Missing Skills:
- Cloud Deployment
- Machine Learning

Strengths:
Strong analytical background and relevant technical skills.

Weaknesses:
The CV could include more quantified achievements.

Recommendations:
Improve measurable outcomes and tailor the summary to the role.
"""