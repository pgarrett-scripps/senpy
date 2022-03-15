import ast
from dataclasses import dataclass
from enum import Enum
from typing import List, Union, Any, ClassVar

from util import cast_float, cast_int


class _BiosaurFeatureLineDeserializationException(Exception):

    def __init__(self, _row: List[Any]):
        self.row = _row

    def __repr__(self) -> str:
        return f"Error deserializing Biosaur feature row '{self.row}'"


class _BiosaurFeatureLineColumns(Enum):
    """
    Enum class to represent Biosaur feature column numbers
    """
    neutral_mass = 0
    rt_apex = 1
    intensity_apex = 2
    charge = 3
    num_isotopes = 4
    num_scans = 5
    sulfur = 6
    cos_corr_1 = 7
    cos_corr_2 = 8
    diff_for_output = 9
    corr_fill_zero = 10
    intensity_1 = 11
    scan_id_1 = 12
    mz_std_1 = 13
    intensity_2 = 14
    scan_id_2 = 15
    mz_std_2 = 16
    mz = 17
    rt_start = 18
    rt_end = 19
    id = 20
    ion_mobility = 21
    faims = 22
    targeted_mode = 23


@dataclass
class BiosaurFeatureLine:
    """
    Class keeping track of Biosaur features.

    Example Biosaur line:
        massCalib	rtApex	intensityApex	charge	nIsotopes	nScans	sulfur	cos_corr_1	cos_corr_2	\
        diff_for_output	corr_fill_zero	intensity_1	scan_id_1	mz_std_1	intensity_2	scan_id_2	mz_std_2	\
        mz	rtStart	rtEnd	id	ion_mobility	FAIMS	targeted_mode
    """
    neutral_mass: Union[float, None]
    rt_apex: Union[float, None]
    intensity_apex: Union[float, None]
    charge: Union[int, None]
    num_isotopes: Union[int, None]
    num_scans: Union[int, None]
    sulfur: Union[int, None]
    cos_corr_1: Union[float, None]
    cos_corr_2: Union[float, None]
    diff_for_output: Union[float, None]
    corr_fill_zero: Union[float, None]
    intensity_1: List[Union[float, None]]
    scan_id_1: List[Union[int, None]]
    mz_std_1: Union[float, None]
    intensity_2: List[Union[float, None]]
    scan_id_2: List[Union[int, None]]
    mz_std_2: Union[float, None]
    mz: Union[float, None]
    rt_start: Union[float, None]
    rt_end: Union[float, None]
    id: Union[int, None]
    ion_mobility: Union[float, None]
    faims: Union[int, None]
    targeted_mode: Union[float, None]

    _LINE_ELEMENTS: ClassVar[int] = len(_BiosaurFeatureLineColumns)

    @staticmethod
    def get_number_elements() -> int:
        return BiosaurFeatureLine._LINE_ELEMENTS

    @staticmethod
    def deserialize(line: str) -> 'BiosaurFeatureLine':
        line_elements = line.rstrip().split("\t")

        if len(line_elements) != len(_BiosaurFeatureLineColumns):
            raise _BiosaurFeatureLineDeserializationException(line_elements)

        neutral_mass = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        rt_apex = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        intensity_apex = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        charge = cast_int(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        num_isotopes = cast_int(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        num_scans = cast_int(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        sulfur = cast_int(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        cos_corr_1 = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        cos_corr_2 = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        diff_for_output = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        corr_fill_zero = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        intensity_1 = [cast_float(elem) for elem
                       in ast.literal_eval(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])]
        scan_id_1 = [cast_int(elem) for elem
                     in ast.literal_eval(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])]
        mz_std_1 = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        intensity_2 = [cast_float(elem) for elem
                       in ast.literal_eval(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])]
        scan_id_2 = [cast_int(elem) for elem
                     in ast.literal_eval(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])]
        mz_std_2 = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        mz = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        rt_start = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        rt_end = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        id = cast_int(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        ion_mobility = cast_float(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        faims = cast_int(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])
        targeted_mode = [cast_float(elem) for elem
                         in ast.literal_eval(line_elements[_BiosaurFeatureLineColumns.neutral_mass.value])]

        feature_line = BiosaurFeatureLine(
            neutral_mass=neutral_mass,
            rt_apex=rt_apex,
            intensity_apex=intensity_apex,
            charge=charge,
            num_isotopes=num_isotopes,
            num_scans=num_scans,
            sulfur=sulfur,
            cos_corr_1=cos_corr_1,
            cos_corr_2=cos_corr_2,
            diff_for_output=diff_for_output,
            corr_fill_zero=corr_fill_zero,
            intensity_1=intensity_1,
            scan_id_1=scan_id_1,
            mz_std_1=mz_std_1,
            intensity_2=intensity_2,
            scan_id_2=scan_id_2,
            mz_std_2=mz_std_2,
            mz=mz,
            rt_start=rt_start,
            rt_end=rt_end,
            id=id,
            ion_mobility=ion_mobility,
            faims=faims,
            targeted_mode=targeted_mode
        )

        return feature_line

    @staticmethod
    def serialize(self) -> str:
        pass
