from dataclasses import dataclass, field
from typing import List, ClassVar, Union

from . import exceptions as sqt_exceptions
from .columns import LLineColumns, MLineColumns, MLineColumns_v2_1_0, MLineColumns_v2_1_0_ext, SLineColumns, \
    SLineColumns_v2_1_0, SLineColumns_v2_1_0_ext
from ..util import HLine

@dataclass
class LLine:
    """
    Class keeping track of sqt L lines.

    Example L line:
        L [locus name] [peptide index in protein sequence] [peptide sequence]
        #L	sp|Q9C0C9|UBE2O_HUMAN	223	ILK.LSNGARCSMNTEDGAKLYDVCPHVSDSGLFFDDSY(79.966331)GFY(79.966331)PGQVLIGPAK.IFS
    """

    LETTER = "L"

    locus_name: str
    peptide_index_in_protein_sequence: int
    peptide_sequence: str

    @staticmethod
    def deserialize(line: str, version='auto') -> 'LLine':
        line_elements = line.rstrip().split("\t")
        columns = LLineColumns
        if len(line_elements) < len(columns):
            raise sqt_exceptions.SqtFileDeserializationLLineException(_line=line)

        locus_name = LLine._deserialize_locus_name(line_elements[columns.locus_name.value])
        peptide_index_in_protein_sequence = LLine._deserialize_peptide_index_in_protein_sequence(
            line_elements[columns.peptide_index_in_protein_sequence.value])
        peptide_sequence = LLine._deserialize_peptide_sequence(line_elements[columns.peptide_sequence.value])

        l_line = LLine(locus_name, peptide_index_in_protein_sequence, peptide_sequence)
        return l_line

    @staticmethod
    def _deserialize_locus_name(val: str) -> str:
        return val

    @staticmethod
    def _deserialize_peptide_index_in_protein_sequence(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_peptide_sequence(val: str) -> str:
        return val

    def serialize(self, version='auto') -> str:
        columns = LLineColumns
        line_elements = [""] * len(columns)
        line_elements[columns.letter.value] = LLine.LETTER
        line_elements[columns.locus_name.value] = self._serialize_locus_name()
        line_elements[columns.peptide_index_in_protein_sequence.value] = \
            self._serialize_peptide_index_in_protein_sequence()
        line_elements[columns.peptide_sequence.value] = self._serialize_peptide_sequence()

        return '\t'.join(line_elements) + '\n'

    def _serialize_locus_name(self) -> str:
        return self.locus_name

    def _serialize_peptide_index_in_protein_sequence(self) -> str:
        return f"{self.peptide_index_in_protein_sequence}"

    def _serialize_peptide_sequence(self) -> str:
        return self.peptide_sequence


@dataclass
class MLine:
    """
    Class keeping track of sqt M lines.

    Example M line:
        M [rank by Xcorr] [rank by Sp] [calculated mass]
        [DeltaCN] [Xcorr] [Sp] [matched ions] [expected ions] [sequence matched]
        [validation status U = unknown, Y = yes, N = no, M = Maybe] [predicted 1/k0]
        #M	6	0	5415.35096	0.0000	0.0000	0.000	1	159	K.LSNGARCSMNTEDGGFY(79.966331)PGQVLIGPAK.I	U	NA	NA
    """
    LETTER = "M"

    xcorr_rank: int
    sp_rank: int
    calculated_mass: float
    delta_cn: float
    xcorr: float
    sp: float
    matched_ions: int
    expected_ions: int
    sequence: str
    validation_status: str
    predicted_ook0: float
    tims_score: float
    tims_b_score_m2: float
    tims_b_score_best_m: float

    l_lines: List[LLine] = field(default_factory=list)

    PREDICTED_OOK0_PRECISION: ClassVar[int] = 4
    TIMS_SCORE_PRECISION: ClassVar[int] = 4
    XCORR_PRECISION: ClassVar[int] = 4
    TIMS_B_SCORE_M2_PRECISION: ClassVar[int] = 4
    TIMS_B_SCORE_BEST_M_PRECISION: ClassVar[int] = 4
    CALCULATED_MASS_PRECISION: ClassVar[int] = 5
    DELTA_CN_PRECISION: ClassVar[int] = 4
    SP_PRECISION: ClassVar[int] = 5

    @staticmethod
    def guess_version(line: str):
        line_elements = line.rstrip().split("\t")
        if len(line_elements) == len(MLineColumns):
            return "v1.4"
        elif len(line_elements) == len(MLineColumns_v2_1_0):
            return "v2.1.0"
        elif len(line_elements) == len(MLineColumns_v2_1_0_ext):
            return "v2.1.0_ext"
        else:
            raise None

    @staticmethod
    def deserialize(line: str, version="auto") -> 'MLine':

        if version == "auto":
            version = MLine.guess_version(line)

        line_elements = line.rstrip().split("\t")
        if version == "v1.4":

            columns = MLineColumns
            if len(line_elements) != len(columns):
                raise sqt_exceptions.SqtFileDeserializationMLineException(_line=line)

            xcorr_rank = MLine._deserialize_xcorr_rank(line_elements[columns.xcorr_rank.value])
            sp_rank = MLine._deserialize_sp_rank(line_elements[columns.sp_rank.value])
            calculated_mass = MLine._deserialize_calculated_mass(line_elements[columns.calculated_mass.value])
            delta_cn = MLine._deserialize_delta_cn(line_elements[columns.delta_cn.value])
            xcorr = MLine._deserialize_xcorr(line_elements[columns.xcorr.value])
            sp = MLine._deserialize_sp(line_elements[columns.sp.value])
            matched_ions = MLine._deserialize_matched_ions(line_elements[columns.matched_ions.value])
            expected_ions = MLine._deserialize_expected_ions(line_elements[columns.expected_ions.value])
            sequence = MLine._deserialize_sequence(line_elements[columns.sequence.value])
            validation_status = MLine._deserialize_validation_status(line_elements[columns.validation_status.value])
            predicted_ook0 = None
            tims_score = None
            tims_b_score_m2 = None
            tims_b_score_best_m = None

        elif version == "v2.1.0":

            columns = MLineColumns_v2_1_0
            if len(line_elements) != len(columns):
                raise sqt_exceptions.SqtFileDeserializationMLineException(_line=line)

            xcorr_rank = MLine._deserialize_xcorr_rank(line_elements[columns.xcorr_rank.value])
            sp_rank = MLine._deserialize_sp_rank(line_elements[columns.sp_rank.value])
            calculated_mass = MLine._deserialize_calculated_mass(line_elements[columns.calculated_mass.value])
            delta_cn = MLine._deserialize_delta_cn(line_elements[columns.delta_cn.value])
            xcorr = MLine._deserialize_xcorr(line_elements[columns.xcorr.value])
            sp = MLine._deserialize_sp(line_elements[columns.sp.value])
            matched_ions = MLine._deserialize_matched_ions(line_elements[columns.matched_ions.value])
            expected_ions = MLine._deserialize_expected_ions(line_elements[columns.expected_ions.value])
            sequence = MLine._deserialize_sequence(line_elements[columns.sequence.value])
            validation_status = MLine._deserialize_validation_status(line_elements[columns.validation_status.value])
            predicted_ook0 = MLine._deserialize_predicted_ook0(line_elements[columns.predicted_ook0.value])
            tims_score = MLine._deserialize_tims_score(line_elements[columns.tims_score.value])
            tims_b_score_m2 = None
            tims_b_score_best_m = None

        elif version == "v2.1.0_ext":

            columns = MLineColumns_v2_1_0_ext
            if len(line_elements) != len(columns):
                raise sqt_exceptions.SqtFileDeserializationMLineException(_line=line)

            xcorr_rank = MLine._deserialize_xcorr_rank(line_elements[columns.xcorr_rank.value])
            sp_rank = MLine._deserialize_sp_rank(line_elements[columns.sp_rank.value])
            calculated_mass = MLine._deserialize_calculated_mass(line_elements[columns.calculated_mass.value])
            delta_cn = MLine._deserialize_delta_cn(line_elements[columns.delta_cn.value])
            xcorr = MLine._deserialize_xcorr(line_elements[columns.xcorr.value])
            sp = MLine._deserialize_sp(line_elements[columns.sp.value])
            matched_ions = MLine._deserialize_matched_ions(line_elements[columns.matched_ions.value])
            expected_ions = MLine._deserialize_expected_ions(line_elements[columns.expected_ions.value])
            sequence = MLine._deserialize_sequence(line_elements[columns.sequence.value])
            validation_status = MLine._deserialize_validation_status(line_elements[columns.validation_status.value])
            predicted_ook0 = MLine._deserialize_predicted_ook0(line_elements[columns.predicted_ook0.value])
            tims_score = MLine._deserialize_tims_score(line_elements[columns.tims_score.value])
            tims_b_score_m2 = MLine._deserialize_tims_b_score_m2(line_elements[columns.tims_b_score_m2.value])
            tims_b_score_best_m = \
                MLine._deserialize_tims_b_score_best_m(line_elements[columns.tims_b_score_best_m.value])
        else:
            raise NotImplementedError

        m_line = MLine(xcorr_rank=xcorr_rank,
                       sp_rank=sp_rank,
                       calculated_mass=calculated_mass,
                       delta_cn=delta_cn,
                       xcorr=xcorr,
                       sp=sp,
                       matched_ions=matched_ions,
                       expected_ions=expected_ions,
                       sequence=sequence,
                       validation_status=validation_status,
                       predicted_ook0=predicted_ook0,
                       tims_score=tims_score,
                       tims_b_score_m2=tims_b_score_m2,
                       tims_b_score_best_m=tims_b_score_best_m)
        return m_line

    @staticmethod
    def _deserialize_xcorr_rank(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_sp_rank(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_calculated_mass(val: str) -> float:
        return float(val)

    @staticmethod
    def _deserialize_delta_cn(val: str) -> float:
        return float(val)

    @staticmethod
    def _deserialize_xcorr(val: str) -> float:
        return float(val)

    @staticmethod
    def _deserialize_sp(val: str) -> float:
        return float(val)

    @staticmethod
    def _deserialize_matched_ions(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_expected_ions(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_sequence(val: str) -> str:
        return val

    @staticmethod
    def _deserialize_validation_status(val: str) -> str:
        return val

    @staticmethod
    def _deserialize_predicted_ook0(val: str) -> float:
        return None if val == "NA" else float(val)

    @staticmethod
    def _deserialize_tims_score(val: str) -> float:
        return None if val == "NA" else float(val)

    @staticmethod
    def _deserialize_tims_b_score_m2(val: str) -> float:
        return None if val == "NA" else float(val)

    @staticmethod
    def _deserialize_tims_b_score_best_m(val: str) -> float:
        return None if val == "NA" else float(val)

    def serialize(self, version="auto") -> str:

        if version == "auto":
            raise NotImplementedError

        if version == "v1.4":

            columns = MLineColumns
            line_elements = [""]*len(columns)
            line_elements[columns.letter.value] = MLine.LETTER
            line_elements[columns.xcorr_rank.value] = self._serialize_xcorr_rank()
            line_elements[columns.sp_rank.value] = self._serialize_sp_rank()
            line_elements[columns.calculated_mass.value] = self._serialize_calculated_mass()
            line_elements[columns.delta_cn.value] = self._serialize_delta_cn()
            line_elements[columns.xcorr.value] = self._serialize_xcorr()
            line_elements[columns.sp.value] = self._serialize_sp()
            line_elements[columns.matched_ions.value] = self._serialize_matched_ions()
            line_elements[columns.expected_ions.value] = self._serialize_expected_ions()
            line_elements[columns.sequence.value] = self._serialize_sequence()
            line_elements[columns.validation_status.value] = self._serialize_validation_status()

        elif version == "v2.1.0":

            columns = MLineColumns_v2_1_0
            line_elements = [""] * len(columns)
            line_elements[columns.letter.value] = MLine.LETTER
            line_elements[columns.xcorr_rank.value] = self._serialize_xcorr_rank()
            line_elements[columns.sp_rank.value] = self._serialize_sp_rank()
            line_elements[columns.calculated_mass.value] = self._serialize_calculated_mass()
            line_elements[columns.delta_cn.value] = self._serialize_delta_cn()
            line_elements[columns.xcorr.value] = self._serialize_xcorr()
            line_elements[columns.sp.value] = self._serialize_sp()
            line_elements[columns.matched_ions.value] = self._serialize_matched_ions()
            line_elements[columns.expected_ions.value] = self._serialize_expected_ions()
            line_elements[columns.sequence.value] = self._serialize_sequence()
            line_elements[columns.validation_status.value] = self._serialize_validation_status()
            line_elements[columns.predicted_ook0.value] = self._serialize_predicted_ook0()
            line_elements[columns.tims_score.value] = self._serialize_tims_score()

        elif version == "v2.1.0_ext":

            columns = MLineColumns_v2_1_0_ext
            line_elements = [""] * len(columns)
            line_elements[columns.letter.value] = MLine.LETTER
            line_elements[columns.xcorr_rank.value] = self._serialize_xcorr_rank()
            line_elements[columns.sp_rank.value] = self._serialize_sp_rank()
            line_elements[columns.calculated_mass.value] = self._serialize_calculated_mass()
            line_elements[columns.delta_cn.value] = self._serialize_delta_cn()
            line_elements[columns.xcorr.value] = self._serialize_xcorr()
            line_elements[columns.sp.value] = self._serialize_sp()
            line_elements[columns.matched_ions.value] = self._serialize_matched_ions()
            line_elements[columns.expected_ions.value] = self._serialize_expected_ions()
            line_elements[columns.sequence.value] = self._serialize_sequence()
            line_elements[columns.validation_status.value] = self._serialize_validation_status()
            line_elements[columns.predicted_ook0.value] = self._serialize_predicted_ook0()
            line_elements[columns.tims_score.value] = self._serialize_tims_score()
            line_elements[columns.tims_b_score_m2.value] = self._serialize_tims_b_score_m2()
            line_elements[columns.tims_b_score_best_m.value] = self._serialize_tims_b_score_best_m()

        else:
            raise NotImplementedError

        return '\t'.join(line_elements) + '\n'

    def _serialize_xcorr_rank(self) -> str:
        return f"{self.xcorr_rank}"

    def _serialize_sp_rank(self) -> str:
        return f"{self.sp_rank}"

    def _serialize_calculated_mass(self) -> str:
        return f"{self.calculated_mass:.{MLine.CALCULATED_MASS_PRECISION}f}"

    def _serialize_delta_cn(self) -> str:
        return f"{self.delta_cn:.{MLine.DELTA_CN_PRECISION}f}"

    def _serialize_xcorr(self) -> str:
        return f"{self.xcorr:.{MLine.XCORR_PRECISION}f}"

    def _serialize_sp(self) -> str:
        return f"{self.sp:.{MLine.SP_PRECISION}f}"

    def _serialize_matched_ions(self) -> str:
        return f"{self.matched_ions}"

    def _serialize_expected_ions(self) -> str:
        return f"{self.expected_ions}"

    def _serialize_sequence(self) -> str:
        return self.sequence

    def _serialize_validation_status(self) -> str:
        return self.validation_status

    def _serialize_predicted_ook0(self) -> str:
        if self.predicted_ook0 is None:
            return "NA"
        return f"{self.predicted_ook0:.{MLine.PREDICTED_OOK0_PRECISION}f}"

    def _serialize_tims_score(self) -> str:
        if self.tims_score is None:
            return "NA"
        return str(round(self.tims_score, MLine.TIMS_SCORE_PRECISION))

    def _serialize_tims_b_score_m2(self) -> str:
        if self.tims_b_score_m2 is None:
            return "NA"
        return str(round(self.tims_b_score_m2, MLine.TIMS_B_SCORE_M2_PRECISION))

    def _serialize_tims_b_score_best_m(self) -> str:
        if self.tims_b_score_best_m is None:
            return "NA"
        return str(round(self.tims_b_score_best_m, MLine.TIMS_B_SCORE_BEST_M_PRECISION))

    def get_clean_seq(self) -> str:
        return self.sequence[2:-2]

    def is_reverse(self) -> bool:
        for l_line in self.l_lines:
            if "Reverse" not in l_line.locus_name:
                return False
        return True


@dataclass
class SLine:
    """
    Class keeping track of sqt S lines.

    Example S_line:
        S [low scan] [high scan] [charge] [process time] [server] [experimental mass] [total ion intensity]
        [lowest Sp] [# of seq. matched] [experimental 1/k0]
        #S	83131	83131	5	34	paserbox_Thread-71766	5417.09229	353.00	0.0016	0	1.2735202
    """

    LETTER = 'S'

    low_scan: int
    high_scan: int
    charge: int
    process_time: int
    server: str
    experimental_mass: float
    total_ion_intensity: float
    lowest_sp: Union[float, None]
    number_matches: int
    experimental_ook0: Union[float, None]
    experimental_mz: Union[float, None]
    corrected_ook0: Union[float, None]

    m_lines: List[MLine] = field(default_factory=list)

    EXPERIMENTAL_MALL_PRECISION: ClassVar[int] = 5
    TOTAL_ION_INTENSITY_PRECISION: ClassVar[int] = 2
    LOWEST_SP_PRECISION: ClassVar[int] = 4
    EXPERIMENTAL_OOK0_PRECISION: ClassVar[int] = 4
    EXPERIMENTAL_MASS_PRECISION: ClassVar[int] = 4
    CORRECTED_OOK0_PRECISION: ClassVar[int] = 4

    @staticmethod
    def guess_version(line: str):
        line_elements = line.rstrip().split("\t")
        if len(line_elements) == len(SLineColumns):
            return "v1.4"
        elif len(line_elements) == len(SLineColumns_v2_1_0):
            return "v2.1.0"
        elif len(line_elements) == len(SLineColumns_v2_1_0_ext):
            return "v2.1.0_ext"
        else:
            return None

    @staticmethod
    def deserialize(line: str, version="auto") -> 'SLine':

        if version == "auto":
            version = SLine.guess_version(line)

        line_elements = line.rstrip().split("\t")
        if version == "v1.4":

            columns = SLineColumns
            if len(line_elements) != len(columns):
                raise sqt_exceptions.SqtFileDeserializationSLineException(_line=line)

            low_scan = SLine._deserialize_low_scan(line_elements[columns.low_scan.value])
            high_scan = SLine._deserialize_high_scan(line_elements[columns.high_scan.value])
            charge = SLine._deserialize_charge(line_elements[columns.charge.value])
            process_time = SLine._deserialize_process_time(line_elements[columns.process_time.value])
            server = SLine._deserialize_server(line_elements[columns.server.value])
            experimental_mass = SLine._deserialize_experimental_mass(line_elements[columns.experimental_mass.value])
            total_ion_intensity = \
                SLine._deserialize_total_ion_intensity(line_elements[columns.total_ion_intensity.value])
            lowest_sp = SLine._deserialize_lowest_sp(line_elements[columns.lowest_sp.value])
            number_matches = SLine._deserialize_number_matches(line_elements[columns.number_matches.value])
            experimental_ook0 = None
            experimental_mz = None
            corrected_ook0 = None

        elif version == "v2.1.0":

            columns = SLineColumns_v2_1_0
            if len(line_elements) != len(columns):
                raise sqt_exceptions.SqtFileDeserializationSLineException(_line=line)

            low_scan = SLine._deserialize_low_scan(line_elements[columns.low_scan.value])
            high_scan = SLine._deserialize_high_scan(line_elements[columns.high_scan.value])
            charge = SLine._deserialize_charge(line_elements[columns.charge.value])
            process_time = SLine._deserialize_process_time(line_elements[columns.process_time.value])
            server = SLine._deserialize_server(line_elements[columns.server.value])
            experimental_mass = SLine._deserialize_experimental_mass(line_elements[columns.experimental_mass.value])
            total_ion_intensity = \
                SLine._deserialize_total_ion_intensity(line_elements[columns.total_ion_intensity.value])
            lowest_sp = SLine._deserialize_lowest_sp(line_elements[columns.lowest_sp.value])
            number_matches = SLine._deserialize_number_matches(line_elements[columns.number_matches.value])
            experimental_ook0 = SLine._deserialize_experimental_ook0(line_elements[columns.experimental_ook0.value])
            experimental_mz = None
            corrected_ook0 = None

        elif version == "v2.1.0_ext":

            columns = SLineColumns_v2_1_0_ext
            if len(line_elements) != len(columns):
                raise sqt_exceptions.SqtFileDeserializationSLineException(_line=line)

            low_scan = SLine._deserialize_low_scan(line_elements[columns.low_scan.value])
            high_scan = SLine._deserialize_high_scan(line_elements[columns.high_scan.value])
            charge = SLine._deserialize_charge(line_elements[columns.charge.value])
            process_time = SLine._deserialize_process_time(line_elements[columns.process_time.value])
            server = SLine._deserialize_server(line_elements[columns.server.value])
            experimental_mass = SLine._deserialize_experimental_mass(line_elements[columns.experimental_mass.value])
            total_ion_intensity = \
                SLine._deserialize_total_ion_intensity(line_elements[columns.total_ion_intensity.value])
            lowest_sp = SLine._deserialize_lowest_sp(line_elements[columns.lowest_sp.value])
            number_matches = SLine._deserialize_number_matches(line_elements[columns.number_matches.value])
            experimental_ook0 = SLine._deserialize_experimental_ook0(line_elements[columns.experimental_ook0.value])
            experimental_mz = SLine._deserialize_experimental_mz(line_elements[columns.experimental_mz.value])
            corrected_ook0 = SLine._deserialize_corrected_ook0(line_elements[columns.corrected_ook0.value])

        else:
            raise NotImplementedError

        s_line = SLine(low_scan=low_scan,
                       high_scan=high_scan,
                       charge=charge,
                       process_time=process_time,
                       server=server,
                       experimental_mass=experimental_mass,
                       total_ion_intensity=total_ion_intensity,
                       lowest_sp=lowest_sp,
                       number_matches=number_matches,
                       experimental_ook0=experimental_ook0,
                       experimental_mz=experimental_mz,
                       corrected_ook0=corrected_ook0)
        return s_line

    @staticmethod
    def _deserialize_low_scan(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_high_scan(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_charge(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_process_time(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_server(val: str) -> str:
        return val

    @staticmethod
    def _deserialize_experimental_mass(val: str) -> float:
        return float(val)

    @staticmethod
    def _deserialize_total_ion_intensity(val: str) -> float:
        return float(val)

    @staticmethod
    def _deserialize_lowest_sp(val: str) -> float:
        return None if val == "NA" else float(val)

    @staticmethod
    def _deserialize_number_matches(val: str) -> int:
        return int(val)

    @staticmethod
    def _deserialize_experimental_ook0(val: str) -> Union[float, None]:
        return None if val == "NA" else float(val)

    @staticmethod
    def _deserialize_experimental_mz(val: str) -> Union[float, None]:
        return None if val == "NA" else float(val)

    @staticmethod
    def _deserialize_corrected_ook0(val: str) -> Union[float, None]:
        return None if val == "NA" else float(val)

    def serialize(self, version='auto') -> str:
        if version == "auto":
            raise NotImplementedError

        if version == "v1.4":
            columns = SLineColumns
            line_elements = [""]*len(columns)

            line_elements[columns.letter.value] = SLine.LETTER
            line_elements[columns.low_scan.value] = self._serialize_low_scan()
            line_elements[columns.high_scan.value] = self._serialize_high_scan()
            line_elements[columns.charge.value] = self._serialize_charge()
            line_elements[columns.process_time.value] = self._serialize_process_time()
            line_elements[columns.server.value] = self._serialize_server()
            line_elements[columns.experimental_mass.value] = self._serialize_experimental_mass()
            line_elements[columns.total_ion_intensity.value] = self._serialize_total_ion_intensity()
            line_elements[columns.lowest_sp.value] = self._serialize_lowest_sp()
            line_elements[columns.number_matches.value] = self._serialize_number_matches()

        elif version == "v2.1.0":

            columns = SLineColumns_v2_1_0
            line_elements = [""] * len(columns)

            line_elements[columns.letter.value] = SLine.LETTER
            line_elements[columns.low_scan.value] = self._serialize_low_scan()
            line_elements[columns.high_scan.value] = self._serialize_high_scan()
            line_elements[columns.charge.value] = self._serialize_charge()
            line_elements[columns.process_time.value] = self._serialize_process_time()
            line_elements[columns.server.value] = self._serialize_server()
            line_elements[columns.experimental_mass.value] = self._serialize_experimental_mass()
            line_elements[columns.total_ion_intensity.value] = self._serialize_total_ion_intensity()
            line_elements[columns.lowest_sp.value] = self._serialize_lowest_sp()
            line_elements[columns.number_matches.value] = self._serialize_number_matches()
            line_elements[columns.experimental_ook0.value] = self._serialize_experimental_ook0()

        elif version == "v2.1.0_ext":

            columns = SLineColumns_v2_1_0_ext
            line_elements = [""] * len(columns)
            
            line_elements[columns.letter.value] = SLine.LETTER
            line_elements[columns.low_scan.value] = self._serialize_low_scan()
            line_elements[columns.high_scan.value] = self._serialize_high_scan()
            line_elements[columns.charge.value] = self._serialize_charge()
            line_elements[columns.process_time.value] = self._serialize_process_time()
            line_elements[columns.server.value] = self._serialize_server()
            line_elements[columns.experimental_mass.value] = self._serialize_experimental_mass()
            line_elements[columns.total_ion_intensity.value] = self._serialize_total_ion_intensity()
            line_elements[columns.lowest_sp.value] = self._serialize_lowest_sp()
            line_elements[columns.number_matches.value] = self._serialize_number_matches()
            line_elements[columns.experimental_ook0.value] = self._serialize_experimental_ook0()
            line_elements[columns.experimental_mz.value] = self._serialize_experimental_mz()
            line_elements[columns.corrected_ook0.value] = self._serialize_corrected_ook0()

        else:
            raise NotImplementedError

        return '\t'.join(line_elements) + '\n'

    def _serialize_low_scan(self) -> str:
        return f"{self.low_scan}"

    def _serialize_high_scan(self) -> str:
        return f"{self.high_scan}"

    def _serialize_charge(self) -> str:
        return f"{self.charge}"

    def _serialize_process_time(self) -> str:
        return f"{self.process_time}"

    def _serialize_server(self) -> str:
        return self.server

    def _serialize_experimental_mass(self) -> str:
        return f"{self.experimental_mass:.{SLine.EXPERIMENTAL_MALL_PRECISION}f}"

    def _serialize_total_ion_intensity(self) -> str:
        return f"{self.total_ion_intensity:.{SLine.TOTAL_ION_INTENSITY_PRECISION}f}"

    def _serialize_lowest_sp(self) -> str:
        if self.lowest_sp is None:
            return "NA"
        return f"{self.lowest_sp:.{SLine.LOWEST_SP_PRECISION}f}"

    def _serialize_number_matches(self) -> str:
        return f"{self.number_matches}"

    def _serialize_experimental_ook0(self) -> str:
        if self.experimental_ook0 is None:
            return "NA"
        return f"{self.experimental_ook0:.{SLine.EXPERIMENTAL_OOK0_PRECISION}f}"

    def _serialize_experimental_mz(self) -> str:
        if self.experimental_mass is None:
            return "NA"
        return f"{self.experimental_mass:.{SLine.EXPERIMENTAL_MASS_PRECISION}f}"

    def _serialize_corrected_ook0(self) -> str:
        if self.corrected_ook0 is None:
            return "NA"
        return f"{self.corrected_ook0:.{SLine.CORRECTED_OOK0_PRECISION}f}"


def parse_sqt_line(line: str, version='auto') -> Union[HLine, SLine, MLine, LLine]:
    """
    Returns the appropriate Ms2 Line object or throws error
    """
    if line[0] == HLine.LETTER:
        return HLine.deserialize(line, version=version)
    elif line[0] == SLine.LETTER:
        return SLine.deserialize(line, version=version)
    elif line[0] == MLine.LETTER:
        return MLine.deserialize(line, version=version)
    elif line[0] == LLine.LETTER:
        return LLine.deserialize(line, version=version)
    else:
        raise sqt_exceptions.SqtFileDeserializationUnsupportedLineException
