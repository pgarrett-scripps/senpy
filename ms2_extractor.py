import argparse
import os
import time

from tqdm import tqdm

from src.senpy.d_folder.tables import get_frame_table_items
from src.senpy.d_folder.tables import get_pasef_frame_msms_table_items
from src.senpy.d_folder.tables import get_precursors_table_items
from src.senpy.d_folder.timsdata import TimsData, oneOverK0ToCCSforMz
from src.senpy.d_folder.timstof_utils import build_precursor_to_mobility_spectra_map, \
    build_frame_id_ms1_scan_map, build_parent_id_to_precursors_map

from src.senpy.ms2.lines import Ms2Spectra, ILine

PROTON_MASS = 1.007276466
VERSION = '0.0.1'

def parse_args():
    # Parse Arguments
    _parser = argparse.ArgumentParser(description='Arguments for Ms2 Extractor')
    _parser.add_argument('--analysis_dir', required=True, type=str,
                         help='path_to_analysis_dir')
    _parser.add_argument('--output_ms2_path', required=False, type=str, default=None,
                         help='absolute path for output ms2 file')
    _parser.add_argument('--include_mobility_spectra', action='store_true',
                         help='include complete mobility spectra in I lines')
    _parser.add_argument('--mobility_spectra_ppm', required=False, type=int, default=15,
                         help='ppm to use for identifying precursor ion')
    _parser.add_argument('--skip_spectra', action='store_true',
                         help='skip msms spectra')

    _parser.add_argument('--ook0_keyword', required=False, type=str, help='keyword for ook0')
    _parser.add_argument('--ccs_keyword', required=False, type=str, help='keyword for ccs')
    _parser.add_argument('--parent_id_keyword', required=False, type=str, help='keyword for parent id')
    _parser.add_argument('--precursor_id_keyword', required=False, type=str, help='keyword for precursor id')
    _parser.add_argument('--retention_time_keyword', required=False, type=str, help='keyword for retention time')
    _parser.add_argument('--collision_energy_keyword', required=False, type=str, help='keyword for collision energy')
    _parser.add_argument('--isolation_mz_keyword', required=False, type=str, help='keyword for isolation mz')
    _parser.add_argument('--isolation_width_keyword', required=False, type=str, help='keyword for isolation width')
    _parser.add_argument('--scan_number_begin_keyword', required=False, type=str, help='keyword for scan number begin')
    _parser.add_argument('--scan_number_end_keyword', required=False, type=str, help='keyword for scan number end')
    _parser.add_argument('--precursor_intensity_keyword', required=False, type=str,
                         help='keyword for precursor intensity')
    _parser.add_argument('--ook0_spectra_keyword', required=False, type=str, help='keyword for ook0 spectra')
    _parser.add_argument('--ccs_spectra_keyword', required=False, type=str, help='keyword for ccs spectra')
    _parser.add_argument('--mz_spectra_keyword', required=False, type=str, help='keyword for mobility mz spectra')
    _parser.add_argument('--intensity_spectra_keyword', required=False, type=str,
                         help='keyword for mobility intensity spectra')

    # add the command line args from the stream-engine
    return _parser.parse_args()


def get_ms2_header(version, ppm, last_scan):
    ms2_header = 'H\tExtractor\tTimsTOF_extractor\n' \
                 'H\tExtractorVersion\t{}\n' \
                 'H\tPublicationDate\t20-02-2020\n' \
                 'H\tComments\tTimsTOF_extractor written by Yu Gao, 2018\n' \
                 'H\tComments\tTimsTOF_extractor modified by Titus Jung, 2019\n' \
                 'H\tComments\tTimsTOF_extractor modified by Patrick Garrett, 2022\n' \
                 'H\tExtractorOptions\tMSn\n' \
                 'H\tAcquisitionMethod\tData-Dependent\n' \
                 'H\tInstrumentType\tTIMSTOF\n' \
                 'H\tDataType\tCentroid\n' \
                 'H\tScanType\tMS2\n' \
                 'H\tResolution\n' \
                 'H\tFeature Extraction Resolution: {}ppm\n' \
                 'H\tIsolationWindow\n' \
                 'H\tFirstScan\t1\n' \
                 'H\tLastScan\t{}\n' \
                 'H\tMonoIsotopic PrecMz\tTrue\n'.format(version, ppm, last_scan)
    return ms2_header


