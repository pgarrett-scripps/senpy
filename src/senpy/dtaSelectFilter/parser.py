from senpy.util import LineSerializer
from senpy.dtaSelectFilter.lines import LocusLine
from senpy.dtaSelectFilter.serializer import UniqueLineSerializer_version_2_1_12, LocusLineSerializer_version_2_1_12, \
    LocusLineSerializer_version_2_1_13, UniqueLineSerializer_version_2_1_13

from enum import Enum


class FileState(Enum):
    HEADER = 1
    DATA = 2
    INFO = 3


def get_unique_line_serializer_by_version(version: str) -> LineSerializer:
    if version == "v2.1.12":
        return UniqueLineSerializer_version_2_1_12
    elif version == "v2.1.13":
        return UniqueLineSerializer_version_2_1_13
    else:
        print("version: ", version)
        raise NotImplementedError


def get_locus_line_serializer_by_version(version: str) -> LineSerializer:
    if version == "v2.1.12":
        return LocusLineSerializer_version_2_1_12
    elif version == "v2.1.13":
        return LocusLineSerializer_version_2_1_13
    else:
        print("version: ", version)
        raise NotImplementedError


def parse_file(dta_select_filter_file_path: str) -> ([str], [LocusLine], [str]):
    """
    Return list of S_lines and H_lines
    """
    h_lines, locus_lines, end_lines = [], [], []
    file_state = FileState.HEADER

    unique_line_serializer = None
    locus_line_serializer = None

    with open(dta_select_filter_file_path) as file:
        for line in file:
            line_elements = line.split("\t")

            # update file state
            if len(line_elements) > 0 and line_elements[0] == 'Unique':
                file_state = FileState.DATA
                continue

            if len(line_elements) > 1 and line_elements[1] == "Proteins":
                file_state = FileState.INFO
                continue

            if file_state == FileState.HEADER:
                h_lines.append(line)
                if line[:9] == 'DTASelect':
                    version = line.split(" ")[1].rstrip()
                    print("version: ", version)
                    unique_line_serializer = get_unique_line_serializer_by_version(version)
                    locus_line_serializer = get_locus_line_serializer_by_version(version)

            if file_state == FileState.DATA:
                if line_elements[0] == '' or line_elements[0] == '*':
                    unique_line = unique_line_serializer.deserialize(line)
                    locus_lines[-1].unique_lines.append(unique_line)
                else:
                    locus_line = locus_line_serializer.deserialize(line)
                    locus_lines.append(locus_line)

            if file_state == FileState.INFO:
                end_lines.append(line)

    return h_lines, locus_lines, end_lines


def write_file(h_lines: [str], locus_lines: [LocusLine], end_lines: [str], out_file_path: str) -> None:
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
            for unique_line in locus_line.unique_lines:
                line = unique_line_serializer.serialize(unique_line)
                file.write(line)

        for end_line in end_lines:
            file.write(end_line)


if __name__ == "__main__":
    h_lines, locus_lines, end_lines = parse_file("/sample_frag_ion\\DTASelect-filter.txt")
    write_file(h_lines, locus_lines, end_lines, "tmp_out.dta")
