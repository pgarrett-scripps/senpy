import ast
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Union, ClassVar
import numpy as np

from senpy.ms2 import exceptions as ms2_exceptions
from senpy.util import Line


class _PeakLineColumns(Enum):
    mz = 0
    intensity = 1


@dataclass
class PeakLine(Line):
    """
    Class for keeping track of peak lines

    Example Z_line:
        [mz] [intensity]
        982.1023	120.0
    """

    mz: np.float32
    intensity: np.float32

    MZ_PRECISION: ClassVar[int] = 5
    INTENSITY_PRECISION: ClassVar[int] = 1

    __slots__ = 'mz', 'intensity'

    @staticmethod
    def deserialize(line: str) -> 'PeakLine':
        line_elements = line.rstrip().split(" ")
        if len(line_elements) != len(_PeakLineColumns):
            raise ms2_exceptions.Ms2FileDeserializationPeakLineException(_line=line)
        mz = np.float32(line_elements[_PeakLineColumns.mz.value])
        intensity = np.float32(line_elements[_PeakLineColumns.intensity.value])

        peak_line = PeakLine(mz, intensity)
        return peak_line

    def serialize(self) -> str:
        line_elements = [None] * len(_PeakLineColumns)
        line_elements[_PeakLineColumns.mz.value] = f"{self.mz:.{PeakLine.MZ_PRECISION}f}"
        line_elements[_PeakLineColumns.intensity.value] = f"{self.mz:.{PeakLine.INTENSITY_PRECISION}f}"
        line_elements = [str(elem) for elem in line_elements]
        return ' '.join(line_elements) + '\n'


@dataclass
class HLine(Line):
    """
    Class for storing H line Information

    Example H Line:
        H   [info]
    """

    info: str

    __slots__ = 'info'

    @staticmethod
    def deserialize(line: str) -> 'HLine':
        line_elements = line.rstrip().split("\t")
        return HLine("\t".join(line_elements[1:]))

    def serialize(self) -> str:
        line_elements = ["H",
                         self.info
                         ]
        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'


class _ZLineColumns(Enum):
    letter = 0
    charge = 1
    mass = 2


@dataclass
class ZLine:
    """
    Class keeping track of ms2 Z lines

    Example Z_line:
        Z [low charge] [mass]
        Z	2	1887.9438
    """
    charge: int
    mass: float

    MASS_PRECISION: ClassVar[int] = 5

    __slots__ = 'charge', 'mass'

    @staticmethod
    def deserialize(line: str) -> 'ZLine':
        line_elements = line.rstrip().split("\t")

        if len(line_elements) != len(_ZLineColumns):
            raise ms2_exceptions.Ms2FileDeserializationZLineException(_line=line)

        charge = int(line_elements[_ZLineColumns.charge.value])
        mass = float(line_elements[_ZLineColumns.mass.value])

        return ZLine(charge, mass)

    def serialize(self) -> str:
        line_elements = [None]*len(_ZLineColumns)
        line_elements[_ZLineColumns.letter.value] = "Z"
        line_elements[_ZLineColumns.charge.value] = f"{self.charge}"
        line_elements[_ZLineColumns.mass.value] = f"{self.mass:.{ZLine.MASS_PRECISION}f}"
        line_elements = [str(elem) for elem in line_elements]
        return '\t'.join(line_elements) + '\n'


class _ILineColumns(Enum):
    letter = 0
    keyword = 1
    value = 2


@dataclass
class ILine(Line):
    """
    Class keeping track of ms2 I lines.

    Example I_line:
        I	Keyword	Value
        I	TIMSTOF_Parent_ID	8
        I	TIMSTOF_Precursor_ID	1
        I	RetTime	1.3691
    """
    keyword: str
    value: str

    # Keywords
    PARENT_ID_KEYWORD: ClassVar[str] = 'TIMSTOF_Parent_ID'
    PRECURSOR_ID_KEYWORD: ClassVar[str] = 'TIMSTOF_Precursor_ID'
    OOK0_KEYWORD: ClassVar[str] = 'OOK0'
    CCS_KEYWORD: ClassVar[str] = 'CCS'
    RETENTION_TIME_KEYWORD: ClassVar[str] = 'Retention_Time'
    COLLISION_ENERGY_KEYWORD: ClassVar[str] = 'Collision_Energy'
    ISOLATION_MZ_KEYWORD: ClassVar[str] = 'Isolation_Mz'
    ISOLATION_WIDTH_KEYWORD: ClassVar[str] = 'Isolation_Width'
    SCAN_NUMBER_BEGIN_KEYWORD: ClassVar[str] = 'Scan_Number_Begin'
    SCAN_NUMBER_END_KEYWORD: ClassVar[str] = 'Scan_Number_End'
    PRECURSOR_INTENSITY_KEYWORD: ClassVar[str] = 'Intensity'
    OOK0_SPECTRA_KEYWORD: ClassVar[str] = 'OOK0_Spectra'
    CCS_SPECTRA_KEYWORD: ClassVar[str] = 'CCS_Spectra'
    INTENSITY_SPECTRA_KEYWORD: ClassVar[str] = 'Intensity_Spectra'

    __slots__ = 'keyword', 'value'

    @staticmethod
    def deserialize(line: str) -> 'ILine':
        line_elements = line.rstrip().split("\t")

        if len(line_elements) != len(_ILineColumns):
            raise ms2_exceptions.Ms2FileDeserializationILineException(_line=line)

        keyword = line_elements[_ILineColumns.keyword.value]
        value = line_elements[_ILineColumns.value.value]

        return ILine(keyword, value)

    def serialize(self) -> str:

        line_elements = [None] * len(_ILineColumns)
        line_elements[_ILineColumns.letter.value] = "I"
        line_elements[_ILineColumns.keyword.value] = self.keyword
        line_elements[_ILineColumns.value.value] = self.value
        line_elements = [str(elem) for elem in line_elements]
        return '\t'.join(line_elements) + '\n'


