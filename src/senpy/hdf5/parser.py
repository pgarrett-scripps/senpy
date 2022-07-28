import ast
from dataclasses import dataclass
from typing import Any, Dict, List

import h5py
import numpy as np

from ..constants import PROTON_MASS
from ..ms2.lines import Ms2Spectra, ILine


@dataclass
class Ms2Spectra:
    scan_id: np.int32
    mz: np.float64
    charge: np.int8
    i_line_dict: Dict[int, Any]
    mz_spectra: np.ndarray
    int_spectra: np.ndarray

    @property
    def mass(self):
        return float((self.mz * self.charge) - (self.charge - 1) * PROTON_MASS)

    @property
    def parent_id(self) -> int:
        return int(self.i_line_dict.get(ILine.PARENT_ID_KEYWORD))

    @parent_id.setter
    def parent_id(self, val: int):
        self.i_line_dict[ILine.PARENT_ID_KEYWORD] = val

    @property
    def precursor_id(self) -> int:
        return int(self.i_line_dict.get(ILine.PRECURSOR_ID_KEYWORD))

    @precursor_id.setter
    def precursor_id(self, val: int):
        self.i_line_dict[ILine.PRECURSOR_ID_KEYWORD] = val

    @property
    def retention_time(self) -> float:
        return float(self.i_line_dict.get(ILine.RETENTION_TIME_KEYWORD))

    @retention_time.setter
    def retention_time(self, val: float):
        self.i_line_dict[ILine.RETENTION_TIME_KEYWORD] = val

    @property
    def collision_energy(self) -> float:
        return float(self.i_line_dict.get(ILine.COLLISION_ENERGY_KEYWORD))

    @collision_energy.setter
    def collision_energy(self, val: float):
        self.i_line_dict[ILine.COLLISION_ENERGY_KEYWORD] = val

    @property
    def ook0(self) -> float:
        return float(self.i_line_dict.get(ILine.OOK0_KEYWORD))

    @ook0.setter
    def ook0(self, val: float):
        self.i_line_dict[ILine.OOK0_KEYWORD] = val

    @property
    def ccs(self) -> float:
        return float(self.i_line_dict.get(ILine.CCS_KEYWORD))

    @ccs.setter
    def ccs(self, val: float):
        self.i_line_dict[ILine.CCS_KEYWORD] = val

    @property
    def precursor_intensity(self) -> float:
        return float(self.i_line_dict.get(ILine.PRECURSOR_INTENSITY_KEYWORD))

    @precursor_intensity.setter
    def precursor_intensity(self, val: float):
        self.i_line_dict[ILine.PRECURSOR_INTENSITY_KEYWORD] = val


    @property
    def ook0_spectra(self) -> List[float]:
        return [float(i) for i in ast.literal_eval(self.i_line_dict.get(ILine.OOK0_SPECTRA_KEYWORD))]

    @ook0_spectra.setter
    def ook0_spectra(self, val: List[float]):
        self.i_line_dict[ILine.OOK0_SPECTRA_KEYWORD] = val

    @property
    def ccs_spectra(self) -> List[float]:
        return [float(i) for i in ast.literal_eval(self.i_line_dict.get(ILine.CCS_SPECTRA_KEYWORD))]

    @ccs_spectra.setter
    def ccs_spectra(self, val: List[float]):
        self.i_line_dict[ILine.CCS_SPECTRA_KEYWORD] = val

    @property
    def mobility_intensity_spectra(self) -> List[float]:
        return [float(i) for i in ast.literal_eval(self.i_line_dict.get(ILine.INTENSITY_SPECTRA_KEYWORD))]

    @mobility_intensity_spectra.setter
    def mobility_intensity_spectra(self, val: List[float]):
        self.i_line_dict[ILine.INTENSITY_SPECTRA_KEYWORD] = val

    @property
    def mobility_mz_spectra(self) -> List[float]:
        return [float(i) for i in ast.literal_eval(self.i_line_dict.get(ILine.MZ_SPECTRA_KEYWORD))]

    @mobility_mz_spectra.setter
    def mobility_mz_spectra(self, val: List[float]):
        self.i_line_dict[ILine.MZ_SPECTRA_KEYWORD] = val

    @property
    def isolation_mz(self) -> float:
        return float(self.i_line_dict.get(ILine.ISOLATION_MZ_KEYWORD))

    @isolation_mz.setter
    def isolation_mz(self, val: float):
        self.i_line_dict[ILine.ISOLATION_MZ_KEYWORD] = val

    @property
    def isolation_width(self) -> float:
        return float(self.i_line_dict.get(ILine.ISOLATION_WIDTH_KEYWORD))

    @isolation_width.setter
    def isolation_width(self, val: float):
        self.i_line_dict[ILine.ISOLATION_WIDTH_KEYWORD] = val

    @property
    def scan_num_begin(self) -> float:
        return float(self.i_line_dict.get(ILine.SCAN_NUMBER_BEGIN_KEYWORD))

    @scan_num_begin.setter
    def scan_num_begin(self, val: float):
        self.i_line_dict[ILine.SCAN_NUMBER_BEGIN_KEYWORD] = val

    @property
    def scan_num_end(self) -> float:
        return float(self.i_line_dict.get(ILine.SCAN_NUMBER_END_KEYWORD))

    @scan_num_end.setter
    def scan_num_end(self, val: float):
        self.i_line_dict[ILine.SCAN_NUMBER_END_KEYWORD] = val

    @staticmethod
    def setup_from_ms2_lines(lines):
        i_lines = {}
        mz_spectra, int_spectra = [], []
        low_scan, high_scan, mz, charge, mass = None, None, None, None, None
        for line in lines:
            if line[0] == 'S':
                letter, low_scan, high_scan, mz = line.rstrip().split("\t")
                low_scan = int(low_scan)
                high_scan = int(high_scan)
                mz = float(mz)
            elif line[0] == 'Z':
                letter, charge, mass = line.rstrip().split("\t")
                charge = int(charge)
                mass = float(mass)
            elif line[0] == 'I':
                letter, key, val = line.rstrip().split("\t")
                i_lines[key] = val
            else:
                mz, i, = map(float, line.rstrip().split(" "))
                mz_spectra.append(mz)
                int_spectra.append(i)

        return Ms2Spectra(scan_id=low_scan, mz=mz,
                          charge=charge, i_line_dict=i_lines,
                          mz_spectra=np.array(mz_spectra, dtype=np.float64),
                          int_spectra=np.array(int_spectra, dtype=np.float32))


