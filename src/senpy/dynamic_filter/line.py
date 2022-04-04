import ast
from dataclasses import dataclass, make_dataclass
from typing import ClassVar, List

from senpy.util import Line


def interpret(val):
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val


def clean_header(header: str):
    header = header.replace("%", "")
    header = header.replace("+", "")
    header = header.replace(" ", "_")
    return header


def get_data_class(line: str, h_line_components, class_name):
    line_elements = line.rstrip().split("\t")
    line_elements = [interpret(elem) for elem in line_elements]
    line_elems_type_tuple = [(key, type(elem)) for elem, key in zip(line_elements, h_line_components)]
    return make_dataclass(class_name, line_elems_type_tuple)


def get_dict(line: str, h_line_components):
    line_elements = line.rstrip().split("\t")
    line_elements = [interpret(elem) for elem in line_elements]
    return {key:value for key, value in zip(h_line_components, line_elements)}


if __name__ == '__main__':

    header = "Unique	FileName	XCorr	DeltCN	Conf%	M+H+	CalcM+H+	PPM	TotalIntensity	SpR	Prob Score	pI	IonProportion	Redundancy	Measured_IM_Value	Predicted_IM_Value	IM_Score	Sequence"
    peptide_line = "*	190806_300ng_180m_03_Slot2-3_1_646_nopd.357198.357198.2	6.4774	0.8641	100.0	1868.9581	1868.9752	-9.1	422160.0	0	63.016	8.64	95.7	9	1.1144	1.1519999504089355	0.5299	R.YVASYLLAALGGNSSPSAK.D"

    header_valid = clean_header(header)
    PeptideLine = get_data_class(peptide_line, header.split("\t"), 'PeptideLine')
    print(PeptideLine(*[interpret(elem) for elem in peptide_line.rstrip().split("\t")]))