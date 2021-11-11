from dataclasses import dataclass, field
from typing import List

import numpy as np

from senpy.abstract_class import Line

@dataclass
class MobilogramItem:
    ook0: np.float32
    ccs: np.float32
    intensity: np.float32

@dataclass
class OutLine(Line):
    """
    DataClass for holding information in out file

    Example out line:
        Scan_Number	seq	charge	mass	mz	xcorr	RetTime	1/k0	CCS	Collision_Energy	prec_intenisty	mob_list	ccs_list	int_list
    """

    Scan_Number: int
    sequence: str
    charge: int
    mass: float
    mz: float
    xcorr: float
    retention_time: float
    ook0: float
    CCS: float
    collision_energy: float
    precursor_intensity: float
    mobilogram: List[MobilogramItem]
