from dataclasses import dataclass

import numpy as np

from senpy.ms2_refactor.lines import PeakLine, HLine, ZLine, ILine, SLine
from senpy.ms2_refactor.columns import _PeakLineColumns, _ZLineColumns, _ILineColumns, _SLineColumns
from senpy.ms2_refactor import exceptions as ms2_exceptions


@dataclass
class PeakLineSerializer:

    MZ_PRECISION: int = 5
    INTENSITY_PRECISION: int = 1

    def serialize(self, line: PeakLine):
        line_elements = [None] * len(_PeakLineColumns)
        line_elements[_PeakLineColumns.mz.value] = self.serialize_mz(line.mz, self.MZ_PRECISION)
        line_elements[_PeakLineColumns.intensity.value] = self.serialize_intensity(line.intensity,
                                                                                   self.INTENSITY_PRECISION)
        return ' '.join(line_elements) + '\n'

    @staticmethod
    def deserialize(line: str) -> 'PeakLine':
        line_elements = line.rstrip().split(" ")
        if len(line_elements) != len(_PeakLineColumns):
            raise ms2_exceptions.Ms2FileDeserializationPeakLineException(_line=line)

        mz = np.float32(line_elements[_PeakLineColumns.mz.value])
        intensity = np.float32(line_elements[_PeakLineColumns.intensity.value])

        peak_line = PeakLine(mz, intensity)
        return peak_line

    @staticmethod
    def serialize_mz(mz, precision):
        return f"{mz:.{precision}f}"

    @staticmethod
    def serialize_intensity(intensity, precision):
        return f"{intensity:.{precision}f}"

@dataclass
class HLineSerializer:

    def serialize(self) -> str:
        line_elements = ["H",
                         self.info
                         ]
        return '\t'.join(line_elements) + '\n'

    @staticmethod
    def deserialize(line: str) -> 'HLine':
        line_elements = line.rstrip().split("\t")
        return HLine("\t".join(line_elements[1:]))


@dataclass
class ZLineSerializer:

    MASS_PRECISION: int = 5

    def serialize(self) -> str:
        line_elements = [None]*len(_ZLineColumns)
        line_elements[_ZLineColumns.letter.value] = "Z"
        line_elements[_ZLineColumns.charge.value] = self.serialize_charge(self.charge)
        line_elements[_ZLineColumns.mass.value] = self.serialize_mass(self.mass, self.MASS_PRECISION)
        return '\t'.join(line_elements) + '\n'

    @staticmethod
    def deserialize(line: str) -> 'ZLine':
        line_elements = line.rstrip().split("\t")

        if len(line_elements) != len(_ZLineColumns):
            raise ms2_exceptions.Ms2FileDeserializationZLineException(_line=line)

        charge = np.uint8(line_elements[_ZLineColumns.charge.value])
        mass = np.float32(line_elements[_ZLineColumns.mass.value])

        return ZLine(charge, mass)

    @staticmethod
    def serialize_charge(charge):
        return f"{charge}"

    @staticmethod
    def serialize_mass(mass, precision):
        return f"{mass:.{precision}f}"


@dataclass
class ILineSerializer:

    def serialize(self) -> str:
        line_elements = [None]*len(_ILineColumns)
        line_elements[_ILineColumns.letter.value] = "I"
        line_elements[_ILineColumns.keyword.value] = self.keyword
        line_elements[_ILineColumns.value.value] = self.value
        return '\t'.join(line_elements) + '\n'

    @staticmethod
    def deserialize(line: str) -> 'ILine':
        line_elements = line.rstrip().split("\t")

        if len(line_elements) != len(_ILineColumns):
            raise ms2_exceptions.Ms2FileDeserializationILineException(_line=line)

        keyword = line_elements[_ILineColumns.keyword.value]
        value = line_elements[_ILineColumns.value.value]

        return ILine(keyword, value)


@dataclass
class SLineSerializer:

    LOW_SCAN_LENGTH: int = 6
    HIGH_SCAN_LENGTH: int = 6
    MZ_PRECISION: int = 5

    @staticmethod
    def deserialize(line: str) -> 'SLine':
        line_elements = line.rstrip().split("\t")

        if len(line_elements) != len(_SLineColumns):
            raise ms2_exceptions.Ms2FileDeserializationSLineException(_line=line)

        low_scan = int(line_elements[_SLineColumns.low_scan.value])
        high_scan = int(line_elements[_SLineColumns.high_scan.value])
        mz = float(line_elements[_SLineColumns.mz.value])

        return SLine(low_scan, high_scan, mz)

    def serialize(self):
        line_elements = [None] * len(_SLineColumns)
        line_elements[_SLineColumns.letter.value] = "S"
        line_elements[_SLineColumns.low_scan.value] = self.serialize_low_scan(self.low_scan, SLine.LOW_SCAN_LENGTH)
        line_elements[_SLineColumns.high_scan.value] = self.serialize_high_scan(self.high_scan, SLine.HIGH_SCAN_LENGTH)
        line_elements[_SLineColumns.mz.value] = self.serialize_mz(self.mz, SLine.MZ_PRECISION)
        return '\t'.join(line_elements) + '\n'

    @staticmethod
    def serialize_low_scan(low_scan, max_length):
        return f"{low_scan:0{max_length}d}"

    @staticmethod
    def serialize_high_scan(high_scan, max_length):
        return f"{high_scan:0{max_length}d}"

    @staticmethod
    def serialize_mz(mz, precision):
        return f"{mz:.{precision}f}"