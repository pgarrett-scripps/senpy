from dataclasses import dataclass
from typing import List, Dict, Union
import numpy as np

from . import exceptions as ms2_exceptions
from .columns import PeakLineColumns, ZLineColumns, ILineColumns, SLineColumns
from .lines import ILine as ms2_ILine, Ms2Spectra


@dataclass
class PeakLine:
    """
    Class for keeping track of peak lines

    Example Z_line:
        [mz] [intensity]
        982.1023	120.0
    """

    line: str

    def get_mz(self):
        line_elements = self.line.rstrip().split(" ")
        return line_elements[PeakLineColumns.mz.value]

    def get_intensity(self):
        line_elements = self.line.rstrip().split(" ")
        return line_elements[PeakLineColumns.intensity.value]

    def serialize(self) -> str:
        return self.line

    @staticmethod
    def deserialize(line: str) -> 'PeakLine':
        return PeakLine(line)


@dataclass
class HLine:
    """
    Class for storing H line Information

    Example H Line:
        H   [info]
    """

    line: str

    def get_info(self):
        line_elements = self.line.rstrip().split("\t")
        return "\t".join(line_elements[1:])

    def serialize(self) -> str:
        return self.line

    @staticmethod
    def deserialize(line: str) -> 'HLine':
        return HLine(line)


@dataclass
class ZLine:
    """
    Class keeping track of ms2 Z lines

    Example Z_line:
        Z [low charge] [mass]
        Z	2	1887.9438
    """
    line: str

    def get_charge(self):
        line_elements = self.line.rstrip().split("\t")
        return line_elements[ZLineColumns.charge.value]

    def get_mass(self):
        line_elements = self.line.rstrip().split("\t")
        return line_elements[ZLineColumns.mass.value]

    def serialize(self) -> str:
        return self.line

    @staticmethod
    def deserialize(line: str) -> 'ZLine':
        return ZLine(line)


@dataclass
class ILine:
    """
    Class keeping track of ms2 I lines.

    Example I_line:
        I	Keyword	Value
        I	TIMSTOF_Parent_ID	8
        I	TIMSTOF_Precursor_ID	1
        I	RetTime	1.3691
    """
    line: str

    def get_keyword(self):
        line_elements = self.line.rstrip().split("\t")
        return line_elements[ILineColumns.keyword.value]

    def get_value(self):
        line_elements = self.line.rstrip().split("\t")
        return line_elements[ILineColumns.val.value]

    def serialize(self) -> str:
        return self.line

    @staticmethod
    def deserialize(line: str) -> 'ILine':
        return ILine(line)

@dataclass
class SLine:
    """
    Class keeping track of ms2 S lines.

    Example S_line:
        S [low scan] [high scan] [m/z]
        S	000009	000009	944.4755
    """

    line: str

    def get_low_scan(self):
        line_elements = self.line.rstrip().split("\t")
        return line_elements[SLineColumns.low_scan.value]

    def get_high_scan(self):
        line_elements = self.line.rstrip().split("\t")
        return line_elements[SLineColumns.high_scan.value]

    def get_mz(self):
        line_elements = self.line.rstrip().split("\t")
        return line_elements[SLineColumns.mz.value]

    def serialize(self) -> str:
        return self.line

    @staticmethod
    def deserialize(line: str) -> 'SLine':
        return SLine(line)

@dataclass
class Ms2SpectraFast(Ms2Spectra):
    """
    Dataclass tp store Ms2Spectra Line Types. Each Ms2Spectra contains:
        1 SLine
        0 or more ILines
        1 ZLine
        0 or more PeakLines
    """

    s_line: SLine
    i_lines: List[ILine]
    z_line: ZLine
    peak_lines: List[PeakLine]
    i_line_dict = None

    def get_mz_spectra(self):
        return [peak_line.get_mz() for peak_line in self.peak_lines]

    def get_intensity_spectra(self):
        return [peak_line.get_intensity() for peak_line in self.peak_lines]

    def get_i_line_dict(self):
        return {i_line.get_keyword(): i_line.get_value() for i_line in self.i_lines}

    def get_i_line_value(self, keyword) -> Union[str, None]:
        if self.i_line_dict is None:
            self.i_line_dict = self.get_i_line_dict()
        if keyword in self.i_line_dict:
            return self.i_line_dict[keyword]
        return None

    @staticmethod
    def create(low_scan: int, high_scan: int, mz: float, charge: int, mass: float, mz_spectra: np.ndarray,
               intensity_spectra: np.ndarray, info_dict: Dict[str, str]) -> 'Ms2Spectra':
        pass


def parse_ms2_line(line: str) -> Union[HLine, SLine, ILine, ZLine, PeakLine]:
    """
    Returns the appropriate Ms2 Line object or throws error
    """
    if line[0] == 'H':
        return HLine(line)
    elif line[0] == 'S':
        return SLine(line)
    elif line[0] == 'I':
        return ILine(line)
    elif line[0] == 'Z':
        return ZLine(line)
    elif line[0].isnumeric():
        return None #PeakLine(line)
    else:
        raise ms2_exceptions.Ms2FileDeserializationUnsupportedLineException
