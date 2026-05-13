from agents.parser_agent import ParserAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.matcher_agent import MatcherAgent


class Orchestrator:
    def __init__(self, use_rag=False):
        self.use_rag = use_rag
        self.parser_agent = ParserAgent()
        self.analyzer_agent = AnalyzerAgent(use_rag=use_rag)
        self.matcher_agent = MatcherAgent()

    def run_single(self, cv_path, job_description, cv_id="uploaded_cv"):
        cv_text = self.parser_agent.run(cv_path)

        result = self.analyzer_agent.run(
            cv_text=cv_text,
            job_description=job_description,
            cv_id=cv_id
        )

        return result

    def run_batch(self, cv_paths, job_description):
        results = []

        for cv_path in cv_paths:
            cv_text = self.parser_agent.run(cv_path)

            result = self.analyzer_agent.run(
                cv_text=cv_text,
                job_description=job_description,
                cv_id=cv_path
            )

            results.append(result)

        ranked_results = self.matcher_agent.run(results)

        return ranked_results