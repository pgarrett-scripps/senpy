from senpy.dtaSelectFilter.lines import ProteinLine, DTAFilterResult, PeptideLine
from enum import Enum


class FileState(Enum):
    HEADER = 1
    DATA = 2
    INFO = 3


def parse_file(dta_select_filter_file_path: str) -> [DTAFilterResult]:
    """
    Return list of FilteredProteinResult's
    """
    dta_filter_results = []
    file_state = FileState.HEADER
    version = None

    protein_line = None
    peptide_lines = []

    with open(dta_select_filter_file_path) as file:
        for line in file:
            line_elements = line.split("\t")

            # update file state
            if len(line_elements) > 0 and line_elements[0] == 'Unique':
                file_state = FileState.DATA
                continue

            if len(line_elements) > 1 and line_elements[1] == "Proteins":
                dta_filter_results.append(DTAFilterResult(protein_line, peptide_lines))
                file_state = FileState.INFO
                continue

            if file_state == FileState.HEADER:
                if line[:9] == 'DTASelect':
                    version = line.split(" ")[1].rstrip()
                    print("version: ", version)

            if file_state == FileState.DATA:
                if line_elements[0] == '' or line_elements[0] == '*':
                    peptide_lines.append(PeptideLine.deserialize(line, version=version))
                else:
                    if protein_line is not None:
                        dta_filter_results.append(DTAFilterResult(protein_line, peptide_lines))
                        peptide_lines = []
                    protein_line = ProteinLine.deserialize(line, version=version)

            if file_state == FileState.INFO:
                continue

    return dta_filter_results


def write_file(h_lines: [str], locus_lines: [ProteinLine], end_lines: [str], out_file_path: str) -> None:
    """
    Write Sqt file from hlines and slines
    """
    unique_line_serializer = None
    locus_line_serializer = None
    with open(out_file_path, "w") as file:
        for h_line in h_lines:
            file.write(h_line)
            if h_line[:9] == 'DTASelect':
                version = h_line.split(" ")[1].rstrip()
                unique_line_serializer = get_unique_line_serializer_by_version(version)
                locus_line_serializer = get_locus_line_serializer_by_version(version)

        for locus_line in locus_lines:
            line = locus_line_serializer.serialize(locus_line)
            file.write(line)
            for unique_line in locus_line.peptide_lines:
                line = unique_line_serializer.serialize(unique_line)
                file.write(line)

        for end_line in end_lines:
            file.write(end_line)


if __name__ == "__main__":
    h_lines, locus_lines, end_lines = parse_file("/sample_frag_ion\\DTASelect-filter.txt")
    write_file(h_lines, locus_lines, end_lines, "tmp_out.dta")