class _SLineColumns(Enum):
    letter = 0
    low_scan = 1
    high_scan = 2
    mz = 3


@dataclass
class SLine(Line):
    """
    Class keeping track of ms2 S lines.

    Example S_line:
        S [low scan] [high scan] [m/z]
        S	000009	000009	944.4755
    """

    low_scan: int
    high_scan: int
    mz: float

    LOW_SCAN_LENGTH: ClassVar[int] = 6
    HIGH_SCAN_LENGTH: ClassVar[int] = 6
    MZ_PRECISION: ClassVar[int] = 5

    __slots__ = 'low_scan', 'high_scan', 'mz'

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
        line_elements[_SLineColumns.low_scan.value] = f"{self.low_scan:0{SLine.LOW_SCAN_LENGTH}d}"
        line_elements[_SLineColumns.high_scan.value] = f"{self.high_scan:0{SLine.HIGH_SCAN_LENGTH}d}"
        line_elements[_SLineColumns.mz.value] = f"{self.mz:.{SLine.MZ_PRECISION}f}"
        line_elements = [str(elem) for elem in line_elements]
        return '\t'.join(line_elements) + '\n'


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

    __slots__ = 's_line', 'i_lines', 'z_line', 'peak_lines'

    def get_mz_spectra(self):
        return [peak_line.mz for peak_line in self.peak_lines]

    def get_intensity_spectra(self):
        return [peak_line.intensity for peak_line in self.peak_lines]

    def get_i_line_dict(self):
        return {i_line.keyword: i_line.value for i_line in self.i_lines}

    def get_i_line_value(self, keyword) -> Union[str, None]:
        i_line_dict = self.get_i_line_dict()
        if keyword in i_line_dict:
            return i_line_dict[keyword]
        return None

    def get_retention_time(self, keyword=None) -> Union[float, None]:
        if keyword is None:
            keyword = ILine.RETENTION_TIME_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return float(val) if val else val

    def get_collision_energy(self, keyword=None) -> Union[float, None]:
        if keyword is None:
            keyword = ILine.COLLISION_ENERGY_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return float(val) if val else val

    def get_OOK0(self, keyword=None) -> Union[float, None]:
        if keyword is None:
            keyword = ILine.OOK0_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return float(val) if val else val

    def get_CCS(self, keyword=None) -> Union[float, None]:
        if keyword is None:
            keyword = ILine.CCS_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return float(val) if val else val

    def get_precursor_intensity(self, keyword=None) -> Union[float, None]:
        if keyword is None:
            keyword = ILine.PRECURSOR_INTENSITY_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return float(val) if val else val

    def get_OOK0_spectra(self, keyword=None) -> Union[List[float], None]:
        if keyword is None:
            keyword = ILine.OOK0_SPECTRA_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return [float(i) for i in ast.literal_eval(val)] if val else val

    def get_CCS_spectra(self, keyword=None) -> Union[List[float], None]:
        if keyword is None:
            keyword = ILine.CCS_SPECTRA_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return [float(i) for i in ast.literal_eval(val)] if val else val

    def get_intensity_spectra(self, keyword=None) -> Union[List[float], None]:
        if keyword is None:
            keyword = ILine.INTENSITY_SPECTRA_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return [float(i) for i in ast.literal_eval(val)] if val else val

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
        return HLine.deserialize(line)
    elif line[0] == 'S':
        return SLine.deserialize(line)
    elif line[0] == 'I':
        return ILine.deserialize(line)
    elif line[0] == 'Z':
        return ZLine.deserialize(line)
    elif line[0].isnumeric():
        return PeakLine.deserialize(line)
    else:
        raise ms2_exceptions.Ms2FileDeserializationUnsupportedLineException
