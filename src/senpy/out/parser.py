from typing import List

from .line import OutLine


def read_file(file_path: str) -> List[OutLine]:
    """
    Return list of out_lines and H_lines
    """
    out_lines = []
    with open(file_path) as file:
        for i, line in enumerate(file):
            if i == 0:
                continue
            else:
                out_lines.append(OutLine.deserialize(line))
    return out_lines


def write_file(out_lines: [OutLine], out_file_path: str):
    """
    Write out file from h_lines and out_lines
    """
    with open(out_file_path, "w") as file:
        file.write(OutLine.get_header())
        for out_line in out_lines:
            file.write(out_line.serialize())
