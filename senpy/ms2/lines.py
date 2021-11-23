from dataclasses import field, dataclass
from typing import List

import numpy as np

PeakLine = np.dtype(
    [
        ('mz', np.float32),
        ('intensity', np.float32)
    ]
)


@dataclass
class ZLine:
    """
    Class keeping track of ms2 Z lines.

    Example Z_line:
        Z [low charge] [mass]
        Z	2	1887.9438
    """
    charge: int
    mass: np.float32

    __slots__ = 'charge', 'mass'


@dataclass
class ILine:
    """
    Class keeping track of ms2 I lines.

    Example I_line:
        I	TIMSTOF_Parent_ID	8
        I	TIMSTOF_Precursor_ID	1
        I	RetTime	1.3691
    """
    keyword: str
    value: str

    __slots__ = 'keyword', 'value'


@dataclass
class SLine:
    """
    Class keeping track of ms2 S lines.

    Example S_line:
        S [low scan] [high scan] [m/z]
        #S	000009	000009	944.4755
    """

    low_scan: int
    high_scan: int
    mz: float

    i_lines: List[ILine] = field(default_factory=list)
    z_line: ZLine = None
    peak_lines: [] = field(default_factory=list)

    def convert_peak_list_to_arr(self):
        self.peak_lines = np.array(self.peak_lines, dtype=PeakLine)

    def get_mass_spectra(self) -> [np.float32]:
        mass_spectra = []
        for peak_line in self.peak_lines:
            mass_spectra.append(peak_line[0])
        return mass_spectra

    def get_intensity_spectra(self) -> [np.float32]:
        intensity_spectra = []
        for peak_line in self.peak_lines:
            intensity_spectra.append(peak_line[1])
        return intensity_spectra

    def get_i_line_dict(self) -> {str: str}:
        i_line_dict = {}
        for i_line in self.i_lines:
            i_line_dict[i_line.keyword] = i_line.value
        return i_line_dict

    def get_retention_time(self):
        tmp_dict = self.get_i_line_dict()
        if 'RetTime' in tmp_dict:
            return float(tmp_dict['RetTime'])
        else:
            return None

    def get_ccs(self):
        tmp_dict = self.get_i_line_dict()
        if 'ccs' in tmp_dict:
            return float(tmp_dict['ccs'])
        else:
            return None

    def get_ook0(self):
        tmp_dict = self.get_i_line_dict()
        if 'ook0' in tmp_dict:
            return float(tmp_dict['ook0'])
        else:
            return None
