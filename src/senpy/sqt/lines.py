from dataclasses import dataclass, field
from typing import List

from senpy.util import Line


@dataclass
class LLine(Line):
    """
    Class keeping track of sqt L lines.

    Example L line:
        L [locus name] [peptide index in protein sequence] [peptide sequence]
        #L	sp|Q9C0C9|UBE2O_HUMAN	223	ILK.LSNGARCSMNTEDGAKLYDVCPHVSDSGLFFDDSY(79.966331)GFY(79.966331)PGQVLIGPAK.IFS
    """

    locus_name: str
    peptide_index_in_protein_sequence: int
    peptide_sequence: str



@dataclass
class MLine(Line):
    """
    Class keeping track of sqt M lines.

    Example M line:
        M [rank by Xcorr] [rank by Sp] [calculated mass]
        [DeltaCN] [Xcorr] [Sp] [matched ions] [expected ions] [sequence matched]
        [validation status U = unknown, Y = yes, N = no, M = Maybe] [predicted 1/k0]
        #M	6	0	5415.35096	0.0000	0.0000	0.000	1	159	K.LSNGARCSMNTEDGGFY(79.966331)PGQVLIGPAK.I	U	NA	NA
    """

    xcorr_rank: int
    sp_rank: int
    calculated_mass: float
    DeltaCN: float
    xcorr: float
    sp: int
    matched_ions: int
    expected_ions: int
    sequence: str
    validation_status: str
    predicted_ook0: float
    tims_score: float
    tims_b_score_m2: float = None
    tims_b_score_best_m: float = None

    l_lines: List[LLine] = field(default_factory=list)

    def get_clean_seq(self) -> str:
        return self.sequence[2:-2]

    def is_reverse(self) -> bool:
        for l_line in self.l_lines:
            if "Reverse" not in l_line.locus_name:
                return False
        return True

    def __eq__(self, other):
        if not isinstance(other, MLine):
            return False
        else:
            return self.xcorr_rank == other.xcorr_rank and self.xcorr == other.xcorr and \
                   self.sp_rank == other.sp_rank and self.sp == other.sp and \
                   self.calculated_mass == other.calculated_mass and self.DeltaCN == other.DeltaCN and \
                   self.matched_ions == other.matched_ions and self.expected_ions == other.expected_ions and \
                   self.sequence == other.sequence and self.validation_status == other.validation_status and \
                   self.predicted_ook0 == other.predicted_ook0 and self.tims_score == other.tims_score and \
                   self.tims_b_score_m2 == other.tims_b_score_m2 and \
                   self.tims_b_score_best_m == other.tims_b_score_best_m

@dataclass
class SLine(Line):
    """
    Class keeping track of sqt S lines.

    Example S_line:
        S [low scan] [high scan] [charge] [process time] [server] [experimental mass] [total ion intensity]
        [lowest Sp] [# of seq. matched] [experimental 1/k0]
        #S	83131	83131	5	34	paserbox_Thread-71766	5417.09229	353.00	0.0016	0	1.2735202
    """

    low_scan: int
    high_scan: int
    charge: int
    process_time: int
    server: str
    experimental_mass: float
    total_ion_intensity: float
    lowest_Sp: float
    number_matches: int
    experimental_ook0: float
    experimental_mz: float
    corrected_ook0: float

    m_lines: List[MLine] = field(default_factory=list)

    def __eq__(self, other):
        if not isinstance(other, SLine):
            return False
        else:
            return self.low_scan == other.low_scan and self.high_scan == other.high_scan and \
                   self.charge == other.charge and self.process_time == other.process_time and \
                   self.server == other.server and self.experimental_mass == other.experimental_mass and \
                   self.total_ion_intensity == other.total_ion_intensity and self.lowest_Sp == other.lowest_Sp and \
                   self.number_matches == other.number_matches and self.experimental_ook0 == other.experimental_ook0 and \
                   self.experimental_mz == other.experimental_mz and self.corrected_ook0 == other.corrected_ook0
