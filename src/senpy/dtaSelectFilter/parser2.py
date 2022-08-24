from enum import Enum, auto
from typing import List, Dict, Union
from dataclasses import dataclass, field


def apply_transformation(val, t):
    if val is not None:
        val = t(val)
    return val


@dataclass
class ProteinLine:
    data: Dict[str, str]

    @property
    def locus(self) -> Union[bool, str]:
        return apply_transformation(self.data.get('Locus'), str)

    @property
    def sequence_count(self) -> Union[int, None]:
        return apply_transformation(self.data.get('Sequence Count'), int)

    @property
    def spectrum_count(self) -> Union[int, None]:
        return apply_transformation(self.data.get('Spectrum Count'), int)

    @property
    def sequence_coverage(self) -> Union[float, None]:
        return apply_transformation(self.data.get('Sequence Coverage'), lambda x: float(x.strip('%')))

    @property
    def length(self) -> Union[int, None]:
        return apply_transformation(self.data.get('Length'), int)

    @property
    def mol_wt(self) -> Union[int, None]:
        return apply_transformation(self.data.get('MolWt'), int)

    @property
    def pi(self) -> Union[float, None]:
        return apply_transformation(self.data.get('pI'), float)

    @property
    def validation_status(self) -> float:
        return apply_transformation(self.data.get('Validation Status'), str)

    @property
    def nsaf(self) -> float:
        return apply_transformation(self.data.get('NSAF'), float)

    @property
    def empai(self) -> float:
        return apply_transformation(self.data.get('EMPAI'), float)

    @property
    def description_name(self) -> float:
        return apply_transformation(self.data.get('Descriptive Name'), str)

    @property
    def h_redundancy(self) -> float:
        return apply_transformation(self.data.get('HRedundancy'), float)

    @property
    def l_redundancy(self) -> float:
        return apply_transformation(self.data.get('LRedundancy'), float)

    @property
    def m_redundancy(self) -> float:
        return apply_transformation(self.data.get('MRedundancy'), float)


@dataclass
class PeptideLine:
    data: Dict[str, str]

    @property
    def unique(self) -> Union[bool, None]:
        return apply_transformation(self.data.get('Unique'), lambda x: x == "*")

    @property
    def file_name(self) -> Union[str, None]:
        return apply_transformation(self.data.get('FileName'), lambda x: x.split('.')[0])

    @property
    def low_scan(self) -> Union[int, None]:
        return apply_transformation(self.data.get('FileName'), lambda x: int(x.split('.')[1]))

    @property
    def high_scan(self) -> Union[int, None]:
        return apply_transformation(self.data.get('FileName'), lambda x: int(x.split('.')[2]))

    @property
    def charge(self) -> Union[int, None]:
        return apply_transformation(self.data.get('FileName'), lambda x: int(x.split('.')[3]))

    @property
    def x_corr(self) -> Union[float, None]:
        return apply_transformation(self.data.get('XCorr'), float)

    @property
    def delta_cn(self) -> Union[float, None]:
        return apply_transformation(self.data.get('DeltCN'), float)

    @property
    def conf(self) -> Union[float, None]:
        return apply_transformation(self.data.get('Conf%'), float)

    @property
    def mass_plus_hydrogen(self) -> Union[float, None]:
        return apply_transformation(self.data.get('M+H+'), float)

    @property
    def calculated_mass_plus_hydrogen(self) -> Union[float, None]:
        return apply_transformation(self.data.get('CalcM+H+'), float)

    @property
    def ppm(self) -> Union[float, None]:
        return apply_transformation(self.data.get('PPM'), float)

    @property
    def total_intensity(self) -> Union[float, None]:
        return apply_transformation(self.data.get('TotalIntensity'), float)

    @property
    def spr(self) -> Union[float, None]:
        return apply_transformation(self.data.get('SpR'), float)

    @property
    def prob_score(self) -> Union[float, None]:
        return apply_transformation(self.data.get('Prob Score'), float)

    @property
    def pi(self) -> Union[float, None]:
        return apply_transformation(self.data.get('pI'), float)

    @property
    def ion_proportion(self) -> Union[float, None]:
        return apply_transformation(self.data.get('IonProportion'), float)

    @property
    def redundancy(self) -> Union[int, None]:
        return apply_transformation(self.data.get('Redundancy'), int)

    @property
    def sequence(self) -> Union[str, None]:
        return apply_transformation(self.data.get('Sequence'), str)

    @property
    def retention_time(self) -> Union[float, None]:
        return apply_transformation(self.data.get('RetTime'), float)

    @property
    def ptm_index(self) -> Union[int, None]:
        return apply_transformation(self.data.get('PTMIndex'), lambda x: None if x == 'NA' else int(x))

    @property
    def ptm_index_protein_list(self) -> Union[int, None]:
        return apply_transformation(self.data.get('PTMIndex Protein List'), lambda x: None if x == 'NA' else int(x))


@dataclass
class DtaFilterResult:
    proteins: List[ProteinLine] = field(default_factory=lambda: [])
    peptides: List[PeptideLine] = field(default_factory=lambda: [])


class FileState(Enum):
    HEADER = auto()
    COLUMN_NAMES = auto()
    DATA = auto()
    INFO = auto()


def read_file(file_input):

    state = FileState.HEADER

    header_lines = []
    info_lines = []

    protein_columns = None
    peptide_columns = None

    dta_filter_results = [DtaFilterResult()]

    if isinstance(file_input, str):
        with open(file_input) as file:
            lines = file.readlines()
    elif isinstance(file_input, list):
        lines = file_input
    else:
        raise Exception("Input not supported")

    for line in lines:
        line = line.rstrip()

        if state == FileState.HEADER:
            header_lines.append(line.rstrip())

            if line == "":
                state = FileState.COLUMN_NAMES
                continue

        elif state == FileState.COLUMN_NAMES:
            if protein_columns is None:
                protein_columns = line.rstrip().split('\t')
            elif peptide_columns is None:
                peptide_columns = line.rstrip().split('\t')
                state = FileState.DATA
                continue

        elif state == FileState.DATA:
            elems = line.rstrip().split('\t')
            if elems[1].isnumeric():
                if len(dta_filter_results[-1].peptides) != 0:
                    dta_filter_results.append(DtaFilterResult())

                protein_line = ProteinLine({name: val for name, val in zip(protein_columns, elems)})
                dta_filter_results[-1].proteins.append(protein_line)

            elif elems[1].count(".") == 3:
                dta_filter_results[-1].peptides.append(
                    PeptideLine({name: val for name, val in zip(peptide_columns, elems)}))
            else:
                state = FileState.INFO
                continue
        else:
            info_lines.append(line.rstrip())

    return header_lines, dta_filter_results, info_lines