def extract_ms2_file(analysis_dir: str,
                     output_file: str = None,
                     include_mobility_spectra: bool = False,
                     ppm: int = 15,
                     skip_spectra: bool = False
                     ):

    if output_file is None:
        output_file = os.path.join(analysis_dir, os.path.basename(analysis_dir).split('.')[0] + '.ms2')

        if skip_spectra:
            output_file += ".index"

    print(f"analysis_dir: {analysis_dir}")
    print(f"output_file: {output_file}")

    td = TimsData(analysis_dir)
    conn = td.conn

    with conn:
        pasef_frame_msms_table_items = get_pasef_frame_msms_table_items(conn)
        frame_table_items = get_frame_table_items(conn)
        precursors_table_items = get_precursors_table_items(conn)

    max_scan_number = int(frame_table_items[0].num_scans)
    precursor_to_pasef_frame_msms_info_map = {item.precursor_id: item for item in pasef_frame_msms_table_items}

    precursor_map = build_parent_id_to_precursors_map(precursors_table_items)
    frame_id_ms1_scan_map, ms2_scan_map = build_frame_id_ms1_scan_map(precursor_map, frame_table_items)

    spectra_dict = None
    if include_mobility_spectra:
        print('----- Extracting Mobility Spectra -----')
        spectra_dict = build_precursor_to_mobility_spectra_map(precursors_table_items, td, max_scan_number, ppm)

    print('----- Generating Ms2 File -----')
    ms2_header = get_ms2_header(version=VERSION, ppm=ppm, last_scan=len(pasef_frame_msms_table_items))
    with open(output_file, 'w') as out_file:
        out_file.write(ms2_header)
        for item in tqdm(precursors_table_items):

            if item.monoisotopic_mz is None or item.charge is None:
                continue

            precursor_mass = (item.monoisotopic_mz * item.charge) - (item.charge - 1) * PROTON_MASS
            precursor_pasef_frame_msms_info_item = precursor_to_pasef_frame_msms_info_map[item.id]
            scan_id = ms2_scan_map[item.parent_frame][item.id]
            ook0 = td.scanNumToOneOverK0(item.parent_frame, [item.scan_number])[0]
            ccs = oneOverK0ToCCSforMz(ook0, item.charge, item.monoisotopic_mz)

            spectra_mz_array = []
            spectra_intensity_array = []
            if not skip_spectra:
                msms_spectra = td.readPasefMsMs([item.id])
                spectra_mz_array = msms_spectra[item.id][0]
                spectra_intensity_array = msms_spectra[item.id][1]

            if not skip_spectra and len(spectra_mz_array) == 0:
                continue

            info_dict = {
                 ILine.PARENT_ID_KEYWORD: f"{item.parent_frame}",
                 ILine.PRECURSOR_ID_KEYWORD: f"{item.id}",
                 ILine.OOK0_KEYWORD: f"{ook0:.4f}",
                 ILine.CCS_KEYWORD: f"{ccs:.4f}",
                 ILine.RETENTION_TIME_KEYWORD: f"{frame_table_items[item.parent_frame].time:.4f}",
                 ILine.COLLISION_ENERGY_KEYWORD: f"{precursor_pasef_frame_msms_info_item.collision_energy:.4f}",
                 ILine.ISOLATION_MZ_KEYWORD: f"{precursor_pasef_frame_msms_info_item.isolation_mz:.4f}",
                 ILine.ISOLATION_WIDTH_KEYWORD: f"{precursor_pasef_frame_msms_info_item.isolation_width:.4f}",
                 ILine.SCAN_NUMBER_BEGIN_KEYWORD: f"{precursor_pasef_frame_msms_info_item.scan_number_begin:.4f}",
                 ILine.SCAN_NUMBER_END_KEYWORD: f"{precursor_pasef_frame_msms_info_item.scan_number_end:.4f}",
                 ILine.PRECURSOR_INTENSITY_KEYWORD: f"{item.intensity:.4f}"
            }

            if include_mobility_spectra:
                ook0_spectra = td.scanNumToOneOverK0(item.parent_frame, spectra_dict[item.id].scan_numbers)
                mz_list = td.indexToMz(item.parent_frame, spectra_dict[item.id].indexes)
                ccs_spectra = [oneOverK0ToCCSforMz(val, item.charge, item.monoisotopic_mz) for val in ook0_spectra]
                intensity_list = spectra_dict[item.id].intensities

                info_dict[ILine.OOK0_SPECTRA_KEYWORD] = str([round(val, 4) for val in ook0_spectra])
                info_dict[ILine.CCS_SPECTRA_KEYWORD] = str([round(val, 4) for val in ccs_spectra])
                info_dict[ILine.MZ_SPECTRA_KEYWORD] = str([round(val, 4) for val in mz_list])
                info_dict[ILine.INTENSITY_SPECTRA_KEYWORD] = str([round(val, 1) for val in intensity_list])

            precursor_spectra = Ms2Spectra.create(low_scan=scan_id,
                                                  high_scan=scan_id,
                                                  mz=item.monoisotopic_mz,
                                                  charge=item.charge,
                                                  mass=precursor_mass,
                                                  mz_spectra=spectra_mz_array,
                                                  intensity_spectra=spectra_intensity_array,
                                                  info_dict=info_dict)

            out_file.write(precursor_spectra.serialize())

    print("Done!")


