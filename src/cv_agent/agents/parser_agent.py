from cv_agent.agents.base_agent import BaseAgent
from cv_agent.services.parser import parse_cv
from cv_agent.services.vector_store import add_cv


class ParserAgent(BaseAgent):
    def __init__(self):
        super().__init__("ParserAgent")

    def run(self, cv_path: str, cv_id: str = None, metadata: dict = None) -> str:
        """Parse a CV file and optionally store it in the vector database."""
        self._log(f"Parsing {cv_path}")
        cv_text = parse_cv(cv_path)

        if cv_id:
            self._log(f"Storing CV '{cv_id}' in vector database")
            add_cv(cv_id, cv_text, metadata or {})

        return cv_text
