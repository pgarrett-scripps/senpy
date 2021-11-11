from senpy.sqt.serializer import SLineSerializer, MLineSerializer, LLineSerializer
from senpy.sqt.lines import SLine

def parse_file(file_path: str) -> ([str], [SLine]):
    """
    Return list of S_lines and H_lines
    """
    h_lines, s_lines = [], []
    with open(file_path) as file:
        for line in file:
            if line[0] == "H":
                h_lines.append(line)
            if line[0] == "S":
                s_lines.append(SLineSerializer.deserialize(line))
            if line[0] == "M":
                s_lines[-1].m_lines.append(MLineSerializer.deserialize(line))
            if line[0] == "L":
                s_lines[-1].m_lines[-1].l_lines.append(LLineSerializer.deserialize(line))
    return h_lines, s_lines

def write_file(h_lines: [str], s_lines: [SLine], out_file_path: str) -> None:
    """
    Write Sqt file from hlines and slines
    """
    with open(out_file_path, "w") as file:

        for h_line in h_lines:
            file.write(h_line)

        for s_line in s_lines:
            file.write(SLineSerializer.serialize(s_line))
            for m_line in s_line.m_lines:
                file.write(MLineSerializer.serialize(m_line))
                for l_line in m_line.l_lines:
                    file.write(LLineSerializer.serialize(l_line))
            file.write("\n")