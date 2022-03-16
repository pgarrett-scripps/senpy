from dataclasses import dataclass, field
from typing import List

from senpy.util import Line


@dataclass
class UniqueLine(Line):
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
    Conf: float
    mass_plus_hydrogen: float
    calc_mass_plus_hydrogen: float
    ppm: float
    total_intensity: float
    spr: int
    pi: float
    ion_proportion: float
    redundancy: int
    sequence: str

    def get_clean_seq(self) -> str:
        return self.sequence[2:-2]


@dataclass
class LocusLine(Line):
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

    unique_lines: List[UniqueLine] = field(default_factory=list)
