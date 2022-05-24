from dataclasses import dataclass
from typing import List, ClassVar, Union

from ..util import Line, serialize_float
from .exceptions import *
from .columns import *


@dataclass
class PeptideLine(Line):
    """
    Class keeping track of Unique lines.

    Example L line:
        Unique	FileName	XCorr	DeltCN	Conf%	M+H+	CalcM+H+	PPM	TotalIntensity	SpR	Prob Score
        pI	IonProportion	Redundancy	Sequence
        *	190806_300ng_180m_03_Slot2-3_1_646_nopd.357198.357198.2	6.4774	0.8641	100.0	1868.9581
        1868.9752	-9.1	422160.0	0	63.016	8.64	95.7	9	R.YVASYLLAALGGNSSPSAK.D

    """

    __slots__ = ['is_unique', 'file_name', 'low_scan', 'high_scan', 'charge', 'x_corr', 'delta_cn',
                 'Conf', 'mass_plus_hydrogen', 'calc_mass_plus_hydrogen', 'ppm', 'total_intensity', 'spr', 'pi',
                 'ion_proportion', 'redundancy', 'sequence', 'measured_im_value', 'predicted_im_value', 'im_score',
                 'ret_time', 'ptm_index', 'ptm_index_protein_list']

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
    total_intensity: float
    spr: int
    ion_proportion: float
    redundancy: int
    sequence: str

    # some versions include these elements
    prob_score: Union[float, None]
    pi: Union[float, None]
    measured_im_value: Union[float, None]
    predicted_im_value: Union[float, None]
    im_score: Union[float, None]
    ret_time: Union[float, None]
    ptm_index: Union[str, None]
    ptm_index_protein_list: Union[str, None]

    experimental_mz: Union[float, None]
    corrected_1k0: Union[float, None]
    ion_mobility: Union[float, None]

    X_CORR_PRECISION: ClassVar[int] = 4
    DELTA_CN_PRECISION: ClassVar[int] = 4
    CONF_PRECISION: ClassVar[int] = 14
    MASS_PLUS_HYDROGEN_PRECISION: ClassVar[int] = 4
    CALC_MASS_PLUS_HYDROGEN_PRECISION: ClassVar[int] = 4
    PPM_PRECISION: ClassVar[int] = 1
    TOTAL_INTENSITY_PRECISION: ClassVar[int] = 1
    PI_PRECISION: ClassVar[int] = 3
    PROB_SCORE_PRECISION: ClassVar[int] = 6
    ION_PROPORTION_PRECISION: ClassVar[int] = 2
    MEASURED_IM_VALUE_PRECISION: ClassVar[int] = 4
    PREDICTED_IM_VALUE_PRECISION: ClassVar[int] = 16
    IM_SCORE_PRECISION: ClassVar[int] = 4
    RET_TIME_PRECISION: ClassVar[int] = 4
    EXPERIMENTAL_MZ_PRECISION: ClassVar[int] = 4
    CORRECTED_OOK0_PRECISION: ClassVar[int] = 4
    ION_MOBILITY_PRECISION: ClassVar[int] = 4

    @staticmethod
    def deserialize(line: str, version="v2.1.13") -> 'PeptideLine':
        line_elements = line.rstrip().split("\t")

        if version == "v2.1.12":
            columns = PeptideLineColumns_v2_1_12

            if len(line_elements) != len(columns):
                raise DTASelectFilterDeserializationPeptideLineException(line)

            is_unique = PeptideLine._deserialize_is_unique(line_elements[columns.is_unique.value])
            file_name, low_scan, high_scan, charge = \
                PeptideLine._deserialize_file_line(line_elements[columns.file_name.value])
            x_corr = PeptideLine._deserialize_x_corr(line_elements[columns.x_corr.value])
            delta_cn = PeptideLine._deserialize_delta_cn(line_elements[columns.delta_cn.value])
            conf = PeptideLine._deserialize_conf(line_elements[columns.conf.value])
            mass_plus_hydrogen = \
                PeptideLine._deserialize_mass_plus_hydrogen(line_elements[columns.mass_plus_hydrogen.value])
            calc_mass_plus_hydrogen = \
                PeptideLine._deserialize_calc_mass_plus_hydrogen(line_elements[columns.calc_mass_plus_hydrogen.value])
            total_intensity = PeptideLine._deserialize_total_intensity(line_elements[columns.total_intensity.value])
            spr = PeptideLine._deserialize_spr(line_elements[columns.spr.value])
            prob_score = PeptideLine._deserialize_prob_score(line_elements[columns.prob_score.value])
            ion_proportion = PeptideLine._deserialize_ion_proportion(line_elements[columns.ion_proportion.value])
            redundancy = PeptideLine._deserialize_redundancy(line_elements[columns.redundancy.value])
            sequence = PeptideLine._deserialize_sequence(line_elements[columns.sequence.value])
            ppm = None
            pi = None
            measured_im_value = None
            predicted_im_value = None
            im_score = None
            ret_time = None
            ptm_index = None
            ptm_index_protein_list = None
            experimental_mz = None
            corrected_1k0 = None
            ion_mobility = None

        elif version == "v2.1.13":
            columns = PeptideLineColumns_v2_1_13

            if len(line_elements) != len(columns):
                raise DTASelectFilterDeserializationPeptideLineException(line)

            is_unique = PeptideLine._deserialize_is_unique(line_elements[columns.is_unique.value])
            file_name, low_scan, high_scan, charge = \
                PeptideLine._deserialize_file_line(line_elements[columns.file_name.value])
            x_corr = PeptideLine._deserialize_x_corr(line_elements[columns.x_corr.value])
            delta_cn = PeptideLine._deserialize_delta_cn(line_elements[columns.delta_cn.value])
            conf = PeptideLine._deserialize_conf(line_elements[columns.conf.value])
            mass_plus_hydrogen = \
                PeptideLine._deserialize_mass_plus_hydrogen(line_elements[columns.mass_plus_hydrogen.value])
            calc_mass_plus_hydrogen = \
                PeptideLine._deserialize_calc_mass_plus_hydrogen(line_elements[columns.calc_mass_plus_hydrogen.value])
            ppm = PeptideLine._deserialize_ppm(line_elements[columns.ppm.value])
            total_intensity = PeptideLine._deserialize_total_intensity(line_elements[columns.total_intensity.value])
            spr = PeptideLine._deserialize_spr(line_elements[columns.spr.value])
            pi = PeptideLine._deserialize_pi(line_elements[columns.pi.value])
            prob_score = PeptideLine._deserialize_prob_score(line_elements[columns.prob_score.value])
            ion_proportion = PeptideLine._deserialize_ion_proportion(line_elements[columns.ion_proportion.value])
            redundancy = PeptideLine._deserialize_redundancy(line_elements[columns.redundancy.value])
            sequence = PeptideLine._deserialize_sequence(line_elements[columns.sequence.value])
            measured_im_value = \
                PeptideLine._deserialize_measured_im_value(line_elements[columns.measured_im_value.value])
            predicted_im_value = \
                PeptideLine._deserialize_predicted_im_value(line_elements[columns.predicted_im_value.value])
            im_score = PeptideLine._deserialize_im_score(line_elements[columns.im_score.value])
            ret_time = None
            ptm_index = None
            ptm_index_protein_list = None
            experimental_mz = None
            corrected_1k0 = None
            ion_mobility = None

        elif version == "v2.1.12_paser":
            columns = PeptideLineColumns_v2_1_12_paser

            if len(line_elements) != len(columns):
                raise DTASelectFilterDeserializationPeptideLineException(line)

            is_unique = PeptideLine._deserialize_is_unique(line_elements[columns.is_unique.value])
            file_name, low_scan, high_scan, charge = \
                PeptideLine._deserialize_file_line(line_elements[columns.file_name.value])
            x_corr = PeptideLine._deserialize_x_corr(line_elements[columns.x_corr.value])
            delta_cn = PeptideLine._deserialize_delta_cn(line_elements[columns.delta_cn.value])
            conf = PeptideLine._deserialize_conf(line_elements[columns.conf.value])
            mass_plus_hydrogen = \
                PeptideLine._deserialize_mass_plus_hydrogen(line_elements[columns.mass_plus_hydrogen.value])
            calc_mass_plus_hydrogen = \
                PeptideLine._deserialize_calc_mass_plus_hydrogen(line_elements[columns.calc_mass_plus_hydrogen.value])
            ppm = PeptideLine._deserialize_ppm(line_elements[columns.ppm.value])
            total_intensity = PeptideLine._deserialize_total_intensity(line_elements[columns.total_intensity.value])
            spr = PeptideLine._deserialize_spr(line_elements[columns.spr.value])
            pi = PeptideLine._deserialize_pi(line_elements[columns.pi.value])
            prob_score = PeptideLine._deserialize_prob_score(line_elements[columns.prob_score.value])
            ion_proportion = PeptideLine._deserialize_ion_proportion(line_elements[columns.ion_proportion.value])
            redundancy = PeptideLine._deserialize_redundancy(line_elements[columns.redundancy.value])
            sequence = PeptideLine._deserialize_sequence(line_elements[columns.sequence.value])
            ret_time = PeptideLine._deserialize_ret_time(line_elements[columns.ret_time.value])
            ptm_index = PeptideLine._deserialize_ptm_index(line_elements[columns.ptm_index.value])
            ptm_index_protein_list = \
                PeptideLine._deserialize_ptm_index_protein_list(line_elements[columns.ptm_index_protein_list.value])
            measured_im_value = None
            predicted_im_value = None
            im_score = None
            experimental_mz = None
            corrected_1k0 = None
            ion_mobility = None
            
        elif version == "v2.1.13_timscore":
            columns = PeptideLineColumns_v2_1_13_timscore

            if len(line_elements) != len(columns):
                raise DTASelectFilterDeserializationPeptideLineException(line)

            is_unique = PeptideLine._deserialize_is_unique(line_elements[columns.is_unique.value])
            file_name, low_scan, high_scan, charge = PeptideLine._deserialize_file_line(line_elements[columns.file_name.value])
            x_corr = PeptideLine._deserialize_x_corr(line_elements[columns.x_corr.value])
            delta_cn = PeptideLine._deserialize_delta_cn(line_elements[columns.delta_cn.value])
            conf = PeptideLine._deserialize_conf(line_elements[columns.conf.value])
            mass_plus_hydrogen = PeptideLine._deserialize_mass_plus_hydrogen(line_elements[columns.mass_plus_hydrogen.value])
            calc_mass_plus_hydrogen = PeptideLine._deserialize_calc_mass_plus_hydrogen(line_elements[columns.calc_mass_plus_hydrogen.value])
            ppm = PeptideLine._deserialize_ppm(line_elements[columns.ppm.value])
            total_intensity = PeptideLine._deserialize_total_intensity(line_elements[columns.total_intensity.value])
            spr = PeptideLine._deserialize_spr(line_elements[columns.spr.value])
            prob_score = PeptideLine._deserialize_prob_score(line_elements[columns.prob_score.value])
            pi = PeptideLine._deserialize_pi(line_elements[columns.pi.value])
            ion_proportion = PeptideLine._deserialize_ion_proportion(line_elements[columns.ion_proportion.value])
            redundancy = PeptideLine._deserialize_redundancy(line_elements[columns.redundancy.value])
            measured_im_value = PeptideLine._deserialize_measured_im_value(line_elements[columns.measured_im_value.value])
            predicted_im_value = PeptideLine._deserialize_predicted_im_value(line_elements[columns.predicted_im_value.value])
            im_score = PeptideLine._deserialize_im_score(line_elements[columns.im_score.value])
            sequence = PeptideLine._deserialize_sequence(line_elements[columns.sequence.value])
            experimental_mz = PeptideLine._deserialize_experimental_mz(line_elements[columns.experimental_mz.value])
            corrected_1k0 = PeptideLine._deserialize_corrected_1k0(line_elements[columns.corrected_1k0.value])
            ion_mobility = PeptideLine._deserialize_ion_mobility(line_elements[columns.ion_mobility.value])
            ret_time = PeptideLine._deserialize_ret_time(line_elements[columns.ret_time.value])
            ptm_index = PeptideLine._deserialize_ptm_index(line_elements[columns.ptm_index.value])
            ptm_index_protein_list = PeptideLine._deserialize_ptm_index_protein_list(line_elements[columns.ptm_index_protein_list.value])

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
                           sequence=sequence,
                           measured_im_value=measured_im_value,
                           predicted_im_value=predicted_im_value,
                           im_score=im_score,
                           ret_time=ret_time,
                           ptm_index=ptm_index,
                           ptm_index_protein_list=ptm_index_protein_list,
                           experimental_mz=experimental_mz,
                           corrected_1k0=corrected_1k0,
                           ion_mobility=ion_mobility,
                           )

        return line

    @staticmethod
    def _deserialize_is_unique(val):
        return "*" == val

    @staticmethod
    def _deserialize_file_name(val):
        return val

    @staticmethod
    def _deserialize_low_scan(val):
        return int(val)

    @staticmethod
    def _deserialize_high_scan(val):
        return int(val)

    @staticmethod
    def _deserialize_charge(val):
        return int(val)

    @staticmethod
    def _deserialize_file_line(val):
        val_elems = val.split(".")
        file_name = PeptideLine._deserialize_file_name(val_elems[PeptideLineFileNameColumns.file_name.value])
        low_scan = PeptideLine._deserialize_low_scan(val_elems[PeptideLineFileNameColumns.low_scan.value])
        high_scan = PeptideLine._deserialize_high_scan(val_elems[PeptideLineFileNameColumns.high_scan.value])
        charge = PeptideLine._deserialize_charge(val_elems[PeptideLineFileNameColumns.charge.value])
        return file_name, low_scan, high_scan, charge

    @staticmethod
    def _deserialize_x_corr(val):
        return float(val)

    @staticmethod
    def _deserialize_delta_cn(val):
        return float(val)

    @staticmethod
    def _deserialize_conf(val):
        return float(val)

    @staticmethod
    def _deserialize_mass_plus_hydrogen(val):
        return float(val)

    @staticmethod
    def _deserialize_calc_mass_plus_hydrogen(val):
        return float(val)

    @staticmethod
    def _deserialize_ppm(val):
        return float(val)

    @staticmethod
    def _deserialize_total_intensity(val):
        return float(val)

    @staticmethod
    def _deserialize_spr(val):
        return int(val)

    @staticmethod
    def _deserialize_pi(val):
        return float(val)

    @staticmethod
    def _deserialize_prob_score(val):
        return float(val)

    @staticmethod
    def _deserialize_ion_proportion(val):
        return float(val)

    @staticmethod
    def _deserialize_redundancy(val):
        return int(val)

    @staticmethod
    def _deserialize_measured_im_value(val):
        return None if val == "NA" else float(val)

    @staticmethod
    def _deserialize_predicted_im_value(val):
        return None if val == "NA" else float(val)

    @staticmethod
    def _deserialize_im_score(val):
        return None if val == "NA" else float(val)

    @staticmethod
    def _deserialize_sequence(val):
        return val

    @staticmethod
    def _deserialize_ret_time(val):
        return float(val)

    @staticmethod
    def _deserialize_ptm_index(val):
        return None if val == "NA" else str(val)

    @staticmethod
    def _deserialize_ptm_index_protein_list(val):
        return None if val == "NA" else str(val)

    @staticmethod
    def _deserialize_experimental_mz(val):
        return None if val == "NA" else float(val)

    @staticmethod
    def _deserialize_corrected_1k0(val):
        return None if val == "NA" else float(val)

    @staticmethod
    def _deserialize_ion_mobility(val):
        return None if val == "NA" else float(val)

    def serialize(self, version="v2.1.13") -> str:
        if version == "v2.1.12":
            columns = PeptideLineColumns_v2_1_12
            line_elements = [""] * len(columns)
            line_elements[columns.is_unique.value] = self._serialize_is_unique()
            line_elements[columns.file_name.value] = self._serialize_file_line()
            line_elements[columns.x_corr.value] = self._serialize_x_corr()
            line_elements[columns.delta_cn.value] = self._serialize_delta_cn()
            line_elements[columns.conf.value] = self._serialize_conf()
            line_elements[columns.mass_plus_hydrogen.value] = self._serialize_mass_plus_hydrogen()
            line_elements[columns.calc_mass_plus_hydrogen.value] = self._serialize_calc_mass_plus_hydrogen()
            line_elements[columns.total_intensity.value] = self._serialize_total_intensity()
            line_elements[columns.spr.value] = self._serialize_spr()
            line_elements[columns.prob_score.value] = self._serialize_prob_score()
            line_elements[columns.ion_proportion.value] = self._serialize_ion_proportion()
            line_elements[columns.redundancy.value] = self._serialize_redundancy()
            line_elements[columns.sequence.value] = self._serialize_sequence()
            return '\t'.join(line_elements) + '\n'

        elif version == "v2.1.13":

            columns = PeptideLineColumns_v2_1_13
            line_elements = [""] * len(columns)
            line_elements[columns.is_unique.value] = self._serialize_is_unique()
            line_elements[columns.file_name.value] = self._serialize_file_line()
            line_elements[columns.x_corr.value] = self._serialize_x_corr()
            line_elements[columns.delta_cn.value] = self._serialize_delta_cn()
            line_elements[columns.conf.value] = self._serialize_conf()
            line_elements[columns.mass_plus_hydrogen.value] = self._serialize_mass_plus_hydrogen()
            line_elements[columns.calc_mass_plus_hydrogen.value] = self._serialize_calc_mass_plus_hydrogen()
            line_elements[columns.ppm.value] = self._serialize_ppm()
            line_elements[columns.total_intensity.value] = self._serialize_total_intensity()
            line_elements[columns.spr.value] = self._serialize_spr()
            line_elements[columns.prob_score.value] = self._serialize_prob_score()
            line_elements[columns.ion_proportion.value] = self._serialize_ion_proportion()
            line_elements[columns.redundancy.value] = self._serialize_redundancy()
            line_elements[columns.measured_im_value.value] = self._serialize_measured_im_value()
            line_elements[columns.predicted_im_value.value] = self._serialize_predicted_im_value()
            line_elements[columns.im_score.value] = self._serialize_im_score()
            line_elements[columns.sequence.value] = self._serialize_sequence()
            return '\t'.join(line_elements) + '\n'

        elif version == "v2.1.12_paser":
            columns = PeptideLineColumns_v2_1_12_paser
            line_elements = [""] * len(columns)
            line_elements[columns.is_unique.value] = self._serialize_is_unique()
            line_elements[columns.file_name.value] = self._serialize_file_line()
            line_elements[columns.x_corr.value] = self._serialize_x_corr()
            line_elements[columns.delta_cn.value] = self._serialize_delta_cn()
            line_elements[columns.conf.value] = self._serialize_conf()
            line_elements[columns.mass_plus_hydrogen.value] = self._serialize_mass_plus_hydrogen()
            line_elements[columns.calc_mass_plus_hydrogen.value] = self._serialize_calc_mass_plus_hydrogen()
            line_elements[columns.ppm.value] = self._serialize_ppm()
            line_elements[columns.total_intensity.value] = self._serialize_total_intensity()
            line_elements[columns.spr.value] = self._serialize_spr()
            line_elements[columns.prob_score.value] = self._serialize_prob_score()
            line_elements[columns.pi.value] = self._serialize_pi()
            line_elements[columns.ion_proportion.value] = self._serialize_ion_proportion()
            line_elements[columns.redundancy.value] = self._serialize_redundancy()
            line_elements[columns.sequence.value] = self._serialize_sequence()
            line_elements[columns.ret_time.value] = self._serialize_ret_time()
            line_elements[columns.ptm_index.value] = self._serialize_ptm_index()
            line_elements[columns.ptm_index_protein_list.value] = self._serialize_ptm_index_protein_list()
            return '\t'.join(line_elements) + '\n'
        elif version == "v2.1.13_timscore":
            columns = PeptideLineColumns_v2_1_13_timscore
            line_elements = [""] * len(columns)
            line_elements[columns.is_unique.value] = self._serialize_is_unique()
            line_elements[columns.file_name.value] = self._serialize_file_line()
            line_elements[columns.x_corr.value] = self._serialize_x_corr()
            line_elements[columns.delta_cn.value] = self._serialize_delta_cn()
            line_elements[columns.conf.value] = self._serialize_conf()
            line_elements[columns.mass_plus_hydrogen.value] = self._serialize_mass_plus_hydrogen()
            line_elements[columns.calc_mass_plus_hydrogen.value] = self._serialize_calc_mass_plus_hydrogen()
            line_elements[columns.ppm.value] = self._serialize_ppm()
            line_elements[columns.total_intensity.value] = self._serialize_total_intensity()
            line_elements[columns.spr.value] = self._serialize_spr()
            line_elements[columns.prob_score.value] = self._serialize_prob_score()
            line_elements[columns.pi.value] = self._serialize_pi()
            line_elements[columns.ion_proportion.value] = self._serialize_ion_proportion()
            line_elements[columns.redundancy.value] = self._serialize_redundancy()
            line_elements[columns.measured_im_value.value] = self._serialize_measured_im()
            line_elements[columns.predicted_im_value.value] = self._serialize_predicted_im_value()
            line_elements[columns.im_score.value] = self._serialize_im_score()
            line_elements[columns.sequence.value] = self._serialize_sequence()
            line_elements[columns.experimental_mz.value] = self._serialize_experimental_mz()
            line_elements[columns.corrected_1k0.value] = self._serialize_corrected_1k0()
            line_elements[columns.ion_mobility.value] = self._serialize_ion_mobility()
            line_elements[columns.ret_time.value] = self._serialize_ret_time()
            line_elements[columns.ptm_index.value] = self._serialize_ptm_index()
            line_elements[columns.ptm_index_protein_list.value] = self._serialize_ptm_index_protein_list()
        else:
            raise NotImplementedError

    def _serialize_is_unique(self) -> str:
        return '*' if self.is_unique else ''

    def _serialize_file_name(self) -> str:
        return self.file_name

    def _serialize_low_scan(self) -> str:
        return f"{self.low_scan}"

    def _serialize_high_scan(self) -> str:
        return f"{self.high_scan}"

    def _serialize_charge(self) -> str:
        return f"{self.charge}"

    def _serialize_file_line(self) -> str:
        file_line_elements = [""] * len(PeptideLineFileNameColumns)
        file_line_elements[PeptideLineFileNameColumns.file_name.value] = self._serialize_file_name()
        file_line_elements[PeptideLineFileNameColumns.low_scan.value] = self._serialize_low_scan()
        file_line_elements[PeptideLineFileNameColumns.high_scan.value] = self._serialize_high_scan()
        file_line_elements[PeptideLineFileNameColumns.charge.value] = self._serialize_charge()
        return ".".join(file_line_elements)

    def _serialize_x_corr(self) -> str:
        return str(round(self.x_corr, PeptideLine.X_CORR_PRECISION))

    def _serialize_delta_cn(self) -> str:
        return str(round(self.delta_cn, PeptideLine.DELTA_CN_PRECISION))

    def _serialize_conf(self) -> str:
        return str(round(self.conf, PeptideLine.CONF_PRECISION))

    def _serialize_mass_plus_hydrogen(self) -> str:
        return str(round(self.mass_plus_hydrogen, PeptideLine.MASS_PLUS_HYDROGEN_PRECISION))

    def _serialize_calc_mass_plus_hydrogen(self) -> str:
        return str(round(self.calc_mass_plus_hydrogen, PeptideLine.CALC_MASS_PLUS_HYDROGEN_PRECISION))

    def _serialize_ppm(self) -> str:
        return str(round(self.ppm, self.PPM_PRECISION))

    def _serialize_total_intensity(self) -> str:
        return str(round(self.total_intensity, self.TOTAL_INTENSITY_PRECISION))

    def _serialize_spr(self) -> str:
        return f"{self.spr}"

    def _serialize_pi(self) -> str:
        return str(round(self.pi, self.PI_PRECISION))

    def _serialize_prob_score(self) -> str:
        return str(round(self.prob_score, self.PROB_SCORE_PRECISION))

    def _serialize_ion_proportion(self) -> str:
        return str(round(self.ion_proportion, self.ION_PROPORTION_PRECISION))

    def _serialize_redundancy(self) -> str:
        return f"{self.redundancy}"

    def _serialize_measured_im_value(self) -> str:
        return str(
            round(self.measured_im_value, PeptideLine.MEASURED_IM_VALUE_PRECISION)) if self.measured_im_value else "NA"

    def _serialize_predicted_im_value(self) -> str:
        return str(round(self.predicted_im_value,
                         PeptideLine.PREDICTED_IM_VALUE_PRECISION)) if self.predicted_im_value else "NA"

    def _serialize_im_score(self) -> str:
        return str(round(self.im_score, PeptideLine.IM_SCORE_PRECISION)) if self.im_score else "NA"

    def _serialize_sequence(self) -> str:
        return self.sequence

    def _serialize_ret_time(self) -> str:
        return str(round(self.ret_time, PeptideLine.RET_TIME_PRECISION))

    def _serialize_ptm_index(self) -> str:
        return f"{self.ptm_index}" if self.ptm_index else "NA"

    def _serialize_ptm_index_protein_list(self) -> str:
        return f"{self.ptm_index_protein_list}" if self.ptm_index_protein_list else "NA"

    def _serialize_experimental_mz(self) -> str:
        return str(round(self.experimental_mz, PeptideLine.EXPERIMENTAL_MZ_PRECISION))

    def _serialize_corrected_1k0(self) -> str:
        return str(round(self.corrected_1k0, PeptideLine.CORRECTED_OOK0_PRECISION))

    def _serialize_ion_mobility(self) -> str:
        return str(round(self.ion_mobility, PeptideLine.ION_MOBILITY_PRECISION))


