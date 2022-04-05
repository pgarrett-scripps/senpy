from abc import ABC, abstractmethod
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



