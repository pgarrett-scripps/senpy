from typing import List
import ast
from senpy.abstract_class import LineSerializer
from senpy.biosaur.lines import FeatureLine

class DinosuarLineSerializer(LineSerializer):
    @staticmethod
    def deserialize(line: str) -> FeatureLine:
        line_elements = line.rstrip().split("\t")
        mz = float(line_elements[0])
        mostAbundantMz = float(line_elements[1])
        charge = int(line_elements[2])
        rtStart = float(line_elements[3])
        rtApex = float(line_elements[4])
        rtEnd = float(line_elements[5])
        fwhm = float(line_elements[6])
        nIsotopes = int(line_elements[7])
        nScans = int(line_elements[8])
        averagineCorr = float(line_elements[9])
        mass = float(line_elements[10])
        massCalib = float(line_elements[11])
        intensityApex = float(line_elements[12])
        intensitySum = float(line_elements[13])

        feature_line = FeatureLine(massCalib, rtApex, intensityApex, charge, nIsotopes, nScans, None,
                                   None, None, None, None, None,
                                   None, None, None, None, None, mz, rtStart, rtEnd, id,
                                   None, None, None)
        return feature_line


class BiosaurFeatureLineSerializer(LineSerializer):
    @staticmethod
    def deserialize(line: str) -> FeatureLine:
        line_elements = line.rstrip().split("\t")

        neutral_mass = float(line_elements[0])
        rt_apex = float(line_elements[1])
        intensity_apex = float(line_elements[2])
        charge = int(line_elements[3])
        num_isotopes = int(line_elements[4])
        num_scans = int(line_elements[5])
        sulfur = int(line_elements[6])
        cos_corr_1 = float(line_elements[7])
        cos_corr_2 = float(line_elements[8])
        diff_for_output = float(line_elements[9])
        corr_fill_zero = float(line_elements[10])
        intensity_1 = [float(elem) for elem in ast.literal_eval(line_elements[11])]
        scan_id_1 = [int(elem) for elem in ast.literal_eval(line_elements[12])]
        mz_std_1 = float(line_elements[13])
        intensity_2 = [float(elem) for elem in ast.literal_eval(line_elements[14])]
        scan_id_2 = [int(elem) for elem in ast.literal_eval(line_elements[15])]
        mz_std_2 = float(line_elements[16])
        mz = float(line_elements[17])
        rt_start = float(line_elements[18])
        rt_end = float(line_elements[19])
        id = int(line_elements[20])
        ion_mobility = float(line_elements[21])
        faims = int(line_elements[22])
        targeted_mode = [float(elem) for elem in ast.literal_eval(line_elements[23])]

        feature_line = FeatureLine(neutral_mass, rt_apex, intensity_apex, charge, num_isotopes, num_scans, sulfur,
                                   cos_corr_1, cos_corr_2, diff_for_output, corr_fill_zero, intensity_1,
                                   scan_id_1, mz_std_1, intensity_2, scan_id_2, mz_std_2, mz, rt_start, rt_end, id,
                                   ion_mobility, faims, targeted_mode)

        return feature_line

    @staticmethod
    def serialize(s_line: FeatureLine) -> str:
        pass
