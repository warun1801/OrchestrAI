class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.memory = {}

    def run(self, state):
        """
        Runs the agent's main logic.
        Returns updated state.
        Can call other agents or tools.
        """
        raise NotImplementedError
