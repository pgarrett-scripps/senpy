from dataclasses import dataclass, field
from typing import List

from senpy.abstract_class import Line


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

    xcoor_rank: int
    sp_rank: int
    calculated_mass: float
    DeltaCN: float
    xcorr: float
    sp: int
    matched_ions: int
    expected_ions: int
    sequence: str
    validation_status: str

    l_lines: List[LLine] = field(default_factory=list)

    def get_clean_seq(self) -> str:
        return self.sequence[2:-2]

    def is_reverse(self) -> bool:
        for l_line in self.l_lines:
            if "sp" == l_line.locus_name[:2]:
                return False
        return True

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

    m_lines: List[MLine] = field(default_factory=list)
