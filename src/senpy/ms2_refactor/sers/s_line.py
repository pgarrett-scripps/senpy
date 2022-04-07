import dataclasses
from enum import Enum
from functools import lru_cache
from typing import Callable

import numpy as np

from senpy.ms2_refactor.exceptions import Ms2FileDeserializationSLineException
from senpy.ms2_refactor.columns import SLineColumns
from senpy.ms2_refactor.lines import SLine
from senpy.ms2_refactor.sers.line import LineSerializer


class SLineSerializer(LineSerializer):

    def __init__(self, columns: Enum, low_scan_length: int = 6, high_scan_length: int = 6, mz_precision: int = 5):
        super().__init__(columns=columns,
                         ms2_line=SLine,
                         line_exception=Ms2FileDeserializationSLineException,
                         line_letter="S")

        self.LOW_SCAN_LENGTH = low_scan_length
        self.HIGH_SCAN_LENGTH = high_scan_length
        self.MZ_PRECISION = mz_precision

    def __hash__(self):
        return hash((hash(super), self.LOW_SCAN_LENGTH, self.HIGH_SCAN_LENGTH, self.MZ_PRECISION))

    @lru_cache(maxsize=None)
    def get_serializer_by_name(self, name: str) -> Callable:
        if name == "letter":
            return self.serialize_letter
        if name == "low_scan":
            return self.serialize_low_scan
        elif name == "high_scan":
            return self.serialize_high_scan
        elif name == "mz":
            return self.serialize_mz
        else:
            raise NotImplementedError

    def serialize_letter(self, letter: str) -> str:
        return letter

    def serialize_low_scan(self, val: np.uint32) -> str:
        return f"{val:0{self.LOW_SCAN_LENGTH}d}"

    def serialize_high_scan(self, val: np.uint32) -> str:
        return f"{val:0{self.HIGH_SCAN_LENGTH}d}"

    def serialize_mz(self, val: np.float32) -> str:
        return f"{val:.{self.MZ_PRECISION}f}"

    @lru_cache(maxsize=None)
    def get_deserializer_by_name(self, name: str) -> Callable:
        if name == "letter":
            return self.deserialize_letter
        if name == "low_scan":
            return self.deserialize_low_scan
        elif name == "high_scan":
            return self.deserialize_high_scan
        elif name == "mz":
            return self.deserialize_mz
        else:
            raise NotImplementedError

    def deserialize_letter(self, val: str) -> str:
        return val

    def deserialize_low_scan(self, val: str) -> np.uint32:
        return np.uint32(val)

    def deserialize_high_scan(self, val: str) -> np.uint32:
        return np.uint32(val)

    def deserialize_mz(self, val: str) -> np.float32:
        return np.float32(val)


if __name__ == '__main__':
    sample_s_line = "S\t100\t200\t1000.01\n"

    print(SLine.low_scan, SLine.low_scan == "low_scan")
    print(type(SLine))
    print(dataclasses.fields(SLine))
    print({field.name: field.type for i, field in enumerate(dataclasses.fields(SLine))})
    print(type(getattr(SLine, 'mz')))
    ser = SLineSerializer(SLineColumns)
    print(ser)
    line = ser.deserialize(sample_s_line)
    print(line)
    print(ser.serialize(line))
