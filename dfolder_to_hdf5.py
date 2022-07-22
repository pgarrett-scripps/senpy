import argparse
import os
from tqdm import tqdm
import h5py
import numpy as np

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

    # add the command line args from the stream-engine
    return _parser.parse_args()


def make_hdf5_file(analysis_dir):

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

    peak_dt = [
        ("mz_array", np.float64),
        ("intensity_array", np.float32),
    ]

    precursor_dt = [
        ("n_peaks", np.int32),
        ("scan_id", np.int32),
        ("mz", np.float64),
        ("charge", np.int8),
        ("rt", np.float32),
        ("ce", np.float32),
        ("ook0", np.float32),
        ("ccs", np.float32),
        ("prec_id", np.int32),
        ("prec_parent_id", np.int32),
        ("iso_mz", np.float64),
        ("iso_width", np.float32),
        ("intensity", np.float64),
        ("scan_num_begin", np.float32),
        ("scan_num_end", np.float32)
    ]

    spectras, precursors = [], []
    for item in tqdm(precursors_table_items):

        if item.monoisotopic_mz is None or item.charge is None:
            continue

        precursor_pasef_frame_msms_info_item = precursor_to_pasef_frame_msms_info_map[item.id]
        scan_id = ms2_scan_map[item.parent_frame][item.id]
        ook0 = td.scanNumToOneOverK0(item.parent_frame, [item.scan_number])[0]
        ccs = oneOverK0ToCCSforMz(ook0, item.charge, item.monoisotopic_mz)

        msms_spectra = td.readPasefMsMs([item.id])
        n_peaks = len(msms_spectra[item.id][0])
        spectra = np.zeros(n_peaks, dtype=peak_dt)
        spectra["mz_array"] = msms_spectra[item.id][0]
        spectra["intensity_array"] = msms_spectra[item.id][1]
        spectras.append(spectra)

        precursor = np.zeros(1, dtype=precursor_dt)
        precursor["n_peaks"] = len(spectra)
        precursor["scan_id"] = scan_id
        precursor["mz"] = item.monoisotopic_mz
        precursor["charge"] = item.charge
        precursor["rt"] = frame_table_items[item.parent_frame - 1].time
        precursor["ce"] = precursor_pasef_frame_msms_info_item.collision_energy
        precursor["ook0"] = ook0
        precursor["ccs"] = ccs
        precursor["prec_id"] = item.id
        precursor["prec_parent_id"] = item.parent_frame
        precursor["iso_mz"] = precursor_pasef_frame_msms_info_item.isolation_mz
        precursor["iso_width"] = precursor_pasef_frame_msms_info_item.isolation_width
        precursor["intensity"] = item.intensity
        precursor["scan_num_begin"] = precursor_pasef_frame_msms_info_item.scan_number_begin
        precursor["scan_num_end"] = precursor_pasef_frame_msms_info_item.scan_number_end
        precursors.append(precursor)


    hdf5_file = os.path.join(analysis_dir, os.path.basename(analysis_dir).split('.')[0] + '.hdf5')
    with h5py.File(hdf5_file, 'w') as f:
        f.create_dataset('spectra', data=np.concatenate(spectras), dtype=peak_dt)
        f.create_dataset('precursor', data=precursors, dtype=precursor_dt)

if __name__ == '__main__':
    args = parse_args()
    make_hdf5_file(args.analysis_dir)
