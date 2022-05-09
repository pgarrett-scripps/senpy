import argparse
import os

from src.senpy.ms2_fast.parser import read_file


def parse_args():
    # Parse Arguments
    _parser = argparse.ArgumentParser(description='Arguments for Ms2 Extractor')
    _parser.add_argument('--ms2', required=True, type=str,
                         help='path to ms2 file')
    _parser.add_argument('--out', required=False, type=str,
                         help='output file')

    return _parser.parse_args()

def main(ms2_path, out_path):
    ms2_file_name = os.path.basename(ms2_path).split(".ms2")[0]
    print("ms2_file_name: " + ms2_file_name)

    lines = []
    _, ms2_spectras = read_file(ms2_path)
    for ms2_spectra in ms2_spectras:
        ms2_scan_number = int(ms2_spectra.s_line.get_low_scan())
        precursor_id = int(ms2_spectra.get_precursor_id())
        line = '\t'.join([str(ms2_scan_number), str(precursor_id)]) + '\n'
        lines.append(line)

    with open(out_path, "w") as file:
        file.write(''.join(lines))


if __name__ == '__main__':
    args = parse_args()
    if args.out is None:
        args.out = args.ms2 + ".sn2p"

    print(args)

    main(args.ms2, args.out)