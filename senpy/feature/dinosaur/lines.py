from dataclasses import dataclass
from enum import Enum
from typing import List, Union, Any, ClassVar

from util import cast_float, cast_int


class _DinosaurFeatureLineDeserializationException(Exception):

    def __init__(self, _row: List[Any]):
        self.row = _row

    def __repr__(self) -> str:
        return f"Error deserializing Dinosaur feature row: '{self.row}'"


class _DinosaurFeatureLineColumns(Enum):
    """
    Enum class to represent Dinosaur feature column numbers
    """
    mz = 0
    most_abundant_mz = 1
    charge = 2
    rt_start = 3
    rt_apex = 4
    rt_end = 5
    fwhm = 6
    num_isotopes = 7
    num_scans = 8
    averagine_corr = 9
    mass = 10
    mass_calib = 11
    intensity_apex = 12
    intensity_sum = 13


@dataclass
class DinosaurFeatureLine:
    """
    Class keeping track of Dinosaur features.

    Example Dinosaur line:
        mz	mostAbundantMz	charge	rtStart	rtApex	rtEnd	fwhm	nIsotopes	nScans	averagineCorr	mass	\
        massCalib	intensityApex	intensitySum
    """
    mz: Union[float, None]
    most_abundant_mz: Union[float, None]
    charge: Union[int, None]
    rt_start: Union[float, None]
    rt_apex: Union[float, None]
    rt_end: Union[float, None]
    fwhm: Union[float, None]
    num_isotopes: Union[int, None]
    num_scans: Union[int, None]
    averagine_corr: Union[float, None]
    mass: Union[float, None]
    mass_calib: Union[float, None]
    intensity_apex: Union[int, None]
    intensity_sum: Union[float, None]

    _LINE_ELEMENTS: ClassVar[int] = len(_DinosaurFeatureLineColumns)

    @staticmethod
    def get_number_elements() -> int:
        return DinosaurFeatureLine._LINE_ELEMENTS

    @staticmethod
    def deserialize(line: str) -> 'DinosaurFeatureLine':
        line_elements = line.rstrip().split("\t")

        if len(line_elements) != len(_DinosaurFeatureLineColumns):
            raise _DinosaurFeatureLineDeserializationException(line_elements)

        mz = cast_float(line_elements[_DinosaurFeatureLineColumns.mz.value])
        most_abundant_mz = cast_float(line_elements[_DinosaurFeatureLineColumns.most_abundant_mz.value])
        charge = cast_int(line_elements[_DinosaurFeatureLineColumns.charge.value])
        rt_start = cast_float(line_elements[_DinosaurFeatureLineColumns.rt_start.value])
        rt_apex = cast_float(line_elements[_DinosaurFeatureLineColumns.rt_apex.value])
        rt_end = cast_float(line_elements[_DinosaurFeatureLineColumns.rt_end.value])
        fwhm = cast_float(line_elements[_DinosaurFeatureLineColumns.fwhm.value])
        num_isotopes = cast_int(line_elements[_DinosaurFeatureLineColumns.num_isotopes.value])
        num_scans = cast_int(line_elements[_DinosaurFeatureLineColumns.num_scans.value])
        averagine_corr = cast_float(line_elements[_DinosaurFeatureLineColumns.averagine_corr.value])
        mass = cast_float(line_elements[_DinosaurFeatureLineColumns.mass.value])
        mass_calib = cast_float(line_elements[_DinosaurFeatureLineColumns.mass_calib.value])
        intensity_apex = cast_float(line_elements[_DinosaurFeatureLineColumns.intensity_apex.value])
        intensity_sum = cast_float(line_elements[_DinosaurFeatureLineColumns.intensity_sum.value])

        feature_line = DinosaurFeatureLine(mz=mz,
                                           most_abundant_mz=most_abundant_mz,
                                           charge=charge,
                                           rt_start=rt_start,
                                           rt_apex=rt_apex,
                                           rt_end=rt_end,
                                           fwhm=fwhm,
                                           num_isotopes=num_isotopes,
                                           num_scans=num_scans,
                                           averagine_corr=averagine_corr,
                                           mass=mass,
                                           mass_calib=mass_calib,
                                           intensity_apex=intensity_apex,
                                           intensity_sum=intensity_sum
                                           )
        return feature_line

    @staticmethod
    def serialize(self) -> str:
        pass
