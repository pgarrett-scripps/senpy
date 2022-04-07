from typing import List

from tqdm import tqdm

from senpy.ms2_fast.lines import SLine, HLine, ZLine, PeakLine, ILine, Ms2Spectra, parse_ms2_line


def read_file(file_path) -> (List[HLine], List[Ms2Spectra]):
    """
    Return HLines and Ms2Spectra, from provided ms2 file. Will always
    return correctly and fully read ms2 file until eof or corrupted line is reached.
    :param:     file_path:          str to the path for the sqt file
    :return:    (List[HLine], List[Ms2Spectra]):          lists of HLines and Ms2Spectra
    """
    h_lines, ms2_spectras = [], []

    with open(file_path) as file:
        s_line, z_line, i_lines, peak_lines = None, None, [], []
        for line in tqdm(file):
            if line == "" or line == "\n":
                continue
            ms2_line = parse_ms2_line(line)
            if isinstance(ms2_line, HLine):
                h_lines.append(ms2_line)
                continue
            elif isinstance(ms2_line, SLine):
                if s_line is not None:
                    ms2_spectras.append(Ms2Spectra(s_line=s_line,
                                                   z_line=z_line,
                                                   i_lines=i_lines,
                                                   peak_lines=peak_lines
                                                   )
                                        )
                    s_line, z_line, i_lines, peak_lines = None, None, [], []
                s_line = ms2_line
            elif isinstance(ms2_line, ILine):
                i_lines.append(ms2_line)
            elif isinstance(ms2_line, ZLine):
                z_line = ms2_line
            elif isinstance(ms2_line, PeakLine):
                #peak_lines.append(ms2_line)
                pass

        ms2_spectras.append(Ms2Spectra(s_line=s_line,
                                       z_line=z_line,
                                       i_lines=i_lines,
                                       peak_lines=peak_lines
                                       )
                            )

        return h_lines, ms2_spectras


def read_file_incrementally(file_path) -> List[Ms2Spectra]:
    """
    Return Ms2Spectra incrementally, from provided ms2 file. Will always
    return correctly and fully read ms2 file until eof or corrupted line is reached.
    :param:     file_path:          str to the path for the sqt file
    :return:    List[Ms2Spectra]:          lists of SLines
    """

    with open(file_path) as file:
        s_line, z_line, i_lines, peak_lines = None, None, [], []
        for line in file:
            ms2_line = parse_ms2_line(line)
            if isinstance(ms2_line, HLine):
                continue
            elif isinstance(ms2_line, SLine):
                if s_line is not None:
                    yield Ms2Spectra(s_line=s_line,
                                     z_line=z_line,
                                     i_lines=i_lines,
                                     peak_lines=peak_lines
                                     )

                    s_line, z_line, i_lines, peak_lines = None, None, [], []
                s_line = ms2_line
            elif isinstance(ms2_line, ILine):
                i_lines.append(ms2_line)
            elif isinstance(ms2_line, ZLine):
                z_line = ms2_line
            elif isinstance(ms2_line, PeakLine):
                #peak_lines.append(ms2_line)
                pass

        yield Ms2Spectra(s_line=s_line,
                          z_line=z_line,
                          i_lines=i_lines,
                          peak_lines=peak_lines
                          )

        return


def write_file(h_lines: List[HLine], ms2_spectras: List[Ms2Spectra], out_file_path: str) -> None:
    """
    Write Ms2 file from HLines and Ms2Spectra
    :param:     h_lines:    [HLine],      list of header lines
    :param:     ms2_spectras:    [Ms2Spectra],    ms2_spectras
    :param:     out_file_path   str,    string to the ms2 output file path
    """
    with open(out_file_path, "w") as file:

        for h_line in h_lines:  # Write header lines
            file.write(h_line.serialize())

        for i, ms2_spectra in enumerate(ms2_spectras):
            ms2_spectra_str = ms2_spectra.serialize()
            if i == len(ms2_spectras) - 1:  # remove final newline
                ms2_spectra_str = ms2_spectra_str.rstrip()
            file.write(ms2_spectra_str)
