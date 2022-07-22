from dataclasses import dataclass
from typing import List, Dict, Any

import h5py
import numpy as np


@dataclass
class Ms1Spectra:
    scan_id: np.int32
    rt: np.float64
    mz_spectra: np.ndarray
    int_spectra: np.ndarray


def read_file(hdf5_file) -> List[Ms1Spectra]:
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