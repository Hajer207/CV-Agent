from cv_agent.agents.base_agent import BaseAgent
from cv_agent.model import analyze_cv, generate_interview_questions, get_match_score
from cv_agent.services.vector_store import get_rag_context


class AnalyzerAgent(BaseAgent):
    def __init__(self, use_rag: bool = True):
        super().__init__("AnalyzerAgent")
        self.use_rag = use_rag

    def run(self, cv_text: str, job_description: str) -> dict:
        """Analyze a CV against a job description and return a result dict."""
        rag_context = ""
        if self.use_rag:
            self._log("Fetching RAG context from vector database")
            rag_context = get_rag_context(job_description)

        self._log("Analyzing CV with AI")
        report = analyze_cv(cv_text, job_description, rag_context)
        score = get_match_score(report)

        self._log("Generating interview questions")
        questions = generate_interview_questions(cv_text, job_description)

        return {
            "report": report,
            "score": score,
            "interview_questions": questions,
        }
