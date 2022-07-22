import time
from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np
import numpy.typing as npt
import ast

MS2_FILE = r"C:\Users\Ty\jupyter\search\ecoli.ms2"

def return_lines(file):
    lines = []
    with open(file) as f:
        for line in f:
            lines.append(line)

    return lines


def filter_ms2_lines(lines):
    start = False
    spectra_lines = []
    for line in lines:
        if line[0] == "S":
            if start == True:
                yield spectra_lines
                spectra_lines = []
            else:
                start = True
        if start == True:
            spectra_lines.append(line)
    return spectra_lines


key_to_value_map = {
    'TIMSTOF_Parent_ID': 0,
    'TIMSTOF_Precursor_ID': 1,
    'Ion Mobility': 2,
    'CCS': 3,
    'RetTime': 4,
    'Collision_Energy': 5,
    'Isolation_Mz': 6,
    'Isolation_Width': 7,
    'Scan_Number_Begin': 8,
    'Scan_Number_End': 9,
    'Intensity': 10,
    'OOK0_Spectra': 11,
    'CCS_Spectra': 12,
    'Intensity_Spectra': 13,
    'MZ_Spectra': 14
}

key_to_type_map = {
    'TIMSTOF_Parent_ID': lambda x: int(x),
    'TIMSTOF_Precursor_ID': lambda x: int(x),
    'Ion Mobility': lambda x: np.float32(x),
    'CCS': lambda x: np.float32(x),
    'RetTime': lambda x: np.float32(x),
    'Collision_Energy': lambda x: np.float32(x),
    'Isolation_Mz': lambda x: np.float64(x),
    'Isolation_Width': lambda x: np.float32(x),
    'Scan_Number_Begin': lambda x: np.float32(x),
    'Scan_Number_End': lambda x: np.float32(x),
    'Intensity': lambda x: np.float64(x),
    'OOK0_Spectra': lambda x: ast.literal_eval(x),
    'CCS_Spectra': lambda x: ast.literal_eval(x),
    'Intensity_Spectra': lambda x: ast.literal_eval(x),
    'MZ_Spectra': lambda x: ast.literal_eval(x)
}


@dataclass
class Ms2SpectraFast:
    s_line: str
    z_line: str
    i_lines: List[str]
    peak_lines: List[str]

    @staticmethod
    def setup(lines):
        s_line, z_line, i_lines, peak_lines = None, None, [], []
        for line in lines:
            if line[0] == 'S':
                s_line = line
            elif line[0] == 'Z':
                z_line = line
            elif line[0] == 'I':
                i_lines.append(line)
            elif line[0].isnumeric():
                peak_lines.append(line)
        return Ms2SpectraFast(s_line, z_line, i_lines, peak_lines)


@dataclass
class Ms2Spectra:
    low_scan: int
    high_scan: int
    mz: np.float64
    charge: np.int8
    mass: np.float64
    i_lines: Dict[int, Any]
    mz_spectra: Any
    int_spectra: Any

    __slots__ = ["low_scan", "high_scan", 'mz', 'charge', 'mass', 'i_lines', 'mz_spectra', 'int_spectra']

    @staticmethod
    def setup(lines):
        i_lines = {}
        mz_spectra, int_spectra = [], []
        low_scan, high_scan, mz, charge, mass = None, None, None, None, None
        for line in lines:
            if line[0] == 'S':
                letter, low_scan, high_scan, mz = line.rstrip().split("\t")
                low_scan = int(low_scan)
                high_scan = int(high_scan)
                mz = np.float64(mz)
            elif line[0] == 'Z':
                letter, charge, mass = line.rstrip().split("\t")
                charge = np.int8(charge)
                mass = np.float64(mass)
            elif line[0] == 'I':
                letter, key, val = line.rstrip().split("\t")
                i_lines[key_to_value_map[key]] = key_to_type_map[key](val)
            elif line[0].isnumeric():
                m, i = line.rstrip().split(" ")
                mz_spectra.append(np.float64(m))
                int_spectra.append(np.float32(i))

        return Ms2Spectra(low_scan=low_scan, high_scan=high_scan, mz=mz,
                          charge=charge, mass=mass, i_lines=i_lines,
                          mz_spectra=np.array(mz_spectra, dtype=np.float64),
                          int_spectra=np.array(int_spectra, dtype=np.float32))


def convert_lines_to_ms2_spectra(spectra_lines):
    from senpy.ms2.lines import SLine, HLine, ZLine, PeakLine, ILine, Ms2Spectra, parse_ms2_line
    s_line, z_line, i_lines, peak_lines = None, None, [], []

    for line in spectra_lines:
        ms2_line = parse_ms2_line(line)
        if isinstance(ms2_line, SLine):
            s_line = ms2_line
        elif isinstance(ms2_line, ILine):
            i_lines.append(ms2_line)
        elif isinstance(ms2_line, ZLine):
            z_line = ms2_line
        elif isinstance(ms2_line, PeakLine):
            peak_lines.append(ms2_line)
        else:
            raise Exception

    return Ms2Spectra(s_line=s_line,
                      z_line=z_line,
                      i_lines=i_lines,
                      peak_lines=peak_lines
                      )


