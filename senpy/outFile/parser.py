from senpy.outFile.line import OutLine
from senpy.outFile.serializer import OutLineSerializer


def parse_file(file_path):
    """
    Return list of out_lines and H_lines
    """
    h_lines, out_lines = [], []
    with open(file_path) as file:
        for line in file:
            if line[0] == 'S':
                h_lines.append(line)
            else:
                out_line = OutLineSerializer.deserialize(line)
                out_lines.append(out_line)

    return h_lines, out_lines


def write_file(h_lines: [str], out_lines: [OutLine], out_file_path: str):
    """
    Write out file from h_lines and out_lines
    """
    with open(out_file_path, "w") as file:
        for h_line in h_lines:
            file.write(h_line)
        for out_line in out_lines:
            file.write(OutLineSerializer.serialize(out_line))
