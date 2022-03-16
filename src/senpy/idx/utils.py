import sqlite3
from sqlite3 import Error
import struct

END_INT_VALUE = 2147483647
BYTES_SIZE = 4


def convert_float(element: bytes) -> float:
    return float(list(struct.iter_unpack('<f', element))[0][0])


def convert_int(element: bytes) -> int:
    import struct
    return int(list(struct.iter_unpack('<i', element))[0][0])


def convert_chr(element: bytes) -> str:
    import struct
    return struct.iter_unpack('<s', element)


def convert_float_to_bytes(element: float) -> bytes:
    import struct
    return struct.pack('<f', element)


def convert_int_to_bytes(element: int) -> bytes:
    import struct
    return struct.pack('<i', element)


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
