from senpy.abstract_class import LineSerializer
from senpy.dtaSelectFilter.lines import LocusLine, UniqueLine


class LocusLineSerializer_version_2_1_13(LineSerializer):
    @staticmethod
    def deserialize(line: str) -> LocusLine:
        line_elements = line.rstrip().split("\t")
        locus_name = line_elements[0]
        sequence_count = int(line_elements[1])
        spectrum_count = int(line_elements[2])
        sequence_coverage = float(line_elements[3][:-1])  # remove % sign
        length = int(line_elements[4])
        molWt = int(line_elements[5])
        pi = float(line_elements[6])
        validation_status = str(line_elements[7])
        nsaf = float(line_elements[8])
        empai = float(line_elements[9])
        description_name = str(line_elements[10])

        line = LocusLine(locus_name, sequence_count, spectrum_count, sequence_coverage, length, molWt,
                         pi, validation_status, nsaf, empai, description_name)
        return line

    @staticmethod
    def serialize(locus_line: LocusLine) -> str:
        line_elements = [
            locus_line.locus_name,
            locus_line.sequence_count,
            locus_line.spectrum_count,
            str(round(locus_line.sequence_coverage, 1)) + "%",
            locus_line.length,
            locus_line.molWt,
            round(locus_line.pi, 1),
            locus_line.validation_status,
            round(locus_line.nsaf, 10),
            round(locus_line.empai, 6),
            locus_line.description_name
        ]

        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'


class UniqueLineSerializer_version_2_1_13(LineSerializer):

    @staticmethod
    def deserialize(line: str) -> UniqueLine:
        line_elements = line.rstrip().split("\t")

        is_unique = line_elements[0] == "*"
        file_name = str(line_elements[1].split(".")[0])
        low_scan = int(line_elements[1].split(".")[1])
        high_scan = int(line_elements[1].split(".")[2])
        charge = int(line_elements[1].split(".")[3])
        x_corr = float(line_elements[2])
        delta_cn = float(line_elements[3])
        Conf = float(line_elements[4])
        mass_plus_hydrogen = float(line_elements[5])
        calc_mass_plus_hydrogen = float(line_elements[6])
        ppm = float(line_elements[7])
        total_intensity = float(line_elements[8])
        spr = int(line_elements[9])
        pi = float(line_elements[10])
        ion_proportion = float(line_elements[11])
        redundancy = float(line_elements[12])
        sequence = str(line_elements[13])

        line = UniqueLine(is_unique, file_name, low_scan, high_scan, charge, x_corr, delta_cn, Conf, mass_plus_hydrogen,
                          calc_mass_plus_hydrogen, ppm, total_intensity, spr, pi, ion_proportion, redundancy, sequence)
        return line

    @staticmethod
    def serialize(unique_line: UniqueLine) -> str:
        file_line = '.'.join(
            [unique_line.file_name, str(unique_line.low_scan), str(unique_line.high_scan), str(unique_line.charge)])
        is_unique_symbol = '*' if unique_line.is_unique else ''

        line_elements = [
            is_unique_symbol,
            file_line,
            round(unique_line.x_corr, 4),
            round(unique_line.delta_cn, 4),
            round(unique_line.Conf, 1),
            round(unique_line.mass_plus_hydrogen, 4),
            round(unique_line.calc_mass_plus_hydrogen, 4),
            round(unique_line.ppm, 1),
            round(unique_line.total_intensity, 1),
            unique_line.spr,
            round(unique_line.pi, 3),
            round(unique_line.ion_proportion, 2),
            unique_line.redundancy,
            unique_line.sequence
        ]

        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'


class UniqueLineSerializer_version_2_1_12(LineSerializer):
    """
    Unique	FileName	XCorr	DeltCN	Conf%	M+H+	CalcM+H+	TotalIntensity	SpR	Prob Score	IonProportion	Redundancy	Sequence
    """

    @staticmethod
    def deserialize(line: str) -> UniqueLine:
        line_elements = line.rstrip().split("\t")

        is_unique = line_elements[0] == "*"
        file_name = str(line_elements[1].split(".")[0])
        low_scan = int(line_elements[1].split(".")[1])
        high_scan = int(line_elements[1].split(".")[2])
        charge = int(line_elements[1].split(".")[3])
        x_corr = float(line_elements[2])
        delta_cn = float(line_elements[3])
        Conf = float(line_elements[4])
        mass_plus_hydrogen = float(line_elements[5])
        calc_mass_plus_hydrogen = float(line_elements[6])
        ppm = (mass_plus_hydrogen - calc_mass_plus_hydrogen) / calc_mass_plus_hydrogen * 1_000_000
        total_intensity = float(line_elements[7])
        spr = int(line_elements[8])
        pi = float(line_elements[9])
        ion_proportion = float(line_elements[10])
        redundancy = float(line_elements[11])
        sequence = str(line_elements[12])

        line = UniqueLine(is_unique, file_name, low_scan, high_scan, charge, x_corr, delta_cn, Conf, mass_plus_hydrogen,
                          calc_mass_plus_hydrogen, ppm, total_intensity, spr, pi, ion_proportion, redundancy, sequence)
        return line

    @staticmethod
    def serialize(unique_line: UniqueLine) -> str:
        file_line = '.'.join(
            [unique_line.file_name, str(unique_line.low_scan), str(unique_line.high_scan), str(unique_line.charge)])
        is_unique_symbol = '*' if unique_line.is_unique else ''

        line_elements = [
            is_unique_symbol,
            file_line,
            round(unique_line.x_corr, 4),
            round(unique_line.delta_cn, 4),
            round(unique_line.Conf, 1),
            round(unique_line.mass_plus_hydrogen, 4),
            round(unique_line.calc_mass_plus_hydrogen, 4),
            round(unique_line.total_intensity, 1),
            unique_line.spr,
            round(unique_line.pi, 3),
            round(unique_line.ion_proportion, 2),
            unique_line.redundancy,
            unique_line.sequence
        ]

        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'


class LocusLineSerializer_version_2_1_12(LocusLineSerializer_version_2_1_13):
    """
    Locus	Sequence Count	Spectrum Count	Sequence Coverage	Length	MolWt	pI	Validation Status	NSAF	EMPAI	Descriptive Name

    Same as version 2_1_12
    """
    pass
