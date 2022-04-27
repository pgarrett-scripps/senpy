import ast
from dataclasses import dataclass
from enum import Enum
from typing import List, ClassVar, Union
from senpy.util import Line


class _OutLineColumns(Enum):
    scan_number = 0
    sequence = 1
    charge = 2
    mass = 3
    mz = 4
    x_corr = 5
    retention_time = 6
    OOK0 = 7
    CCS = 8
    collision_energy = 9
    precursor_intensity = 10
    OOK0_spectra = 11
    CCS_spectra = 12
    intensity_spectra = 13
    mz_spectra = 14


@dataclass
class OutLine(Line):
    """
    DataClass for holding information in out file

    Example out line:
        scan_number|seq|charge|mass|mz|xcorr|RetTime|OOK0|CCS|Collision_Energy|prec_intensity|mob_list|ccs_list|int_list
    """

    scan_number: int
    sequence: str
    charge: int
    mass: float
    mz: float
    x_corr: float
    retention_time: float
    OOK0: float
    CCS: float
    collision_energy: float
    precursor_intensity: float
    OOK0_spectra: List[float]
    CCS_spectra: List[float]
    intensity_spectra: List[float]
    mz_spectra: Union[List[float], None]

    MASS_PRECISION: ClassVar[int] = 5
    MZ_PRECISION: ClassVar[int] = 5
    X_CORR_PRECISION: ClassVar[int] = 4
    RETENTION_TIME_PRECISION: ClassVar[int] = 4
    OOK0_PRECISION: ClassVar[int] = 4
    CCS_PRECISION: ClassVar[int] = 1
    COLLISION_ENERGY_PRECISION: ClassVar[int] = 1
    INTENSITY_PRECISION: ClassVar[int] = 1

    @staticmethod
    def get_header() -> str:
        return '\t'.join([column.name for column in _OutLineColumns]) + '\n'

    @staticmethod
    def deserialize(line: str) -> 'OutLine':
        line_elements = line.rstrip().split("\t")

        scan_number = int(line_elements[_OutLineColumns.scan_number.value])
        sequence = line_elements[_OutLineColumns.sequence.value]
        charge = int(line_elements[_OutLineColumns.charge.value])
        mass = float(line_elements[_OutLineColumns.mass.value])
        mz = float(line_elements[_OutLineColumns.mz.value])
        x_corr = float(line_elements[_OutLineColumns.x_corr.value])
        retention_time = float(line_elements[_OutLineColumns.retention_time.value])
        OOK0 = float(line_elements[_OutLineColumns.OOK0.value])
        CCS = float(line_elements[_OutLineColumns.CCS.value])
        collision_energy = float(line_elements[_OutLineColumns.collision_energy.value])
        precursor_intensity = float(line_elements[_OutLineColumns.precursor_intensity.value])
        OOK0_spectra = [float(val) for val in ast.literal_eval(line_elements[_OutLineColumns.OOK0_spectra.value])]
        CCS_spectra = [float(val) for val in ast.literal_eval(line_elements[_OutLineColumns.CCS_spectra.value])]
        intensity_spectra = [float(val) for val in
                             ast.literal_eval(line_elements[_OutLineColumns.intensity_spectra.value])]

        mz_spectra = None
        if len(line_elements) == len(_OutLineColumns):
            mz_spectra = [float(val) for val in
                          ast.literal_eval(line_elements[_OutLineColumns.mz_spectra.value])]

        line = OutLine(scan_number=scan_number,
                       sequence=sequence,
                       charge=charge,
                       mass=mass,
                       mz=mz,
                       x_corr=x_corr,
                       retention_time=retention_time,
                       OOK0=OOK0,
                       CCS=CCS,
                       collision_energy=collision_energy,
                       precursor_intensity=precursor_intensity,
                       OOK0_spectra=OOK0_spectra,
                       CCS_spectra=CCS_spectra,
                       intensity_spectra=intensity_spectra,
                       mz_spectra=mz_spectra
                       )
        return line

    def serialize(self) -> str:
        line_elements = [""] * len(_OutLineColumns)
        line_elements[_OutLineColumns.scan_number.value] = self.scan_number
        line_elements[_OutLineColumns.sequence.value] = self.sequence
        line_elements[_OutLineColumns.charge.value] = f"{self.charge}"
        line_elements[_OutLineColumns.mass.value] = f"{self.mass:.{self.MASS_PRECISION}f}" if type(
            self.mass) != str else self.mass
        line_elements[_OutLineColumns.mz.value] = f"{self.mz:.{self.MZ_PRECISION}f}" if type(
            self.mz) != str else self.mz
        line_elements[_OutLineColumns.x_corr.value] = f"{self.x_corr:.{self.X_CORR_PRECISION}f}" if type(
            self.x_corr) != str else self.x_corr
        line_elements[
            _OutLineColumns.retention_time.value] = f"{self.retention_time:.{self.RETENTION_TIME_PRECISION}f}" if type(
            self.retention_time) != str else self.retention_time
        line_elements[_OutLineColumns.OOK0.value] = f"{self.OOK0:.{self.OOK0_PRECISION}f}" if type(
            self.OOK0) != str else self.OOK0
        line_elements[_OutLineColumns.CCS.value] = f"{self.CCS:.{self.CCS_PRECISION}f}" if type(
            self.CCS) != str else self.CCS
        line_elements[_OutLineColumns.collision_energy.value] = \
            f"{self.collision_energy:.{self.COLLISION_ENERGY_PRECISION}f}" if type(
                self.collision_energy) != str else self.collision_energy
        line_elements[_OutLineColumns.precursor_intensity.value] = \
            f"{self.precursor_intensity:.{self.INTENSITY_PRECISION}f} " if type(
                self.precursor_intensity) != str else self.precursor_intensity
        line_elements[_OutLineColumns.OOK0_spectra.value] = \
            str([f"{val:.{self.OOK0_PRECISION}f}" for val in self.OOK0_spectra]).replace("'", "") if type(
                self.OOK0_spectra) != str else self.OOK0_spectra
        line_elements[_OutLineColumns.CCS_spectra.value] = \
            str([f"{val:.{self.CCS_PRECISION}f}" for val in self.CCS_spectra]).replace("'", "") if type(
                self.CCS_spectra) != str else self.CCS_spectra
        line_elements[_OutLineColumns.intensity_spectra.value] = \
            str([f"{val:.{self.INTENSITY_PRECISION}f}" for val in self.intensity_spectra]).replace("'", "") if type(
                self.intensity_spectra) != str else self.intensity_spectra
        line_elements[_OutLineColumns.mz_spectra.value] = \
            str([f"{val:.{self.MZ_PRECISION}f}" for val in self.mz_spectra]).replace("'", "") if type(
                self.mz_spectra) != str else self.mz_spectra
        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'
