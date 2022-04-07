class Ms2FileDeserializationPeakLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Error deserializing Peak-line: '{self.line}'"


class Ms2FileDeserializationZLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Error deserializing Z-line: '{self.line}'"


class Ms2FileDeserializationILineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Error deserializing I-line: '{self.line}'"


class Ms2FileDeserializationSLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Error deserializing S-line: '{self.line}'"


class Ms2FileDeserializationUnsupportedLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Unsupported ms2 line type: '{self.line}'"
