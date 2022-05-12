import argparse
import os
import time

from src.senpy.ms2.fast_parser import read_file as read_file_fast
from src.senpy.ms2.fast_parser import write_file as write_file_fast
from src.senpy.ms2.parser import read_file


def parse_args():
    # Parse Arguments
    _parser = argparse.ArgumentParser(description='Arguments for Ms2 Extractor')
    _parser.add_argument('--ms2_path', required=True, type=str, help='path to ms2 file')
    _parser.add_argument('--ms2_index_path', required=True, type=str, help='path to ms2.index file')
    return _parser.parse_args()


def main(ms2_path, index_path):
    _, ms2_spectras = read_file(ms2_path)
    _, ms2_index_spectras = read_file_fast(index_path)

    precursor_id_to_peak_lines_map = {}
    for ms2_spectra in ms2_spectras:
        prec_id = int(ms2_spectra.get_precursor_id())
        precursor_id_to_peak_lines_map[prec_id] = ms2_spectra.peak_lines

    for ms2_index_spectra in ms2_index_spectras:
        prec_id = int(ms2_index_spectra.get_precursor_id())
        if prec_id in precursor_id_to_peak_lines_map:
            ms2_index_spectra.peak_lines = precursor_id_to_peak_lines_map[prec_id]

    os.rename(ms2_path, ms2_path + ".bak")
    time.sleep(5)
    write_file_fast(_, ms2_index_spectras, ms2_path)


if __name__ == '__main__':
    args = parse_args()
    main(ms2_path=args.ms2_path, index_path=args.ms2_index_path)