class BaseAgent:
    def __init__(self, name):
        self.name = name

    def log(self, message):
        print(f"[{self.name}] {message}")

    def run(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement run()")