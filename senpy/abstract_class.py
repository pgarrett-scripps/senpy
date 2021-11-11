from abc import ABC, abstractmethod

class Line(ABC):
    pass


class LineSerializer(ABC):

    @staticmethod
    @abstractmethod
    def serialize(line: Line) -> str:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(line: str) -> Line:
        pass