if __name__ == '__main__':
    args = parse_args()

    # Update the keywords for I Lines
    if args.ook0_keyword:
        ILine.OOK0_KEYWORD = args.ook0_keyword
    if args.ccs_keyword:
        ILine.CCS_KEYWORD = args.ccs_keyword
    if args.parent_id_keyword:
        ILine.PARENT_ID_KEYWORD = args.parent_id_keyword
    if args.precursor_id_keyword:
        ILine.PRECURSOR_ID_KEYWORD = args.precursor_id_keyword
    if args.retention_time_keyword:
        ILine.RETENTION_TIME_KEYWORD = args.retention_time_keyword
    if args.collision_energy_keyword:
        ILine.COLLISION_ENERGY_KEYWORD = args.collision_energy_keyword
    if args.isolation_mz_keyword:
        ILine.ISOLATION_MZ_KEYWORD = args.isolation_mz_keyword
    if args.isolation_width_keyword:
        ILine.ISOLATION_WIDTH_KEYWORD = args.isolation_width_keyword
    if args.scan_number_begin_keyword:
        ILine.SCAN_NUMBER_BEGIN_KEYWORD = args.scan_number_begin_keyword
    if args.scan_number_end_keyword:
        ILine.SCAN_NUMBER_END_KEYWORD = args.scan_number_end_keyword
    if args.precursor_intensity_keyword:
        ILine.PRECURSOR_INTENSITY_KEYWORD = args.precursor_intensity_keyword
    if args.ook0_spectra_keyword:
        ILine.OOK0_SPECTRA_KEYWORD = args.ook0_spectra_keyword
    if args.ccs_spectra_keyword:
        ILine.CCS_SPECTRA_KEYWORD = args.ccs_spectra_keyword
    if args.mz_spectra_keyword:
        ILine.MZ_SPECTRA_KEYWORD = args.mz_spectra_keyword
    if args.intensity_spectra_keyword:
        ILine.INTENSITY_SPECTRA_KEYWORD = args.intensity_spectra_keyword

    extract_ms2_file(args.analysis_dir,
                     output_file=args.output_ms2_path,
                     include_mobility_spectra=args.include_mobility_spectra,
                     ppm=args.mobility_spectra_ppm,
                     skip_spectra=args.skip_spectra
                     )