def convert_lines_to_ms2_spectra3(spectra_lines):
    from dataclasses import dataclass
    from typing import List, Dict, Any

    @dataclass
    class Ms2SpectraFast:
        s_line: str
        z_line: str
        i_lines: List[str]
        peak_lines: List[str]

        @staticmethod
        def setup(lines):
            s_line, z_line, i_lines, peak_lines = None, None, [], []
            for line in lines:
                if line[0] == 'S':
                    s_line = line
                elif line[0] == 'Z':
                    z_line = line
                elif line[0] == 'I':
                    i_lines.append(line)
                elif line[0].isnumeric():
                    peak_lines.append(line)
            return Ms2SpectraFast(s_line, z_line, i_lines, peak_lines)

    return Ms2SpectraFast.setup(spectra_lines)


def convert_lines_to_ms2_spectra2(spectra_lines):
    from dataclasses import dataclass, field
    from enum import Enum, auto
    from typing import List, Dict, Any
    import numpy as np
    import numpy.typing as npt
    import ast

    key_to_value_map = {
        'TIMSTOF_Parent_ID': 0,
        'TIMSTOF_Precursor_ID': 1,
        'Ion Mobility': 2,
        'CCS': 3,
        'RetTime': 4,
        'Collision_Energy': 5,
        'Isolation_Mz': 6,
        'Isolation_Width': 7,
        'Scan_Number_Begin': 8,
        'Scan_Number_End': 9,
        'Intensity': 10,
        'OOK0_Spectra': 11,
        'CCS_Spectra': 12,
        'Intensity_Spectra': 13,
        'MZ_Spectra': 14
    }

    key_to_type_map = {
        'TIMSTOF_Parent_ID': lambda x: int(x),
        'TIMSTOF_Precursor_ID': lambda x: int(x),
        'Ion Mobility': lambda x: np.float32(x),
        'CCS': lambda x: np.float32(x),
        'RetTime': lambda x: np.float32(x),
        'Collision_Energy': lambda x: np.float32(x),
        'Isolation_Mz': lambda x: np.float64(x),
        'Isolation_Width': lambda x: np.float32(x),
        'Scan_Number_Begin': lambda x: np.float32(x),
        'Scan_Number_End': lambda x: np.float32(x),
        'Intensity': lambda x: np.float64(x),
        'OOK0_Spectra': lambda x: ast.literal_eval(x),
        'CCS_Spectra': lambda x: ast.literal_eval(x),
        'Intensity_Spectra': lambda x: ast.literal_eval(x),
        'MZ_Spectra': lambda x: ast.literal_eval(x)
    }

    @dataclass
    class Ms2Spectra:
        low_scan: int
        high_scan: int
        mz: np.float64
        charge: np.int8
        mass: np.float64
        i_lines: Dict[int, Any]
        mz_spectra: Any
        int_spectra: Any

        __slots__ = ["low_scan", "high_scan", 'mz', 'charge', 'mass', 'i_lines', 'mz_spectra', 'int_spectra']

        @staticmethod
        def setup(lines):
            i_lines = {}
            mz_spectra, int_spectra = [], []
            low_scan, high_scan, mz, charge, mass = None, None, None, None, None
            for line in lines:
                if line[0] == 'S':
                    letter, low_scan, high_scan, mz = line.rstrip().split("\t")
                    low_scan = int(low_scan)
                    high_scan = int(high_scan)
                    mz = np.float64(mz)
                elif line[0] == 'Z':
                    letter, charge, mass = line.rstrip().split("\t")
                    charge = np.int8(charge)
                    mass = np.float64(mass)
                elif line[0] == 'I':
                    letter, key, val = line.rstrip().split("\t")
                    i_lines[key_to_value_map[key]] = key_to_type_map[key](val)
                elif line[0].isnumeric():
                    m, i = line.rstrip().split(" ")
                    mz_spectra.append(np.float64(m))
                    int_spectra.append(np.float32(i))

            return Ms2Spectra(low_scan=low_scan, high_scan=high_scan, mz=mz,
                              charge=charge, mass=mass, i_lines=i_lines,
                              mz_spectra=np.array(mz_spectra, dtype=np.float64),
                              int_spectra=np.array(int_spectra, dtype=np.float32))

    return Ms2Spectra.setup(spectra_lines)

def multi_process_spectra(n, lines_lines):
    from multiprocess import Pool
    with Pool(processes=n) as pool:
        res = pool.map(convert_lines_to_ms2_spectra2, lines_lines)
    return res


if __name__ == '__main__':
    lines = return_lines(MS2_FILE)
    lines_lines = list(filter_ms2_lines(lines))
    print(len(lines_lines))

    start_time = time.time()
    res = multi_process_spectra(8, lines_lines)
    print((time.time() - start_time)/60)

    start_time = time.time()
    res = multi_process_spectra(1, lines_lines)
    print((time.time() - start_time)/60)
