from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Union


class Line(ABC):

    @staticmethod
    @abstractmethod
    def deserialize(line: str):
        pass

    @abstractmethod
    def serialize(self) -> str:
        pass


# Being Phased out
class LineSerializer(ABC):
    @abstractmethod
    def deserialize(self, line: str):
        pass

    @abstractmethod
    def serialize(self, line: Line) -> str:
        pass


def cast_float(val: Any) -> Union[float, None]:
    return float(val) if val else None


def cast_int(val: Any) -> Union[int, None]:
    return int(val) if val else None


def cast_str(val: Any) -> Union[str, None]:
    return str(val) if val else None


def serialize_float(val, precision):
    return f"{val:.{precision}f}"


@dataclass
class HLine(Line):
    """
    Class for storing H line Information

    Example H Line:
        H   [info]
    """

    LETTER = "H"
    info: str

    __slots__ = 'info'

    @staticmethod
    def deserialize(line: str, version=None) -> 'HLine':
        line_elements = line.rstrip().split("\t")
        return HLine("\t".join(line_elements[1:]))

    def serialize(self, version=None) -> str:
        line_elements = ["H",
                         self.info
                         ]
        return '\t'.join(line_elements) + '\n'



