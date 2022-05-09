import argparse
import os.path

from src.senpy.ms2.lines import ILine
from src.senpy.ms2_fast.parser import read_file
from src.senpy.dtaSelectFilter.parser import read_file as parse_filter
from src.senpy.out.line import OutLine
from src.senpy.out.parser import write_file


def parse_args():
    # Parse Arguments
    _parser = argparse.ArgumentParser(description='Arguments for Ms2 Extractor')
    _parser.add_argument('--ms2', required=True, type=str,
                         help='path to ms2 file')
    _parser.add_argument('--filter', required=True, type=str, default=None,
                         help='path to DTASelect-filter file')
    _parser.add_argument('--out', required=False, type=str, default=None,
                         help='path to DTASelect-filter file')

    # Allow for custom ms2 I line keywords
    _parser.add_argument('--retention_time_keyword', required=False, type=str, default=ILine.RETENTION_TIME_KEYWORD,
                         help='I line keyword for retention time')
    _parser.add_argument('--OOK0_keyword', required=False, type=str, default=ILine.OOK0_KEYWORD,
                         help='I line keyword for OOk0')
    _parser.add_argument('--CCS_keyword', required=False, type=str, default=ILine.CCS_KEYWORD,
                         help='I line keyword for CCS')
    _parser.add_argument('--collision_energy_keyword', required=False, type=str, default=ILine.COLLISION_ENERGY_KEYWORD,
                         help='I line keyword for collision energy')
    _parser.add_argument('--precursor_intensity_keyword', required=False, type=str,
                         default=ILine.PRECURSOR_INTENSITY_KEYWORD, help='I line keyword for precursor intensity')
    _parser.add_argument('--OOK0_spectra_keyword', required=False, type=str, default=ILine.OOK0_SPECTRA_KEYWORD,
                         help='I line keyword for OOK0 spectra')
    _parser.add_argument('--CCS_spectra_keyword', required=False, type=str, default=ILine.CCS_SPECTRA_KEYWORD,
                         help='I line keyword for CCS spectra')
    _parser.add_argument('--intensity_spectra_keyword', required=False, type=str,
                         default=ILine.INTENSITY_SPECTRA_KEYWORD, help='I line keyword for intensity spectra')
    _parser.add_argument('--mz_spectra_keyword', required=False, type=str,
                         default=ILine.MZ_SPECTRA_KEYWORD, help='I line keyword for mz spectra')

    return _parser.parse_args()


def generate_output(ms2_path=None,
                    filter_path=None,
                    out_path=None,
                    retention_time_keyword=None,
                    ook0_keyword=None,
                    ccs_keyword=None,
                    collision_energy_keyword=None,
                    precursor_intensity_keyword=None,
                    ook0_spectra_keyword=None,
                    ccs_spectra_keyword=None,
                    intensity_spectra_keyword=None,
                    mz_spectra_keyword=None
                    ):
    ms2_file_name = os.path.basename(ms2_path).split(".ms2")[0]
    print("ms2_file_name: " + ms2_file_name)

    peptide_line_by_scan_number_map = {}
    _, dta_filter_results, _ = parse_filter(filter_path)

    print("DTASelect-filter")
    for filter_result in dta_filter_results:
        for peptide_line in filter_result.peptide_lines:
            if peptide_line.file_name == ms2_file_name:
                peptide_line_by_scan_number_map[peptide_line.low_scan] = peptide_line
    print(len(peptide_line_by_scan_number_map))

    print("MS2")
    out_lines = []
    _, ms2_spectras = read_file(ms2_path)
    for ms2_spectra in ms2_spectras:
        ms2_scan_number = int(ms2_spectra.s_line.get_low_scan())
        if ms2_scan_number in peptide_line_by_scan_number_map:
            peptide_line = peptide_line_by_scan_number_map[ms2_scan_number]

            out_line = OutLine(scan_number=peptide_line.low_scan,
                               sequence=peptide_line.sequence,
                               charge=peptide_line.charge,
                               mass=ms2_spectra.z_line.get_mass(),
                               mz=ms2_spectra.s_line.get_mz(),
                               x_corr=peptide_line.x_corr,
                               retention_time=ms2_spectra.get_retention_time(keyword=retention_time_keyword),
                               OOK0=ms2_spectra.get_ook0(keyword=ook0_keyword),
                               CCS=ms2_spectra.get_ccs(keyword=ccs_keyword),
                               collision_energy=ms2_spectra.get_collision_energy(keyword=collision_energy_keyword),
                               precursor_intensity=ms2_spectra.get_precursor_intensity(
                                   keyword=precursor_intensity_keyword),
                               OOK0_spectra=ms2_spectra.get_ook0_spectra(keyword=ook0_spectra_keyword),
                               CCS_spectra=ms2_spectra.get_ccs_spectra(keyword=ccs_spectra_keyword),
                               intensity_spectra=ms2_spectra.get_mobility_intensity_spectra(
                                   keyword=intensity_spectra_keyword),
                               mz_spectra=ms2_spectra.get_mobility_mz_spectra(keyword=mz_spectra_keyword))

            out_lines.append(out_line)

    write_file(out_lines, out_path)


if __name__ == '__main__':
    args = parse_args()
    if args.out is None:
        args.out = os.path.splitext(args.ms2)[0] + ".out"

    print(args)

    generate_output(args.ms2,
                    args.filter,
                    args.out,
                    retention_time_keyword=args.retention_time_keyword,
                    ook0_keyword=args.OOK0_keyword,
                    ccs_keyword=args.CCS_keyword,
                    collision_energy_keyword=args.collision_energy_keyword,
                    precursor_intensity_keyword=args.precursor_intensity_keyword,
                    ook0_spectra_keyword=args.OOK0_spectra_keyword,
                    ccs_spectra_keyword=args.CCS_spectra_keyword,
                    intensity_spectra_keyword=args.intensity_spectra_keyword,
                    mz_spectra_keyword=args.mz_spectra_keyword
                    )
