from dataclasses import dataclass, field
from enum import Enum
from typing import List, ClassVar, Union

from senpy.util import Line


class _PeptideLineColumns_v1_2_13(Enum):
    is_unique = 0
    file_name = 1
    x_corr = 2
    delta_cn = 3
    conf = 4
    mass_plus_hydrogen = 5
    calc_mass_plus_hydrogen = 6
    ppm = 7
    total_intensity = 8
    spr = 9
    pi = 10
    ion_proportion = 11
    redundancy = 12
    sequence = 13


class _PeptideLineColumns_v1_2_12(Enum):
    """
    Unique|FileName|XCorr|DeltCN|Conf%|M+H+|CalcM+H+|TotalIntensity|SpR|Prob_Score|IonProportion|Redundancy|Sequence
    """
    is_unique = 0
    file_name = 1
    x_corr = 2
    delta_cn = 3
    conf = 4
    mass_plus_hydrogen = 5
    calc_mass_plus_hydrogen = 6
    total_intensity = 7
    spr = 8
    prob_score = 9
    ion_proportion = 10
    redundancy = 11
    sequence = 12


class DTASelectFilterDeserializationUniqueLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Error deserializing UniqueLine: '{self.line}'"


@dataclass
class PeptideLine(Line):
    """
    Class keeping track of Unique lines.

    Example L line:
        Unique	FileName	XCorr	DeltCN	Conf%	M+H+	CalcM+H+	PPM	TotalIntensity	SpR	Prob Score	pI	IonProportion	Redundancy	Sequence
        *	190806_300ng_180m_03_Slot2-3_1_646_nopd.357198.357198.2	6.4774	0.8641	100.0	1868.9581	1868.9752	-9.1	422160.0	0	63.016	8.64	95.7	9	R.YVASYLLAALGGNSSPSAK.D

    """

    __slots__ = ['is_unique', 'file_name', 'low_scan', 'high_scan', 'charge', 'x_corr', 'delta_cn',
                 'Conf', 'mass_plus_hydrogen', 'calc_mass_plus_hydrogen', 'ppm', 'total_intensity', 'spr', 'pi',
                 'ion_proportion', 'redundancy', 'sequence']

    is_unique: bool
    file_name: str
    low_scan: int
    high_scan: int
    charge: int
    x_corr: float
    delta_cn: float
    conf: float
    mass_plus_hydrogen: float
    calc_mass_plus_hydrogen: float
    ppm: float
    prob_score: Union[float, None]
    total_intensity: float
    spr: int
    pi: float
    ion_proportion: float
    redundancy: int
    sequence: str

    X_CORR_PRECISION: ClassVar[int] = 4
    DELTA_CN_PRECISION: ClassVar[int] = 4
    CONF_PRECISION: ClassVar[int] = 1
    MASS_PLUS_HYDROGEN_PRECISION: ClassVar[int] = 4
    CALC_MASS_PLUS_HYDROGEN_PRECISION: ClassVar[int] = 4
    PPM_PRECISION: ClassVar[int] = 1
    TOTAL_INTENSITY_PRECISION: ClassVar[int] = 1
    PI_PRECISION: ClassVar[int] = 3
    PROB_SCORE_PRECISION: ClassVar[int] = 6
    ION_PROPORTION_PRECISION: ClassVar[int] = 2

    @staticmethod
    def deserialize(line: str, version="v2.1.13") -> 'PeptideLine':
        line_elements = line.rstrip().split("\t")
        if version == "v2.1.12":
            if len(line_elements) != len(_PeptideLineColumns_v1_2_12):
                raise DTASelectFilterDeserializationUniqueLineException(line)
            # v2_1_12
            is_unique = line_elements[_PeptideLineColumns_v1_2_12.is_unique.value] == "*"
            file_name = str(line_elements[_PeptideLineColumns_v1_2_12.file_name.value].split(".")[0])
            low_scan = int(line_elements[_PeptideLineColumns_v1_2_12.file_name.value].split(".")[1])
            high_scan = int(line_elements[_PeptideLineColumns_v1_2_12.file_name.value].split(".")[2])
            charge = int(line_elements[_PeptideLineColumns_v1_2_12.file_name.value].split(".")[3])
            x_corr = float(line_elements[_PeptideLineColumns_v1_2_12.x_corr.value])
            delta_cn = float(line_elements[_PeptideLineColumns_v1_2_12.delta_cn.value])
            conf = float(line_elements[_PeptideLineColumns_v1_2_12.conf.value])
            mass_plus_hydrogen = float(line_elements[_PeptideLineColumns_v1_2_12.mass_plus_hydrogen.value])
            calc_mass_plus_hydrogen = float(line_elements[_PeptideLineColumns_v1_2_12.calc_mass_plus_hydrogen.value])
            ppm = (mass_plus_hydrogen - calc_mass_plus_hydrogen) / calc_mass_plus_hydrogen * 1_000_000
            total_intensity = float(line_elements[_PeptideLineColumns_v1_2_12.total_intensity.value])
            spr = int(line_elements[_PeptideLineColumns_v1_2_12.spr.value])
            pi = None
            prob_score = float(line_elements[_PeptideLineColumns_v1_2_12.prob_score.value])
            ion_proportion = float(line_elements[_PeptideLineColumns_v1_2_12.ion_proportion.value])
            redundancy = int(line_elements[_PeptideLineColumns_v1_2_12.redundancy.value])
            sequence = str(line_elements[_PeptideLineColumns_v1_2_12.sequence.value])

        elif version == "v2.1.13":

            if len(line_elements) != len(_PeptideLineColumns_v1_2_13):
                raise DTASelectFilterDeserializationUniqueLineException(line)

            # v2_1_13
            is_unique = line_elements[_PeptideLineColumns_v1_2_13.is_unique.value] == "*"
            file_name = str(line_elements[_PeptideLineColumns_v1_2_13.file_name.value].split(".")[0])
            low_scan = int(line_elements[_PeptideLineColumns_v1_2_13.file_name.value].split(".")[1])
            high_scan = int(line_elements[_PeptideLineColumns_v1_2_13.file_name.value].split(".")[2])
            charge = int(line_elements[_PeptideLineColumns_v1_2_13.file_name.value].split(".")[3])
            x_corr = float(line_elements[_PeptideLineColumns_v1_2_13.x_corr.value])
            delta_cn = float(line_elements[_PeptideLineColumns_v1_2_13.delta_cn.value])
            conf = float(line_elements[_PeptideLineColumns_v1_2_13.conf.value])
            mass_plus_hydrogen = float(line_elements[_PeptideLineColumns_v1_2_13.mass_plus_hydrogen.value])
            calc_mass_plus_hydrogen = float(line_elements[_PeptideLineColumns_v1_2_13.calc_mass_plus_hydrogen.value])
            ppm = float(line_elements[_PeptideLineColumns_v1_2_13.ppm.value])
            total_intensity = float(line_elements[_PeptideLineColumns_v1_2_13.total_intensity.value])
            spr = int(line_elements[_PeptideLineColumns_v1_2_13.spr.value])
            pi = float(line_elements[_PeptideLineColumns_v1_2_13.pi.value])
            prob_score = None
            ion_proportion = float(line_elements[_PeptideLineColumns_v1_2_13.ion_proportion.value])
            redundancy = int(line_elements[_PeptideLineColumns_v1_2_13.redundancy.value])
            sequence = str(line_elements[_PeptideLineColumns_v1_2_13.sequence.value])
        else:
            raise NotImplementedError

        line = PeptideLine(is_unique=is_unique,
                           file_name=file_name,
                           low_scan=low_scan,
                           high_scan=high_scan,
                           charge=charge,
                           x_corr=x_corr,
                           delta_cn=delta_cn,
                           conf=conf,
                           mass_plus_hydrogen=mass_plus_hydrogen,
                           calc_mass_plus_hydrogen=calc_mass_plus_hydrogen,
                           ppm=ppm,
                           prob_score=prob_score,
                           total_intensity=total_intensity,
                           spr=spr,
                           pi=pi,
                           ion_proportion=ion_proportion,
                           redundancy=redundancy,
                           sequence=sequence
                           )

        return line

    def serialize(self, version="v2.1.13") -> str:
        if version == "v2.1.12":
            file_line = '.'.join(
                [self.file_name, f"{self.low_scan}", f"{self.high_scan}", f"{self.charge}"])
            is_unique_symbol = '*' if self.is_unique else ''

            line_elements = [
                is_unique_symbol,
                file_line,
                f"{self.x_corr:.{PeptideLine.X_CORR_PRECISION}f}",
                f"{self.delta_cn:.{PeptideLine.DELTA_CN_PRECISION}f}",
                f"{self.Conf:.{PeptideLine.CONF_PRECISION}f}",
                f"{self.mass_plus_hydrogen:.{PeptideLine.MASS_PLUS_HYDROGEN_PRECISION}f}",
                f"{self.calc_mass_plus_hydrogen:.{PeptideLine.CALC_MASS_PLUS_HYDROGEN_PRECISION}f}",
                f"{self.total_intensity:.{PeptideLine.TOTAL_INTENSITY_PRECISION}f}",
                f"{self.spr}",
                f"{self.prob_score:.{PeptideLine.PROB_SCORE_PRECISION}f}",
                f"{self.ion_proportion:.{PeptideLine.ION_PROPORTION_PRECISION}f}",
                f"{self.redundancy}",
                self.sequence
            ]
            line_elements = [str(elem) for elem in line_elements]
            return '\t'.join(line_elements) + '\n'
        elif version == "v2.1.13":
            file_line = '.'.join(
                [self.file_name, f"{self.low_scan}", f"{self.high_scan}", f"{self.charge}"])
            is_unique_symbol = '*' if self.is_unique else ''

            line_elements = [
                is_unique_symbol,
                file_line,
                f"{self.x_corr:.{PeptideLine.X_CORR_PRECISION}f}",
                f"{self.delta_cn:.{PeptideLine.DELTA_CN_PRECISION}f}",
                f"{self.Conf:.{PeptideLine.CONF_PRECISION}f}",
                f"{self.mass_plus_hydrogen:.{PeptideLine.MASS_PLUS_HYDROGEN_PRECISION}f}",
                f"{self.calc_mass_plus_hydrogen:.{PeptideLine.CALC_MASS_PLUS_HYDROGEN_PRECISION}f}",
                f"{self.ppm:.{PeptideLine.PPM_PRECISION}f}",
                f"{self.total_intensity:.{PeptideLine.TOTAL_INTENSITY_PRECISION}f}",
                f"{self.spr}",
                f"{self.pi:.{PeptideLine.PI_PRECISION}f}",
                f"{self.ion_proportion:.{PeptideLine.ION_PROPORTION_PRECISION}f}",
                f"{self.redundancy}",
                self.sequence
            ]
            line_elements = [str(elem) for elem in line_elements]
            return '\t'.join(line_elements) + '\n'
        else:
            raise NotImplementedError


