from dataclasses import dataclass
from typing import Any, Dict, List

import h5py
import numpy as np

from ..constants import PROTON_MASS
from ..ms2.lines import Ms2Spectra, ILine

key_to_value_map = {
    ILine.PARENT_ID_KEYWORD: 0,
    ILine.PRECURSOR_ID_KEYWORD: 1,
    ILine.OOK0_KEYWORD: 2,
    ILine.CCS_KEYWORD: 3,
    ILine.RETENTION_TIME_KEYWORD: 4,
    ILine.COLLISION_ENERGY_KEYWORD: 5,
    ILine.ISOLATION_MZ_KEYWORD: 6,
    ILine.ISOLATION_WIDTH_KEYWORD: 7,
    ILine.SCAN_NUMBER_BEGIN_KEYWORD: 8,
    ILine.SCAN_NUMBER_END_KEYWORD: 9,
    ILine.PRECURSOR_INTENSITY_KEYWORD: 10,
    ILine.OOK0_SPECTRA_KEYWORD: 11,
    ILine.CCS_SPECTRA_KEYWORD: 12,
    ILine.INTENSITY_SPECTRA_KEYWORD: 13,
    ILine.MZ_SPECTRA_KEYWORD: 14
}


def get_key_for_keyword(keyword):
    return np.int8(key_to_value_map[keyword])


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
        return (self.mz * self.charge) - (self.charge - 1) * PROTON_MASS

    @property
    def parent_id(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.PARENT_ID_KEYWORD))

    @parent_id.setter
    def parent_id(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.PARENT_ID_KEYWORD)] = val

    @property
    def precursor_id(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.PRECURSOR_ID_KEYWORD))

    @precursor_id.setter
    def precursor_id(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.PRECURSOR_ID_KEYWORD)] = val

    @property
    def retention_time(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.RETENTION_TIME_KEYWORD))

    @retention_time.setter
    def retention_time(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.RETENTION_TIME_KEYWORD)] = val

    @property
    def collision_energy(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.COLLISION_ENERGY_KEYWORD))

    @collision_energy.setter
    def collision_energy(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.COLLISION_ENERGY_KEYWORD)] = val

    @property
    def ook0(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.OOK0_KEYWORD))

    @ook0.setter
    def ook0(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.OOK0_KEYWORD)] = val

    @property
    def ccs(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.CCS_KEYWORD))

    @ccs.setter
    def ccs(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.CCS_KEYWORD)] = val

    @property
    def precursor_intensity(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.PRECURSOR_INTENSITY_KEYWORD))

    @precursor_intensity.setter
    def precursor_intensity(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.PRECURSOR_INTENSITY_KEYWORD)] = val

    @property
    def ook0_spectra(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.OOK0_SPECTRA_KEYWORD))

    @ook0_spectra.setter
    def ook0_spectra(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.OOK0_SPECTRA_KEYWORD)] = val

    @property
    def ccs_spectra(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.CCS_SPECTRA_KEYWORD))

    @ccs_spectra.setter
    def ccs_spectra(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.CCS_SPECTRA_KEYWORD)] = val

    @property
    def mobility_intensity_spectra(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.INTENSITY_SPECTRA_KEYWORD))

    @mobility_intensity_spectra.setter
    def mobility_intensity_spectra(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.INTENSITY_SPECTRA_KEYWORD)] = val

    @property
    def mobility_mz_spectra(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.MZ_SPECTRA_KEYWORD))

    @mobility_mz_spectra.setter
    def mobility_mz_spectra(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.MZ_SPECTRA_KEYWORD)] = val

    @property
    def isolation_mz(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.ISOLATION_MZ_KEYWORD))

    @isolation_mz.setter
    def isolation_mz(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.ISOLATION_MZ_KEYWORD)] = val

    @property
    def isolation_width(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.ISOLATION_WIDTH_KEYWORD))

    @isolation_width.setter
    def isolation_width(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.ISOLATION_WIDTH_KEYWORD)] = val

    @property
    def scan_num_begin(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.SCAN_NUMBER_BEGIN_KEYWORD))

    @scan_num_begin.setter
    def scan_num_begin(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.SCAN_NUMBER_BEGIN_KEYWORD)] = val

    @property
    def scan_num_end(self):
        return self.i_line_dict.get(get_key_for_keyword(ILine.SCAN_NUMBER_END_KEYWORD))

    @scan_num_end.setter
    def scan_num_end(self, val):
        self.i_line_dict[get_key_for_keyword(ILine.SCAN_NUMBER_END_KEYWORD)] = val


def convert_precursor_to_i_line_dict(precursor):
    return {
        key_to_value_map[ILine.PARENT_ID_KEYWORD]: precursor['prec_parent_id'][0],
        key_to_value_map[ILine.PRECURSOR_ID_KEYWORD]: precursor['prec_id'][0],
        key_to_value_map[ILine.OOK0_KEYWORD]: precursor['ook0'][0],
        key_to_value_map[ILine.CCS_KEYWORD]: precursor['ccs'][0],
        key_to_value_map[ILine.RETENTION_TIME_KEYWORD]: precursor['rt'][0],
        key_to_value_map[ILine.COLLISION_ENERGY_KEYWORD]: precursor['ce'][0],
        key_to_value_map[ILine.ISOLATION_MZ_KEYWORD]: precursor['iso_mz'][0],
        key_to_value_map[ILine.ISOLATION_WIDTH_KEYWORD]: precursor['iso_width'][0],
        key_to_value_map[ILine.SCAN_NUMBER_BEGIN_KEYWORD]: precursor['scan_num_begin'][0],
        key_to_value_map[ILine.SCAN_NUMBER_END_KEYWORD]: precursor['scan_num_end'][0],
        key_to_value_map[ILine.PRECURSOR_INTENSITY_KEYWORD]: precursor['intensity'][0]
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
