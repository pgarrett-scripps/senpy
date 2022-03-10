from abc import ABC, abstractmethod


class Line(ABC):

    @staticmethod
    @abstractmethod
    def deserialize(line: str):
        pass

    @abstractmethod
    def serialize(self) -> str:
        pass
