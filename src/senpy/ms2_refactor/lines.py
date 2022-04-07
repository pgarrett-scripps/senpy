from abc import ABC
from dataclasses import dataclass
import numpy as np


@dataclass
class Line(ABC):
    pass


@dataclass
class HLine(Line):
    """
    Class for storing H line data

    Example H Line:
        H   [info]
    """

    info: str

    __slots__ = 'info'


@dataclass
class PeakLine(Line):

    mz: np.float32
    intensity: np.float32

    __slots__ = 'mz', 'intensity'


@dataclass
class ZLine(Line):
    """
    Class to store ZLine data

    Example Z_line:
        Z [low charge] [mass]
        Z	2	1887.9438
    """
    charge: np.uint8
    mass: np.float32

    __slots__ = 'charge', 'mass'


@dataclass
class ILine(Line):
    """
    Class to store ILine data

    Example I_line:
        I	[Keyword]	[Value]
        I	RetTime	1.3691
    """
    keyword: str
    value: str

    __slots__ = 'keyword', 'value'


@dataclass
class SLine(Line):
    """
    Class to store SLine data

    Example S_line:
        S [low scan] [high scan] [m/z]
        S	000009	000009	944.4755
    """

    low_scan: np.uint32
    high_scan: np.uint32
    mz: np.float32

    __slots__ = 'low_scan', 'high_scan', 'mz'

