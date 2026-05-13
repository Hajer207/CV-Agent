from agents.base_agent import BaseAgent


class MatcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="MatcherAgent")

    def run(self, results):
        ranked_results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked_results