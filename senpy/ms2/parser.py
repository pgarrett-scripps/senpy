from senpy.ms2.lines import SLine
from senpy.ms2.serializer import SLineSerializer, ILineSerializer, ZLineSerializer, PeakLineSerializer

def parse_file(file_path) -> ([str], [SLine]):
    """
    Parse ms2 file into h_lines and s_lines
    :param file_path: ms2 file
    :return: h_lines: [str], s_lines: [SLine]
    """
    h_lines, s_lines = [], []

    with open(file_path) as file:
        s_line = None
        for line in file:

            if line[0] == 'H':
                h_lines.append(line)

            elif line[0] == 'S':
                if s_line is not None:
                    s_line.convert_peak_list_to_arr()

                s_line = SLineSerializer.deserialize(line)
                s_lines.append(s_line)

            elif line[0] == 'I':
                i_line = ILineSerializer.deserialize(line)
                s_line.i_lines.append(i_line)

            elif line[0] == 'Z':
                z_line = ZLineSerializer.deserialize(line)
                s_line.z_line = z_line

            else:  # Peak Line
                peak_line = PeakLineSerializer.deserialize(line)
                s_line.peak_lines.append(peak_line)

        return h_lines, s_lines


def parse_file_incremental(file_path) -> ([str], [SLine]):
    """
    Parse ms2 file into h_lines and s_lines
    :param file_path: ms2 file
    :return: h_lines: [str], s_lines: [SLine]
    """

    with open(file_path) as file:
        s_line = None
        for line in file:

            if line[0] == 'H':
                continue

            elif line[0] == 'S':
                if s_line is not None:
                    s_line.convert_peak_list_to_arr()
                    yield s_line

                s_line = SLineSerializer.deserialize(line)

            elif line[0] == 'I':
                i_line = ILineSerializer.deserialize(line)
                s_line.i_lines.append(i_line)

            elif line[0] == 'Z':
                z_line = ZLineSerializer.deserialize(line)
                s_line.z_line = z_line

            else:  # Peak Line
                peak_line = PeakLineSerializer.deserialize(line)
                s_line.peak_lines.append(peak_line)

        return s_line


def write_file(h_lines: [str], s_lines: [SLine], out_file_path: str) -> None:
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