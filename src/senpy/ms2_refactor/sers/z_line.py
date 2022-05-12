import dataclasses
from enum import Enum
from functools import lru_cache
from typing import Callable

import numpy as np

from ..exceptions import Ms2FileDeserializationZLineException
from ..columns import ZLineColumns
from ..lines import ZLine
from .line import LineSerializer


class ZLineSerializer(LineSerializer):

    def __init__(self, columns: Enum, mass_precision: int = 5):
        super().__init__(columns=columns,
                         ms2_line=ZLine,
                         line_exception=Ms2FileDeserializationZLineException,
                         line_letter="Z")

        self.MASS_PRECISION = mass_precision

    def __hash__(self):
        return hash((hash(super), self.MASS_PRECISION))

    @lru_cache(maxsize=None)
    def get_serializer_by_name(self, name: str) -> Callable:
        if name == "letter":
            return self.serialize_letter
        if name == "charge":
            return self.serialize_charge
        elif name == "mass":
            return self.serialize_mass
        else:
            raise NotImplementedError

    def serialize_letter(self, letter: str) -> str:
        return letter

    def serialize_charge(self, val: np.uint8) -> str:
        return f"{val}"

    def serialize_mass(self, val: np.float32) -> str:
        return f"{val:.{self.MASS_PRECISION}f}"

    @lru_cache(maxsize=None)
    def get_deserializer_by_name(self, name: str) -> Callable:
        if name == "letter":
            return self.deserialize_letter
        if name == "charge":
            return self.deserialize_charge
        elif name == "mass":
            return self.deserialize_mass
        else:
            raise NotImplementedError

    def deserialize_letter(self, val: str) -> str:
        return val

    def deserialize_charge(self, val: str) -> np.uint8:
        return np.uint32(val)

    def deserialize_mass(self, val: str) -> np.float32:
        return np.float32(val)


if __name__ == '__main__':
    sample_s_line = "Z\t2\t2000.2\n"

    print(type(ZLine))
    print(dataclasses.fields(ZLine))
    print({field.name: field.type for i, field in enumerate(dataclasses.fields(ZLine))})
    ser = ZLineSerializer(ZLineColumns)
    line = ser.deserialize(sample_s_line)
    print(ser)
    print(line)
    print(ser.serialize(line))

    for i in range(1_000_000):
        line = ser.deserialize(sample_s_line)

    print("done")