def convert_precursor_to_i_line_dict(precursor):
    return {
        ILine.PARENT_ID_KEYWORD: precursor['prec_parent_id'][0],
        ILine.PRECURSOR_ID_KEYWORD: precursor['prec_id'][0],
        ILine.OOK0_KEYWORD: precursor['ook0'][0],
        ILine.CCS_KEYWORD: precursor['ccs'][0],
        ILine.RETENTION_TIME_KEYWORD: precursor['rt'][0],
        ILine.COLLISION_ENERGY_KEYWORD: precursor['ce'][0],
        ILine.ISOLATION_MZ_KEYWORD: precursor['iso_mz'][0],
        ILine.ISOLATION_WIDTH_KEYWORD: precursor['iso_width'][0],
        ILine.SCAN_NUMBER_BEGIN_KEYWORD: precursor['scan_num_begin'][0],
        ILine.SCAN_NUMBER_END_KEYWORD: precursor['scan_num_end'][0],
        ILine.PRECURSOR_INTENSITY_KEYWORD: precursor['intensity'][0]
    }


def read_file(hdf5_file) -> List[Ms2Spectra]:
    ms2_spectras = []
    with h5py.File(hdf5_file, 'r') as f:
        spectras = f['spectra']
        precursors = f['precursor']
        offset = 0
        for precursor in precursors:
            n_peaks = precursor['n_peaks'][0]
            precursor_spectra = spectras[offset:offset + n_peaks]
            i_line_dict = convert_precursor_to_i_line_dict(precursor)
            ms2_spectra = Ms2Spectra(scan_id=precursor['scan_id'][0],
                                     mz=precursor['mz'][0],
                                     charge=precursor['charge'][0],
                                     i_line_dict=i_line_dict,
                                     mz_spectra=precursor_spectra['mz_array'],
                                     int_spectra=precursor_spectra['intensity_array']
                                     )
            ms2_spectras.append(ms2_spectra)

            offset += n_peaks
    return ms2_spectras


if __name__ == '__main__':
    spectra = read_file(r"C:\data\test.d\test.hdf5")

