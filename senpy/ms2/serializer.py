import numpy as np

from senpy.abstract_class import LineSerializer
from senpy.ms2.lines import SLine, ILine, ZLine, PeakLine


class SLineSerializer(LineSerializer):
    @staticmethod
    def deserialize(line: str) -> SLine:
        line_elements = line.rstrip().split("\t")
        low_scan = int(line_elements[1])
        high_scan = int(line_elements[2])
        mz = np.float32(line_elements[3])
        return SLine(low_scan, high_scan, mz)

    @staticmethod
    def serialize(s_line: SLine) -> str:
        line_elements = ["S",
                         f"{s_line.low_scan:06d}",
                         f"{s_line.high_scan:06d}",
                         s_line.mz
                         ]
        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'

class ILineSerializer(LineSerializer):
    @staticmethod
    def deserialize(line: str) -> ILine:
        line_elements = line.rstrip().split("\t")
        keyword = line_elements[1]
        value = line_elements[2]
        return ILine(keyword, value)

    @staticmethod
    def serialize(i_line: ILine) -> str:
        line_elements = ["I",
                         i_line.keyword,
                         i_line.value
                         ]
        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'

class ZLineSerializer(LineSerializer):
    @staticmethod
    def deserialize(line: str) -> ZLine:
        line_elements = line.rstrip().split("\t")
        charge = int(line_elements[1])
        mass = np.float32(line_elements[2])
        return ZLine(charge, mass)

    @staticmethod
    def serialize(z_line: ZLine) -> str:
        line_elements = ["Z",
                         z_line.charge,
                         round(float(z_line.mass), 4),
                         ]
        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'

class PeakLineSerializer(LineSerializer):
    @staticmethod
    def deserialize(line: str) -> PeakLine:
        line_elements = line.rstrip().split(" ")
        mz = np.float32(line_elements[0])
        intensity = np.float32(line_elements[1])
        peak_line = np.array([(mz, intensity)], dtype=PeakLine)[0]
        return peak_line

    @staticmethod
    def serialize(peak_line: PeakLine) -> str:
        line_elements = [round(float(peak_line[0]), 4),
                         round(float(peak_line[1]), 1),
                         ]
        line_elements = [str(elem) for elem in line_elements]

        return ' '.join(line_elements) + '\n'

