from cv_agent.agents.parser_agent import ParserAgent
from cv_agent.agents.analyzer_agent import AnalyzerAgent
from cv_agent.agents.matcher_agent import MatcherAgent


class Orchestrator:
    """Coordinates the full CV analysis pipeline."""

    def __init__(self, use_rag: bool = True):
        self.parser = ParserAgent()
        self.analyzer = AnalyzerAgent(use_rag=use_rag)
        self.matcher = MatcherAgent()

    def run_single(self, cv_path: str, job_description: str, cv_id: str = None) -> dict:
        """Parse, store, and analyse a single CV."""
        cv_text = self.parser.run(cv_path, cv_id=cv_id)
        result = self.analyzer.run(cv_text, job_description)
        result["cv_text"] = cv_text
        result["cv_path"] = cv_path
        return result

    def run_batch(self, cv_paths: list[str], job_description: str) -> list[dict]:
        """Analyse multiple CVs and return them ranked by match score."""
        candidates = []
        for i, cv_path in enumerate(cv_paths):
            cv_id = f"candidate_{i + 1}"
            result = self.run_single(cv_path, job_description, cv_id=cv_id)
            result["candidate_id"] = cv_id
            candidates.append(result)
        return self.matcher.run(candidates)
