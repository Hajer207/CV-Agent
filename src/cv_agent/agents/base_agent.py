from abc import ABC, abstractmethod


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def _log(self, message: str) -> None:
        print(f"[{self.name}] {message}")
