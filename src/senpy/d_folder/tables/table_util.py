from sqlite3 import Connection
from typing import Union, List, Any
from enum import Enum


class TableNames(Enum):
    PRECURSORS = "Precursors"
    PASEF_FRAME_MSMS_INFO = "PasefFrameMsMsInfo"
    FRAMES = "Frames"


def get_table_rows(conn: Connection, table_name: TableNames) -> List[Any]:
    """
    Query all rows in the table
    :param conn: analysis.tdf connection object
    :param table_name: name of the table
    :return: table rows
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name.value}")
    rows = cur.fetchall()
    return rows


def cast_float(val: Any) -> Union[float, None]:
    return float(val) if val else None


def cast_int(val: Any) -> Union[int, None]:
    return int(val) if val else None


def cast_str(val: Any) -> Union[str, None]:
    return str(val) if val else None