@dataclass
class ProteinLine(Line):
    """
    Class keeping track of sqt Locus lines.

    Example L line:
        Locus	Sequence Count	Spectrum Count	Sequence Coverage	Length	MolWt	pI	Validation Status
        NSAF	EMPAI	Descriptive Name
        sp|P05387|RLA2_HUMAN	9	62	84.3%	115	11665	4.5	U	0.0025080831	5.966266	60S acidic ribosomal
        protein P2 OS=Homo sapiens OX=9606 GN=RPLP2 PE=1 SV=1
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
    h_redundancy: int
    l_redundancy: int
    m_redundancy: int

    SEQUENCE_COVERAGE_PRECISION: ClassVar[int] = 1
    PI_PRECISION: ClassVar[int] = 1
    NSAF_PRECISION: ClassVar[int] = 10
    EMPAI_PRECISION: ClassVar[int] = 8

    @staticmethod
    def deserialize(line: str, version="v2.1.13") -> 'ProteinLine':

        line_elements = line.rstrip().split("\t")

        if version == "v2.1.12" or version == "v2.1.13":
            columns = ProteinLineColumns_v2_1_12

            if len(line_elements) != len(columns):
                raise DTASelectFilterDeserializationProteinLineException(line)

            locus_name = ProteinLine._deserialize_locus_name(line_elements[columns.locus_name.value])
            sequence_count = ProteinLine._deserialize_sequence_count(line_elements[columns.sequence_count.value])
            spectrum_count = ProteinLine._deserialize_spectrum_count(line_elements[columns.spectrum_count.value])
            sequence_coverage = ProteinLine._deserialize_sequence_coverage(
                line_elements[columns.sequence_coverage.value][:-1])  # remove % sign
            length = ProteinLine._deserialize_length(line_elements[columns.length.value])
            molWt = ProteinLine._deserialize_molWt(line_elements[columns.molWt.value])
            pi = ProteinLine._deserialize_pi(line_elements[columns.pi.value])
            validation_status = ProteinLine._deserialize_validation_status(
                line_elements[columns.validation_status.value])
            nsaf = ProteinLine._deserialize_nsaf(line_elements[columns.nsaf.value])
            empai = ProteinLine._deserialize_empai(line_elements[columns.empai.value])
            description_name = ProteinLine._deserialize_description_name(line_elements[columns.description_name.value])
            h_redundancy = None
            l_redundancy = None
            m_redundancy = None

        elif version == "v2.1.12_paser" or version == "v2.1.13_timscore":
            columns = ProteinLineColumns_v2_1_12_paser

            if len(line_elements) != len(columns):
                raise DTASelectFilterDeserializationProteinLineException(line)

            locus_name = ProteinLine._deserialize_locus_name(line_elements[columns.locus_name.value])
            sequence_count = ProteinLine._deserialize_sequence_count(line_elements[columns.sequence_count.value])
            spectrum_count = ProteinLine._deserialize_spectrum_count(line_elements[columns.spectrum_count.value])
            sequence_coverage = ProteinLine._deserialize_sequence_coverage(
                line_elements[columns.sequence_coverage.value][:-1])  # remove % sign
            length = ProteinLine._deserialize_length(line_elements[columns.length.value])
            molWt = ProteinLine._deserialize_molWt(line_elements[columns.molWt.value])
            pi = ProteinLine._deserialize_pi(line_elements[columns.pi.value])
            validation_status = ProteinLine._deserialize_validation_status(
                line_elements[columns.validation_status.value])
            nsaf = ProteinLine._deserialize_nsaf(line_elements[columns.nsaf.value])
            empai = ProteinLine._deserialize_empai(line_elements[columns.empai.value])
            description_name = ProteinLine._deserialize_description_name(line_elements[columns.description_name.value])
            h_redundancy = ProteinLine._deserialize_h_redundancy(line_elements[columns.h_redundancy.value])
            l_redundancy = ProteinLine._deserialize_l_redundancy(line_elements[columns.l_redundancy.value])
            m_redundancy = ProteinLine._deserialize_m_redundancy(line_elements[columns.m_redundancy.value])

        else:
            raise NotImplementedError

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
                           description_name=description_name,
                           h_redundancy=h_redundancy,
                           l_redundancy=l_redundancy,
                           m_redundancy=m_redundancy
                           )
        return line

    @staticmethod
    def _deserialize_locus_name(val):
        return val

    @staticmethod
    def _deserialize_sequence_count(val):
        return int(val)

    @staticmethod
    def _deserialize_spectrum_count(val):
        return int(val)

    @staticmethod
    def _deserialize_sequence_coverage(val):
        return float(val)

    @staticmethod
    def _deserialize_length(val):
        return int(val)

    @staticmethod
    def _deserialize_molWt(val):
        return int(val)

    @staticmethod
    def _deserialize_pi(val):
        return float(val)

    @staticmethod
    def _deserialize_validation_status(val):
        return val

    @staticmethod
    def _deserialize_nsaf(val):
        return float(val)

    @staticmethod
    def _deserialize_empai(val):
        return float(val)

    @staticmethod
    def _deserialize_description_name(val):
        return val

    @staticmethod
    def _deserialize_h_redundancy(val):
        return int(val)

    @staticmethod
    def _deserialize_l_redundancy(val):
        return int(val)

    @staticmethod
    def _deserialize_m_redundancy(val):
        return int(val)

    def serialize(self, version="v2.1.13") -> str:
        if version == "v2.1.12" or version == "v2.1.13":
            columns = ProteinLineColumns_v2_1_12
            line_elements = [""] * len(columns)
            line_elements[columns.locus_name.value] = self._serialize_locus_name()
            line_elements[columns.sequence_count.value] = self._serialize_sequence_count()
            line_elements[columns.spectrum_count.value] = self._serialize_spectrum_count()
            line_elements[columns.sequence_coverage.value] = self._serialize_sequence_coverage()
            line_elements[columns.length.value] = self._serialize_length()
            line_elements[columns.molWt.value] = self._serialize_molWt()
            line_elements[columns.pi.value] = self._serialize_pi()
            line_elements[columns.validation_status.value] = self._serialize_validation_status()
            line_elements[columns.nsaf.value] = self._serialize_nsaf()
            line_elements[columns.empai.value] = self._serialize_empai()
            line_elements[columns.description_name.value] = self._serialize_description_name()

        elif version == "v2.1.12_paser" or version == "v2.1.13_timscore":
            columns = ProteinLineColumns_v2_1_12_paser
            line_elements = [""] * len(columns)
            line_elements[columns.locus_name.value] = self._serialize_locus_name()
            line_elements[columns.sequence_count.value] = self._serialize_sequence_count()
            line_elements[columns.spectrum_count.value] = self._serialize_spectrum_count()
            line_elements[columns.sequence_coverage.value] = self._serialize_sequence_coverage()
            line_elements[columns.length.value] = self._serialize_length()
            line_elements[columns.molWt.value] = self._serialize_molWt()
            line_elements[columns.pi.value] = self._serialize_pi()
            line_elements[columns.validation_status.value] = self._serialize_validation_status()
            line_elements[columns.nsaf.value] = self._serialize_nsaf()
            line_elements[columns.empai.value] = self._serialize_empai()
            line_elements[columns.description_name.value] = self._serialize_description_name()
            line_elements[columns.h_redundancy.value] = self._serialize_h_redundancy()
            line_elements[columns.l_redundancy.value] = self._serialize_l_redundancy()
            line_elements[columns.m_redundancy.value] = self._serialize_m_redundancy()

        else:
            raise NotImplementedError

        return '\t'.join(line_elements) + '\n'

    def _serialize_locus_name(self):
        return self.locus_name

    def _serialize_sequence_count(self):
        return f"{self.sequence_count}"

    def _serialize_spectrum_count(self):
        return f"{self.spectrum_count}"

    def _serialize_sequence_coverage(self):
        return serialize_float(self.sequence_coverage, ProteinLine.SEQUENCE_COVERAGE_PRECISION) + "%"

    def _serialize_length(self):
        return f"{self.length}"

    def _serialize_molWt(self):
        return f"{self.molWt}"

    def _serialize_pi(self):
        return f"{self.pi:.{ProteinLine.PI_PRECISION}f}"

    def _serialize_validation_status(self):
        return self.validation_status

    def _serialize_nsaf(self):
        #return f"{self.nsaf:.{ProteinLine.NSAF_PRECISION}E}"
        #return f"{self.nsaf:.{ProteinLine.NSAF_PRECISION}f}"
        return str(round(self.nsaf, ProteinLine.NSAF_PRECISION))

    def _serialize_empai(self):
        return str(round(self.empai, ProteinLine.EMPAI_PRECISION))
        # return f"{self.empai:.{ProteinLine.EMPAI_PRECISION}f}"

    def _serialize_description_name(self):
        return self.description_name

    def _serialize_h_redundancy(self):
        return f"{self.h_redundancy}"

    def _serialize_l_redundancy(self):
        return f"{self.l_redundancy}"

    def _serialize_m_redundancy(self):
        return f"{self.m_redundancy}"


@dataclass
class DTAFilterResult:
    protein_line: ProteinLine
    peptide_lines: List[PeptideLine]

    def serialize(self, version) -> str:
        lines = [self.protein_line] + self.peptide_lines
        return ''.join([line.serialize(version=version) for line in lines])