class _ProteinLineColumns(Enum):
    """
    Enum class to represent PasefFrameMsMsInfo table column numbers
    """
    locus_name = 0
    sequence_count = 1
    spectrum_count = 2
    sequence_coverage = 3
    length = 4
    molWt = 5
    pi = 6
    validation_status = 7
    nsaf = 8
    empai = 9
    description_name = 10


class DTASelectFilterDeserializationLocusLineException(Exception):

    def __init__(self, _line: str):
        self.line = _line

    def __repr__(self):
        return f"Error deserializing UniqueLine: '{self.line}'"


@dataclass
class ProteinLine(Line):
    """
    Class keeping track of sqt Locus lines.

    Example L line:
        Locus	Sequence Count	Spectrum Count	Sequence Coverage	Length	MolWt	pI	Validation Status	NSAF	EMPAI	Descriptive Name
        sp|P05387|RLA2_HUMAN	9	62	84.3%	115	11665	4.5	U	0.0025080831	5.966266	60S acidic ribosomal protein P2 OS=Homo sapiens OX=9606 GN=RPLP2 PE=1 SV=1
    """
    __slots__ = ['locus_name', 'sequence_count', 'spectrum_count', 'sequence_coverage', 'length', 'molWt', 'pi',
                 'validation_status', 'nsaf', 'empai', 'description_name']

    locus_name: str
    sequence_count: int
    spectrum_count: int
    sequence_coverage: float
    length: int
    molWt: int
    pi: float
    validation_status: str
    nsaf: float
    empai: float
    description_name: str

    SEQUENCE_COVERAGE_PRECISION: ClassVar[int] = 1
    PI_PRECISION: ClassVar[int] = 1
    NSAF_PRECISION: ClassVar[int] = 10
    EMPAI_PRECISION: ClassVar[int] = 6

    @staticmethod
    def deserialize(line: str, version="v2.1.13") -> 'ProteinLine':
        line_elements = line.rstrip().split("\t")

        if len(line_elements) != len(_ProteinLineColumns):
            raise DTASelectFilterDeserializationLocusLineException(line)

        locus_name = line_elements[_ProteinLineColumns.locus_name.value]
        sequence_count = int(line_elements[_ProteinLineColumns.sequence_count.value])
        spectrum_count = int(line_elements[_ProteinLineColumns.spectrum_count.value])
        sequence_coverage = float(line_elements[_ProteinLineColumns.sequence_coverage.value][:-1])  # remove % sign
        length = int(line_elements[_ProteinLineColumns.length.value])
        molWt = int(line_elements[_ProteinLineColumns.molWt.value])
        pi = float(line_elements[_ProteinLineColumns.pi.value])
        validation_status = str(line_elements[_ProteinLineColumns.validation_status.value])
        nsaf = float(line_elements[_ProteinLineColumns.nsaf.value])
        empai = float(line_elements[_ProteinLineColumns.empai.value])
        description_name = str(line_elements[_ProteinLineColumns.description_name.value])

        line = ProteinLine(locus_name=locus_name,
                           sequence_count=sequence_count,
                           spectrum_count=spectrum_count,
                           sequence_coverage=sequence_coverage,
                           length=length,
                           molWt=molWt,
                           pi=pi,
                           validation_status=validation_status,
                           nsaf=nsaf,
                           empai=empai,
                           description_name=description_name
                           )
        return line

    def serialize(self, version="v2.1.13") -> str:
        line_elements = [None] * len(_ProteinLineColumns)
        line_elements[_ProteinLineColumns.locus_name.value] = self.locus_name
        line_elements[_ProteinLineColumns.sequence_count.value] = f"{self.sequence_count}"
        line_elements[_ProteinLineColumns.spectrum_count.value] = f"{self.spectrum_count}"
        line_elements[_ProteinLineColumns.sequence_coverage.value] = \
            f"{self.sequence_coverage:.{ProteinLine.SEQUENCE_COVERAGE_PRECISION}f}%"
        line_elements[_ProteinLineColumns.length.value] = f"{self.length}"
        line_elements[_ProteinLineColumns.molWt.value] = f"{self.molWt}"
        line_elements[_ProteinLineColumns.pi.value] = f"{self.pi:.{ProteinLine.PI_PRECISION}f}"
        line_elements[_ProteinLineColumns.validation_status.value] = self.validation_status
        line_elements[_ProteinLineColumns.nsaf.value] = f"{self.nsaf:.{ProteinLine.NSAF_PRECISION}f}"
        line_elements[_ProteinLineColumns.empai.value] = f"{self.empai:.{ProteinLine.EMPAI_PRECISION}f}"
        line_elements[_ProteinLineColumns.description_name.value] = self.description_name

        line_elements = [str(elem) for elem in line_elements]
        return '\t'.join(line_elements) + '\n'


@dataclass
class DTAFilterResult:
    protein_line: ProteinLine
    peptide_lines: List[PeptideLine]

    def serialize(self) -> str:
        lines = [self.protein_line] + self.peptide_lines
        return ''.join([line.serialize() for line in lines])
