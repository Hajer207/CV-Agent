from agents.base_agent import BaseAgent
from model import (
    analyze_cv,
    get_match_score,
    generate_interview_questions
)


class AnalyzerAgent(BaseAgent):
    def __init__(self, use_rag=False):
        super().__init__(name="AnalyzerAgent")
        self.use_rag = use_rag

    def run(self, cv_text, job_description, cv_id="uploaded_cv"):
        self.log("Analyzing CV...")

        report = analyze_cv(
            cv_text=cv_text,
            job_description=job_description
        )

        score = get_match_score(report)

        questions = generate_interview_questions(
            cv_text=cv_text,
            job_description=job_description
        )

        return {
            "cv_id": cv_id,
            "score": score,
            "report": report,
            "interview_questions": questions
        }