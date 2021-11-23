from dataclasses import dataclass
from typing import List


@dataclass
class FeatureLine:
    """
    Class keeping track of ms2 Z lines.

    Example Z_line:
        massCalib	rtApex	intensityApex	charge	nIsotopes	nScans	sulfur	cos_corr_1	cos_corr_2	diff_for_output	corr_fill_zero	intensity_1	scan_id_1	mz_std_1	intensity_2	scan_id_2	mz_std_2	mz	rtStart	rtEnd	id	ion_mobility	FAIMS	targeted_mode
    """
    neutral_mass: float
    rt_apex: float
    intensity_apex: float
    charge: int
    num_isotopes: int
    num_scans: int
    sulfur: int
    cos_corr_1: float
    cos_corr_2: float
    diff_for_output: float
    corr_fill_zero: float
    intensity_1: List[float]
    scan_id_1: List[int]
    mz_std_1: float
    intensity_2: List[float]
    scan_id_2: List[int]
    mz_std_2: float
    mz: float
    rt_start: float
    rt_end: float
    id: int
    ion_mobility: float
    faims: int
    targeted_mode: List[float]