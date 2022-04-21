from dataclasses import dataclass
from sqlite3 import Connection
from enum import Enum
from typing import Union, List, Any

from tables.table_util import get_table_rows, cast_int, cast_float, TableNames


class _PrecursorTableDeserializationException(Exception):

    def __init__(self, _row: List[Any]):
        self.row = _row

    def __repr__(self) -> str:
        return f"Error deserializing Precursors table: '{self.row}'"


class _PrecursorsTableColumns(Enum):
    """
    Enum class to represent precursors table column numbers
    """
    id = 0
    largest_peak_mz = 1
    average_mz = 2
    monoisotopic_mz = 3
    charge = 4
    scan_number = 5
    intensity = 6
    parent_frame = 7


@dataclass
class PrecursorsTableItem:
    """
    Dataclass to store Precursors table row information
    """
    id: Union[int, None]
    largest_peak_mz: Union[float, None]
    average_mz: Union[float, None]
    monoisotopic_mz: Union[float, None]
    charge: Union[int, None]
    scan_number: Union[float, None]
    intensity: Union[float, None]
    parent_frame: Union[int, None]

    __slots__ = 'id', 'largest_peak_mz', 'average_mz', 'monoisotopic_mz', 'charge', 'scan_number', 'intensity', \
                'parent_frame'


def get_precursors_table_items(conn: Connection) -> List[PrecursorsTableItem]:
    """
    Parses Precursors table into a list of PrecursorsTableItem's
    :param conn: analysis.tdf connection object
    :return: list of PrecursorsTableItem's
    """
    rows = get_table_rows(conn, TableNames.PRECURSORS)

    items = []
    for row in rows:
        if len(row) == len(_PrecursorsTableColumns):
            item = PrecursorsTableItem(id=cast_int(row[_PrecursorsTableColumns.id.value]),
                                       largest_peak_mz=cast_float(row[_PrecursorsTableColumns.largest_peak_mz.value]),
                                       average_mz=cast_float(row[_PrecursorsTableColumns.average_mz.value]),
                                       monoisotopic_mz=cast_float(row[_PrecursorsTableColumns.monoisotopic_mz.value]),
                                       charge=cast_int(row[_PrecursorsTableColumns.charge.value]),
                                       scan_number=cast_float(row[_PrecursorsTableColumns.scan_number.value]),
                                       intensity=cast_float(row[_PrecursorsTableColumns.intensity.value]),
                                       parent_frame=cast_int(row[_PrecursorsTableColumns.parent_frame.value])
                                       )
        else:
            raise _PrecursorTableDeserializationException(_row=row)
        items.append(item)
    return items
