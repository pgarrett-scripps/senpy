from dataclasses import dataclass
from enum import Enum
from sqlite3 import Connection
from typing import Union, List, Any

from .table_util import get_table_rows, cast_int, cast_float, cast_str, TableNames


class _FramesTableDeserializationException(Exception):

    def __init__(self, _row: List[Any]):
        self.row = _row

    def __repr__(self) -> str:
        return f"Error deserializing Frames table: '{self.row}'"


class _FramesTableColumns(Enum):
    """
    Enum class to represent frames table column numbers
    """
    id = 0
    time = 1
    polarity = 2
    scan_mode = 3
    msms_type = 4
    tims_id = 5
    max_intensity = 6
    summed_intensity = 7
    num_scans = 8
    num_peaks = 9
    mz_calibration = 10
    t1 = 11
    t2 = 12
    tims_calibration = 13
    property_group = 14
    accumulation_time = 15
    ramp_time = 16
    pressure = 17


@dataclass
class FramesTableItem:
    """
    Dataclass to store Frames table row information
    """
    id: Union[int, None]
    time: Union[float, None]
    polarity: Union[str, None]
    scan_mode: Union[int, None]
    msms_type: Union[int, None]
    tims_id: Union[int, None]
    max_intensity: Union[int, None]
    summed_intensity: Union[int, None]
    num_scans: Union[int, None]
    num_peaks: Union[int, None]
    mz_calibration: Union[int, None]
    t1: Union[float, None]
    t2: Union[float, None]
    tims_calibration: Union[int, None]
    property_group: Union[int, None]
    accumulation_time: Union[float, None]
    ramp_time: Union[float, None]
    pressure: Union[float, None]

    __slots__ = 'id', 'time', 'polarity', 'scan_mode', 'msms_type', 'tims_id', 'max_intensity', 'summed_intensity', \
                'num_scans', 'num_peaks', 'mz_calibration', 't1', 't2', 'tims_calibration', 'property_group', \
                'accumulation_time', 'ramp_time', 'pressure'


def get_frame_table_items(conn: Connection) -> List[FramesTableItem]:
    """
    Parses Frames table into a list of FramesTableItem's
    :param conn: analysis.tdf connection object
    :return: list of FramesTableItem's
    """
    rows = get_table_rows(conn, TableNames.FRAMES)

    items = []
    for row in rows:
        if len(row) == len(_FramesTableColumns):
            print(row[_FramesTableColumns.msms_type.value])
            item = FramesTableItem(id=cast_int(row[_FramesTableColumns.id.value]),
                                   time=cast_float(row[_FramesTableColumns.time.value]),
                                   polarity=cast_str(row[_FramesTableColumns.polarity.value]),
                                   scan_mode=cast_int(row[_FramesTableColumns.scan_mode.value]),
                                   msms_type=cast_int(row[_FramesTableColumns.msms_type.value]),
                                   tims_id=cast_int(row[_FramesTableColumns.tims_id.value]),
                                   max_intensity=cast_int(row[_FramesTableColumns.max_intensity.value]),
                                   summed_intensity=cast_int(row[_FramesTableColumns.summed_intensity.value]),
                                   num_scans=cast_int(row[_FramesTableColumns.num_scans.value]),
                                   num_peaks=cast_int(row[_FramesTableColumns.num_peaks.value]),
                                   mz_calibration=cast_int(row[_FramesTableColumns.mz_calibration.value]),
                                   t1=cast_float(row[_FramesTableColumns.t1.value]),
                                   t2=cast_float(row[_FramesTableColumns.t2.value]),
                                   tims_calibration=cast_int(row[_FramesTableColumns.tims_calibration.value]),
                                   property_group=cast_int(row[_FramesTableColumns.property_group.value]),
                                   accumulation_time=cast_float(row[_FramesTableColumns.accumulation_time.value]),
                                   ramp_time=cast_float(row[_FramesTableColumns.ramp_time.value]),
                                   pressure=cast_float(row[_FramesTableColumns.pressure.value]))

        # Some tdf Files do not have pressure column
        elif len(row) == len(_FramesTableColumns) - 1:
            item = FramesTableItem(id=cast_int(row[_FramesTableColumns.id.value]),
                                   time=cast_float(row[_FramesTableColumns.time.value]),
                                   polarity=cast_str(row[_FramesTableColumns.polarity.value]),
                                   scan_mode=cast_int(row[_FramesTableColumns.scan_mode.value]),
                                   msms_type=cast_int(row[_FramesTableColumns.msms_type.value]),
                                   tims_id=cast_int(row[_FramesTableColumns.tims_id.value]),
                                   max_intensity=cast_int(row[_FramesTableColumns.max_intensity.value]),
                                   summed_intensity=cast_int(row[_FramesTableColumns.summed_intensity.value]),
                                   num_scans=cast_int(row[_FramesTableColumns.num_scans.value]),
                                   num_peaks=cast_int(row[_FramesTableColumns.num_peaks.value]),
                                   mz_calibration=cast_int(row[_FramesTableColumns.mz_calibration.value]),
                                   t1=cast_float(row[_FramesTableColumns.t1.value]),
                                   t2=cast_float(row[_FramesTableColumns.t2.value]),
                                   tims_calibration=cast_int(row[_FramesTableColumns.tims_calibration.value]),
                                   property_group=cast_int(row[_FramesTableColumns.property_group.value]),
                                   accumulation_time=cast_float(row[_FramesTableColumns.accumulation_time.value]),
                                   ramp_time=cast_float(row[_FramesTableColumns.ramp_time.value]),
                                   pressure=None)
        else:
            raise _FramesTableDeserializationException(_row=row)
        items.append(item)
    return items
