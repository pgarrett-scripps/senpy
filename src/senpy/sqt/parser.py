from .lines import SLine, parse_sqt_line, MLine, LLine
from ..util import HLine


def read_file(file_path: str, version='auto') -> ([str], [SLine]):
    """
    Return list of H_lines and S_lines, from provided sqt file. Will always
    return correctly and fully read Precursors/PSMCandidates/Locus' until
    eof or corrupted line is reached. Errors are logged accordingly and not
    thrown outside this function to preserve robustness.
    :param:     file_path:          str to the path for the sqt file
    :return:    ([str], [SLine]):   lists of Hlines and SLines
    """
    h_lines, s_lines = [], []

    with open(file_path) as file:
        for line in file:

            if line == "" or line == "\n":
                continue

            sqt_line = parse_sqt_line(line)
            if isinstance(sqt_line, HLine):
                h_lines.append(sqt_line)
            elif isinstance(sqt_line, SLine):
                s_lines.append(sqt_line)
            elif isinstance(sqt_line, MLine):
                s_lines[-1].m_lines.append(sqt_line)
            elif isinstance(sqt_line, LLine):
                s_lines[-1].m_lines[-1].l_lines.append(sqt_line)

        return h_lines, s_lines


def write_file(h_lines: [HLine], s_lines: [SLine], out_file_path: str, version='auto') -> None:
    """
    Write Sqt file from hlines and slines
    :param:     h_lines:    [str],      list of header lines
    :param:     s_lines:    [SLine],    list of SLines
    :param:     out_file_path   str,    string to the sqt output file path
    """
    with open(out_file_path, "w") as file:

        for h_line in h_lines:
            file.write(h_line.serialize(version=version))

        for s_line in s_lines:
            file.write(s_line.serialize(version=version))
            for m_line in s_line.m_lines:
                file.write(m_line.serialize(version=version))
                for l_line in m_line.l_lines:
                    file.write(l_line.serialize(version=version))
            file.write("\n")
