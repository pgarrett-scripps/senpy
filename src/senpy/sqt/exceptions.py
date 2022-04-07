class SqtFileDeserializationSLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Error deserializing S-line: '{self.line}'"


class SqtFileDeserializationMLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Error deserializing M-line: '{self.line}'"


class SqtFileDeserializationLLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Error deserializing L-line: '{self.line}'"


class SqtFileDeserializationUnsupportedLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Unsupported sqt line type: '{self.line}'"