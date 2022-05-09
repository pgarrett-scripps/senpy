from .lines import ProteinLine, DTAFilterResult, PeptideLine
from enum import Enum


class FileState(Enum):
    HEADER = 1
    DATA = 2
    INFO = 3


def read_file(dta_select_filter_file_path: str, version: str = None) -> ([str], [DTAFilterResult], [str]):
    """
    Return list of FilteredProteinResult's
    """
    dta_filter_results = []
    h_lines = []
    end_lines = []

    file_state = FileState.HEADER

    protein_line = None
    peptide_lines = []

    with open(dta_select_filter_file_path) as file:
        for line in file:
            line_elements = line.split("\t")

            # update file state
            if len(line_elements) > 0 and line_elements[0] == 'Unique':
                h_lines.append(line)
                file_state = FileState.DATA
                continue

            if len(line_elements) > 1 and line_elements[1] == "Proteins":
                dta_filter_results.append(DTAFilterResult(protein_line, peptide_lines))
                file_state = FileState.INFO

            if file_state == FileState.HEADER:
                h_lines.append(line)
                if line[:9] == 'DTASelect':
                    if version is None:
                        version = line.split(" ")[1].rstrip()
                        print("version: ", version)

            if file_state == FileState.DATA:
                if line_elements[0] == '' or line_elements[0] == '*':
                    peptide_lines.append(PeptideLine.deserialize(line, version=version))
                else:
                    if protein_line is not None:
                        dta_filter_results.append(DTAFilterResult(protein_line, peptide_lines))
                        peptide_lines = []
                        protein_line = None
                    protein_line = ProteinLine.deserialize(line, version=version)

            if file_state == FileState.INFO:
                end_lines.append(line)

    return h_lines, dta_filter_results, end_lines


def write_file(h_lines: [str], dta_filter_results: [DTAFilterResult], end_lines: [str], out_file_path: str, version: str = None) -> None:
    """
    Write Sqt file from hlines and slines
    """

    with open(out_file_path, "w") as file:

        for h_line in h_lines:
            file.write(h_line)
            if h_line[:9] == 'DTASelect':
                if version is None:
                    version = h_line.split(" ")[1].rstrip()
                    print("version: ", version)

        for dta_filter_result in dta_filter_results:
            file.write(dta_filter_result.serialize(version))

        for end_line in end_lines:
            file.write(end_line)


if __name__ == "__main__":

    h_lines, locus_lines, end_lines = read_file("C:\\Users\\Ty\\repos\\senpy_package\\sample_files\\DTASelect-filter.txt")
    print("write")
    write_file(h_lines, locus_lines, end_lines, "tmp_out.dta")

    h_lines, locus_lines, end_lines = read_file("C:\\Users\\Ty\\repos\\senpy_package\\sample_files\\paser_dta_select.txt", version="v2.1.12_paser")
    write_file(h_lines, locus_lines, end_lines, "tmp_out.dta", version="v2.1.12_paser")
