from dataclasses import dataclass
from enum import Enum
from sqlite3 import Connection
from typing import Union, List, Any

from senpy.tdf_tables.table_util import get_table_rows, cast_int, cast_float, cast_str, TableNames


class _PasefFrameMsMsInfoDeserializationException(Exception):

    def __init__(self, _row: List[Any]):
        self.row = _row

    def __repr__(self) -> str:
        return f"Error deserializing PasefFrameMsMsInfo table: '{self.row}'"


class _PasefFrameMsMsInfoTableColumns(Enum):
    """
    Enum class to represent PasefFrameMsMsInfo table column numbers
    """
    ms1_frame_id = 0
    scan_number_begin = 1
    scan_number_end = 2
    isolation_mz = 3
    isolation_width = 4
    collision_energy = 5
    precursor_id = 6


@dataclass
class PasefFrameMsMsInfoTableItem:
    """
    Dataclass to store PasefFrameMsMsInfo table row information
    """
    ms1_frame_id: Union[int, None]
    scan_number_begin: Union[float, None]
    scan_number_end: Union[float, None]
    isolation_mz: Union[float, None]
    isolation_width: Union[float, None]
    collision_energy: Union[float, None]
    precursor_id: Union[int, None]

    __slots__ = 'ms1_frame_id', 'scan_number_begin', 'scan_number_end', 'isolation_mz', 'isolation_width', \
                'collision_energy', 'precursor_id'


def get_pasef_frame_msms_table_items(conn: Connection) -> List[PasefFrameMsMsInfoTableItem]:
    """
    Parses PasefFrameMsMsInfo table into a list of PasefFrameMsMsInfoTableItem's
    :param conn: analysis.tdf connection object
    :return: list of PasefFrameMsMsInfoTableItem's
    """
    rows = get_table_rows(conn, TableNames.PASEF_FRAME_MSMS_INFO)

    items = []
    for row in rows:
        if len(row) == len(_PasefFrameMsMsInfoTableColumns):
            item = PasefFrameMsMsInfoTableItem(
                ms1_frame_id=cast_int(row[_PasefFrameMsMsInfoTableColumns.ms1_frame_id.value]),
                scan_number_begin=cast_float(row[_PasefFrameMsMsInfoTableColumns.scan_number_begin.value]),
                scan_number_end=cast_float(row[_PasefFrameMsMsInfoTableColumns.scan_number_end.value]),
                isolation_mz=cast_float(row[_PasefFrameMsMsInfoTableColumns.isolation_mz.value]),
                isolation_width=cast_float(row[_PasefFrameMsMsInfoTableColumns.isolation_width.value]),
                collision_energy=cast_float(row[_PasefFrameMsMsInfoTableColumns.collision_energy.value]),
                precursor_id=cast_int(row[_PasefFrameMsMsInfoTableColumns.precursor_id.value])
            )
        else:
            raise _PasefFrameMsMsInfoDeserializationException(_row=row)
        items.append(item)
    return items
