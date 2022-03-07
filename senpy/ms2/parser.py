from senpy.ms2.lines import SLine
from senpy.ms2.serializer import SLineSerializer, ILineSerializer, ZLineSerializer, PeakLineSerializer

def read_file(file_path) -> ([str], [SLine]):
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

            if line[0] == 'H':
                h_lines.append(line)
            elif line[0] == 'S':
                if len(s_lines) > 0: # convert peak list to np array
                    s_lines[-1].convert_peak_list_to_arr()
                s_lines.append(SLineSerializer.deserialize(line))
            elif line[0] == 'I':
                s_lines[-1].i_lines.append(ILineSerializer.deserialize(line))
            elif line[0] == 'Z':
                s_lines[-1].z_line = ZLineSerializer.deserialize(line)
            else:
                s_lines[-1].peak_lines.append(PeakLineSerializer.deserialize(line))

        return h_lines, s_lines


def read_file_incrementally(file_path) -> SLine:
    """
    Return S_lines incrementally, from provided sqt file. Will always
    return correctly and fully read Precursors/PSMCandidates/Locus' until
    eof or corrupted line is reached. Errors are logged accordingly and not
    thrown outside this function to preserve robustness.
    :param:     file_path:          str to the path for the sqt file
    :return:    ([SLine]):          lists of SLines
    """

    h_lines, s_lines = [], []

    with open(file_path) as file:
        s_line = None
        for line in file:

            if line[0] == 'H':
                h_lines.append(line)
            elif line[0] == 'S':
                if s_line: # convert peak list to np array
                    s_line.convert_peak_list_to_arr()
                    yield s_line
                s_line = SLineSerializer.deserialize(line)
            elif line[0] == 'I':
                s_line.i_lines.append(ILineSerializer.deserialize(line))
            elif line[0] == 'Z':
                s_line.z_line = ZLineSerializer.deserialize(line)
            else:
                s_line.peak_lines.append(PeakLineSerializer.deserialize(line))
        return s_line


def write_file(h_lines: [str], s_lines: [SLine], out_file_path: str) -> None:
    """
    Write Ms2 file from hlines and slines
    :param:     h_lines:    [str],      list of header lines
    :param:     s_lines:    [SLine],    list of SLines
    :param:     out_file_path   str,    string to the ms2 output file path
    """
    with open(out_file_path, "w") as file:

        for h_line in h_lines:  # Write header lines
            file.write(h_line)

        for s_line in s_lines:  # Write S lines
            file.write(SLineSerializer.serialize(s_line))
            for i_line in s_line.i_lines:  # Write I lines
                file.write(ILineSerializer.serialize(i_line))
            file.write(ZLineSerializer.serialize(s_line.z_line))  # Write z line
            for peak_line in s_line.peak_lines:  # Write peak lines
                file.write(PeakLineSerializer.serialize(peak_line))


def write_file_incrementally(h_lines: [str], s_lines: [SLine], out_file: File) -> None:
    """
    Write Ms2 file from hlines and slines
    :param:     h_lines:    [str],      list of header lines
    :param:     s_lines:    [SLine],    list of SLines
    :param:     out_file_path   str,    string to the ms2 output file path
    """
    for h_line in h_lines:  # Write header lines
        out_file.write(h_line)

    for s_line in s_lines:  # Write S lines
        out_file.write(SLineSerializer.serialize(s_line))
        for i_line in s_line.i_lines:  # Write I lines
            file.write(ILineSerializer.serialize(i_line))
        out_file.write(ZLineSerializer.serialize(s_line.z_line))  # Write z line
        for peak_line in s_line.peak_lines:  # Write peak lines
            out_file.write(PeakLineSerializer.serialize(peak_line))


