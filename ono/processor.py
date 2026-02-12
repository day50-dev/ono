from unittest.mock import Mock


class Processor:
    def __init__(self, llm, context=None):
        self.llm = llm
        self.context = context

    def process(self, command: str, context=None):
        return self.llm.generate(command, context)
