import numpy as np

from senpy.abstract_class import LineSerializer
from senpy.outFile.line import OutLine, MobilogramItem


class OutLineSerializer(LineSerializer):
    @staticmethod
    def deserialize(line: str) -> OutLine:
        line_elements = line.rstrip().split("\t")

        Scan_Number = int(line_elements[0])
        sequence = line_elements[1]
        charge = int(line_elements[2])
        mass = float(line_elements[3])
        mz = float(line_elements[4])
        xcorr = float(line_elements[5])
        retention_time = float(line_elements[6])
        ook0 = float(line_elements[7])
        CCS = float(line_elements[8])
        collision_energy = float(line_elements[9])
        precursor_intensity = float(line_elements[10])

        # parse
        ook0_list = np.array(list(float(x) for x in line_elements[11][1:-1].split(", ")), dtype=np.float32)
        ccs_list = np.array(list(float(x) for x in line_elements[12][1:-1].split(", ")), dtype=np.float32)
        intensity_list = np.array(list(float(x) for x in line_elements[13][1:-1].split(", ")), dtype=np.float32)

        mobilogram = []
        for ook0_item, ccs_item, intensity_item in zip(ook0_list, ccs_list, intensity_list):
            mobilogram.append(MobilogramItem(ook0_item, ccs_item, intensity_item))

        line = OutLine(Scan_Number, sequence, charge, mass, mz, xcorr, retention_time, ook0, CCS, collision_energy,
                       precursor_intensity, mobilogram)
        return line

    @staticmethod
    def serialize(line: OutLine) -> str:
        ook0_list = [item.ook0 for item in line.mobilogram]
        ccs_list = [item.ccs for item in line.mobilogram]
        intensity_list = [item.intensity for item in line.mobilogram]

        line_elements = [
                         line.Scan_Number,
                         line.sequence,
                         line.charge,
                         line.mass,
                         line.mz,
                         line.xcorr,
                         line.retention_time,
                         line.ook0,
                         line.CCS,
                         line.collision_energy,
                         line.precursor_intensity,
                         ook0_list,
                         ccs_list,
                         intensity_list
                         ]

        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'
