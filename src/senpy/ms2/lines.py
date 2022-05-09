import ast
from dataclasses import dataclass
from typing import List, Dict, Union, ClassVar
import numpy as np

from . import exceptions as ms2_exceptions
from .columns import PeakLineColumns, ZLineColumns, ILineColumns, SLineColumns
from ..util import Line, HLine


@dataclass
class PeakLine(Line):
    """
    Class for serializing/deserializing PeakLines

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
        if len(line_elements) != len(PeakLineColumns):
            raise ms2_exceptions.Ms2FileDeserializationPeakLineException(_line=line)

        mz = PeakLine._deserialize_mz(line_elements[PeakLineColumns.mz.value])
        intensity = PeakLine._deserialize_intensity(line_elements[PeakLineColumns.intensity.value])

        peak_line = PeakLine(mz, intensity)
        return peak_line

    @staticmethod
    def _deserialize_mz(val: str) -> np.float32:
        return np.float32(val)

    @staticmethod
    def _deserialize_intensity(val: str) -> np.float32:
        return np.float32(val)

    def serialize(self) -> str:
        line_elements = [""] * len(PeakLineColumns)
        line_elements[PeakLineColumns.mz.value] = self._serialize_mz()
        line_elements[PeakLineColumns.intensity.value] = self._serialize_intensity()
        return ' '.join(line_elements) + '\n'

    def _serialize_mz(self):
        return f"{self.mz:.{PeakLine.MZ_PRECISION}f}"

    def _serialize_intensity(self):
        return f"{self.intensity:.{PeakLine.INTENSITY_PRECISION}f}"


@dataclass
class ZLine:
    """
    Class keeping track of ms2 Z lines

    Example Z_line:
        Z [low charge] [mass]
        Z	2	1887.9438
    """
    LETTER = "Z"

    charge: int
    mass: float

    MASS_PRECISION: ClassVar[int] = 5

    __slots__ = 'charge', 'mass'

    @staticmethod
    def deserialize(line: str) -> 'ZLine':
        line_elements = line.rstrip().split("\t")

        if len(line_elements) != len(ZLineColumns):
            raise ms2_exceptions.Ms2FileDeserializationZLineException(_line=line)

        charge = ZLine._deserialize_charge(line_elements[ZLineColumns.charge.value])
        mass = ZLine._deserialize_mass(line_elements[ZLineColumns.mass.value])

        return ZLine(charge, mass)

    @staticmethod
    def _deserialize_charge(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_mass(val: str) -> float:
        return float(val)

    def serialize(self) -> str:
        line_elements = [""]*len(ZLineColumns)
        line_elements[ZLineColumns.letter.value] = ZLine.LETTER
        line_elements[ZLineColumns.charge.value] = self._serialize_charge()
        line_elements[ZLineColumns.mass.value] = self._serialize_mass()
        return '\t'.join(line_elements) + '\n'

    def _serialize_charge(self) -> str:
        return f"{self.charge}"

    def _serialize_mass(self) -> str:
        return f"{self.mass:.{ZLine.MASS_PRECISION}f}"


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

    LETTER = "I"

    keyword: str
    val: str

    # Keywords
    PARENT_ID_KEYWORD: ClassVar[str] = 'TIMSTOF_Parent_ID'
    PRECURSOR_ID_KEYWORD: ClassVar[str] = 'TIMSTOF_Precursor_ID'
    OOK0_KEYWORD: ClassVar[str] = 'Ion Mobility'
    CCS_KEYWORD: ClassVar[str] = 'CCS'
    RETENTION_TIME_KEYWORD: ClassVar[str] = 'RetTime'
    COLLISION_ENERGY_KEYWORD: ClassVar[str] = 'Collision_Energy'
    ISOLATION_MZ_KEYWORD: ClassVar[str] = 'Isolation_Mz'
    ISOLATION_WIDTH_KEYWORD: ClassVar[str] = 'Isolation_Width'
    SCAN_NUMBER_BEGIN_KEYWORD: ClassVar[str] = 'Scan_Number_Begin'
    SCAN_NUMBER_END_KEYWORD: ClassVar[str] = 'Scan_Number_End'
    PRECURSOR_INTENSITY_KEYWORD: ClassVar[str] = 'Intensity'
    OOK0_SPECTRA_KEYWORD: ClassVar[str] = 'OOK0_Spectra'
    CCS_SPECTRA_KEYWORD: ClassVar[str] = 'CCS_Spectra'
    INTENSITY_SPECTRA_KEYWORD: ClassVar[str] = 'Intensity_Spectra'
    MZ_SPECTRA_KEYWORD: ClassVar[str] = 'MZ_Spectra'

    __slots__ = 'keyword', 'value'

    @staticmethod
    def deserialize(line: str) -> 'ILine':
        line_elements = line.rstrip().split("\t")

        if len(line_elements) != len(ILineColumns):
            raise ms2_exceptions.Ms2FileDeserializationILineException(_line=line)

        keyword = ILine._deserialize_keyword(line_elements[ILineColumns.keyword.value])
        val = ILine._deserialize_val(line_elements[ILineColumns.val.value])

        return ILine(keyword, val)

    @staticmethod
    def _deserialize_keyword(val: str) -> str:
        return val

    @staticmethod
    def _deserialize_val(val: str) -> str:
        return val

    def serialize(self) -> str:

        line_elements = [""] * len(ILineColumns)
        line_elements[ILineColumns.letter.value] = ILine.LETTER
        line_elements[ILineColumns.keyword.value] = self._serialize_keyword()
        line_elements[ILineColumns.val.value] = self._serialize_val()
        return '\t'.join(line_elements) + '\n'

    def _serialize_keyword(self) -> str:
        return self.keyword

    def _serialize_val(self) -> str:
        return self.val


@dataclass
class SLine(Line):
    """
    Class keeping track of ms2 S lines.

    Example S_line:
        S [low scan] [high scan] [m/z]
        S	000009	000009	944.4755
    """

    LETTER = "S"

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

        if len(line_elements) != len(SLineColumns):
            raise ms2_exceptions.Ms2FileDeserializationSLineException(_line=line)

        low_scan = SLine._deserialize_low_scan(line_elements[SLineColumns.low_scan.value])
        high_scan = SLine._deserialize_high_scan(line_elements[SLineColumns.high_scan.value])
        mz = SLine._deserialize_mz(line_elements[SLineColumns.mz.value])

        return SLine(low_scan, high_scan, mz)

    @staticmethod
    def _deserialize_low_scan(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_high_scan(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_mz(val: str) -> float:
        return float(val)

    def serialize(self):
        line_elements = [""] * len(SLineColumns)
        line_elements[SLineColumns.letter.value] = SLine.LETTER
        line_elements[SLineColumns.low_scan.value] = self._serialize_low_scan()
        line_elements[SLineColumns.high_scan.value] = self._serialize_high_scan()
        line_elements[SLineColumns.mz.value] = self._serialize_mz()
        return '\t'.join(line_elements) + '\n'

    def _serialize_low_scan(self):
        return f"{self.low_scan:0{SLine.LOW_SCAN_LENGTH}d}"

    def _serialize_high_scan(self):
        return f"{self.high_scan:0{SLine.HIGH_SCAN_LENGTH}d}"

    def _serialize_mz(self):
        return f"{self.mz:.{SLine.MZ_PRECISION}f}"


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

    __slots__ = 's_line', 'i_lines', 'z_line', 'peak_lines'

    def get_mz_spectra(self):
        return [peak_line.mz for peak_line in self.peak_lines]

    def get_intensity_spectra(self):
        return [peak_line.intensity for peak_line in self.peak_lines]

    def get_i_line_dict(self):
        if self.i_line_dict:
            return self.i_line_dict
        return {i_line.keyword: i_line.value for i_line in self.i_lines}

    def get_i_line_value(self, keyword) -> Union[str, None]:
        i_line_dict = self.get_i_line_dict()
        if keyword in i_line_dict:
            return i_line_dict[keyword]
        return None

    def get_parent_id(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ILine.PARENT_ID_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

    def get_precursor_id(self, keyword=None) -> Union[str, None]:
        if keyword is None:
            keyword = ILine.PRECURSOR_ID_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return val

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

    def get_ook0(self, keyword=None) -> Union[float, None]:
        if keyword is None:
            keyword = ILine.OOK0_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return float(val) if val else val

    def get_ccs(self, keyword=None) -> Union[float, None]:
        if keyword is None:
            keyword = ILine.CCS_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return float(val) if val else val

    def get_precursor_intensity(self, keyword=None) -> Union[float, None]:
        if keyword is None:
            keyword = ILine.PRECURSOR_INTENSITY_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return float(val) if val else val

    def get_ook0_spectra(self, keyword=None) -> Union[List[float], None]:
        if keyword is None:
            keyword = ILine.OOK0_SPECTRA_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return [float(i) for i in ast.literal_eval(val)] if val else val

    def get_ccs_spectra(self, keyword=None) -> Union[List[float], None]:
        if keyword is None:
            keyword = ILine.CCS_SPECTRA_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return [float(i) for i in ast.literal_eval(val)] if val else val

    def get_mobility_intensity_spectra(self, keyword=None) -> Union[List[float], None]:
        if keyword is None:
            keyword = ILine.INTENSITY_SPECTRA_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return [float(i) for i in ast.literal_eval(val)] if val else val

    def get_mobility_mz_spectra(self, keyword=None) -> Union[List[float], None]:
        if keyword is None:
            keyword = ILine.MZ_SPECTRA_KEYWORD

        val = self.get_i_line_value(keyword)  # none/str
        return [float(i) for i in ast.literal_eval(val)] if val else val

    def serialize(self) -> str:
        lines = [self.s_line] + self.i_lines + [self.z_line] + self.peak_lines
        return ''.join([line.serialize() for line in lines])

    @staticmethod
    def create(low_scan: int, high_scan: int, mz: float, charge: int, mass: float, mz_spectra: np.ndarray,
               intensity_spectra: np.ndarray, info_dict: Dict[str, str]) -> 'Ms2Spectra':
        s_line = SLine(low_scan=low_scan, high_scan=high_scan, mz=mz)
        i_lines = [ILine(keyword=key, val=val) for key, val in info_dict.items()]
        z_line = ZLine(charge=charge, mass=mass)
        peak_lines = [PeakLine(mz=mz, intensity=intensity) for mz, intensity in zip(mz_spectra, intensity_spectra)]
        precursor_spectra = Ms2Spectra(s_line=s_line, i_lines=i_lines, z_line=z_line, peak_lines=peak_lines)
        return precursor_spectra


def parse_ms2_line(line: str) -> Union[HLine, SLine, ILine, ZLine, PeakLine]:
    """
    Returns the appropriate Ms2 Line object or throws error
    """
    if line[0] == HLine.LETTER:
        return HLine.deserialize(line)
    elif line[0] == SLine.LETTER:
        return SLine.deserialize(line)
    elif line[0] == ILine.LETTER:
        return ILine.deserialize(line)
    elif line[0] == ZLine.LETTER:
        return ZLine.deserialize(line)
    elif line[0].isnumeric():
        return PeakLine.deserialize(line)
    else:
        raise ms2_exceptions.Ms2FileDeserializationUnsupportedLineException
