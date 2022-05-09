import ast
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Union
import numpy as np

from ..ms2 import exceptions as ms2_exceptions
from ..ms2.columns import PeakLineColumns, ZLineColumns, ILineColumns, SLineColumns
from ..ms2.lines import ILine as ms2_ILine


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


@dataclass
class Ms2Spectra:
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

    def get_parent_id(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ms2_ILine.PARENT_ID_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def get_precursor_id(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ms2_ILine.PRECURSOR_ID_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def get_retention_time(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ms2_ILine.RETENTION_TIME_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def get_collision_energy(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ms2_ILine.COLLISION_ENERGY_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def get_ook0(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ms2_ILine.OOK0_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def get_ccs(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ms2_ILine.CCS_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def get_precursor_intensity(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ms2_ILine.PRECURSOR_INTENSITY_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def get_ook0_spectra(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ms2_ILine.OOK0_SPECTRA_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def get_ccs_spectra(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ms2_ILine.CCS_SPECTRA_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def get_mobility_intensity_spectra(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ms2_ILine.INTENSITY_SPECTRA_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def get_mobility_mz_spectra(self, keyword=None) -> Union[List[float], None]:
        if keyword is None:
            keyword = ms2_ILine.MZ_SPECTRA_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def serialize(self) -> str:
        lines = [self.s_line] + self.i_lines + [self.z_line] + self.peak_lines
        return ''.join([line.serialize() for line in lines])

    @staticmethod
    def create(low_scan: int, high_scan: int, mz: float, charge: int, mass: float, mz_spectra: np.ndarray,
               intensity_spectra: np.ndarray, info_dict: Dict[str, str]) -> 'Ms2Spectra':
        s_line = SLine(low_scan=low_scan, high_scan=high_scan, mz=mz)
        i_lines = [ILine(keyword=key, value=value) for key, value in info_dict.items()]
        z_line = ZLine(charge=charge, mass=mass)
        peak_lines = [PeakLine(mz=mz, intensity=intensity) for mz, intensity in zip(mz_spectra, intensity_spectra)]
        precursor_spectra = Ms2Spectra(s_line=s_line, i_lines=i_lines, z_line=z_line, peak_lines=peak_lines)
        return precursor_spectra


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
