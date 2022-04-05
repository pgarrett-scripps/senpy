class DTASelectFilterDeserializationPeptideLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Error deserializing UniqueLine: '{self.line}'"

class DTASelectFilterDeserializationProteinLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Error deserializing UniqueLine: '{self.line}'"