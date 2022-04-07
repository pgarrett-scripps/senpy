from enum import Enum


class PeakLineColumns(Enum):
    mz = 0
    intensity = 1


class ZLineColumns(Enum):
    letter = 0
    charge = 1
    mass = 2


class ILineColumns(Enum):
    letter = 0
    keyword = 1
    val = 2


class SLineColumns(Enum):
    letter = 0
    low_scan = 1
    high_scan = 2
    mz = 3