from cv_agent.agents.base_agent import BaseAgent


class MatcherAgent(BaseAgent):
    def __init__(self):
        super().__init__("MatcherAgent")

    def run(self, candidates: list[dict]) -> list[dict]:
        """Rank a list of candidate result dicts by match score (highest first)."""
        self._log(f"Ranking {len(candidates)} candidates")
        return sorted(candidates, key=lambda c: c.get("score", 0), reverse=True)
