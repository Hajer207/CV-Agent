from cv_agent.agents.base_agent import BaseAgent
from cv_agent.services.parser import parse_cv


class ParserAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ParserAgent")

    def run(self, cv_path):
        self.log(f"Parsing CV: {cv_path}")

        cv_text = parse_cv(cv_path)

        return cv_text