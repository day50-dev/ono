class OnoBlock:
    def __init__(self, content):
        self.content = content

class Variable:
    def __init__(self, identifier):
        self.identifier = identifier

class FunctionCall:
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments

class Expression:
    def __init__(self, expression):
        self.expression = expression

class Text:
    def __init__(self, value):
        self.value = value