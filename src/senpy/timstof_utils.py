from dataclasses import dataclass, field
from typing import Dict, List

from tqdm import tqdm
import numpy as np
import math

from senpy.tdf_tables.frames import FramesTableItem
from senpy.tdf_tables.precursors import PrecursorsTableItem


def find_nearest_idx(array, value):
    """
    Returns the index for the item in array value is closest to value
    """
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx - 1]) < math.fabs(value - array[idx])):
        return idx - 1
    else:
        return idx


def build_parent_id_to_precursors_map(precursors_table_items: [PrecursorsTableItem]) -> Dict[int, List[PrecursorsTableItem]]:
    parent_id_to_precursors_map = {}
    for item in precursors_table_items:
        parent_id_to_precursors_map.setdefault(item.parent_frame, [])
        parent_id_to_precursors_map[item.parent_frame].append(item)
    return parent_id_to_precursors_map


def build_precursor_id_to_scan_number_map(precursors_table_items: [PrecursorsTableItem]) -> Dict[int, int]:
    """
    Assigns each precursor a scan number.
    scan number = (number of previous ms1_frames)+(number of previous precursors)

    :param precursors_table_items: list of PrecursorsTableItem's
    :return: dict which maps precursor id to scan number
    """
    precursor_id_to_scan_number_map = {}

    parent_frames = set()
    for precursor_number, item in enumerate(precursors_table_items, 1):
        parent_frames.add(item.parent_frame)
        precursor_id_to_scan_number_map[item.id] = len(parent_frames) + precursor_number
    return precursor_id_to_scan_number_map


def build_frame_id_ms1_scan_map(precursor_map: Dict[int, List[PrecursorsTableItem]], all_ms1_list: List[FramesTableItem]):
    frame_id_ms1_scan_map = {}
    ms2_map = {}
    prev_scan = 0
    for frame_table_item in all_ms1_list:
        frame_id = frame_table_item.id
        prev_scan += 1
        frame_id_ms1_scan_map[frame_id] = prev_scan
        if frame_id in precursor_map:
            if frame_id not in ms2_map:
                ms2_map[frame_id] = {}
            for count, precursor_table_item in enumerate(precursor_map[frame_id], prev_scan+1):
                prec_id = precursor_table_item.id
                ms2_map[frame_id][prec_id] = count
            prev_scan += len(precursor_map[frame_id])
    return frame_id_ms1_scan_map, ms2_map


@dataclass
class MobilitySpectraItem:
    indexes: [] = field(default_factory=list)
    intensities: [] = field(default_factory=list)
    scan_numbers: [] = field(default_factory=list)


def build_precursor_to_mobility_spectra_map(precursors_table_items: List[PrecursorsTableItem], td: 'TimsData',
                                            max_scan_number: int, ppm: int) -> Dict[int, MobilitySpectraItem]:
    """
    Process precursors by ms1 frames to reduce number of TimsData calls. This function loops over
    all the Tof pushes within the ms1 frame and looks for the presence of a precursor ion within a given ppm

    :param precursors_table_items: list of PrecursorTableItems
    :param td: tTimsData object
    :param max_scan_number: max scan number in the ms1 frames
    :param ppm: precursor mass tolerance for mapping precursor m/z to peaks found in tof frames
    :return: dict which maps precursor_id to mobility spectra information
    """

    ms1_frame_to_precursors_map = build_parent_id_to_precursors_map(precursors_table_items)

    precursor_mobility_spectra_dict = {}
    # precursor dict will contain matched ion mobilities within ppm
    for frame, precursor_frame_items in tqdm(ms1_frame_to_precursors_map.items()):

        precursor_frame_items = [item for item in precursor_frame_items if item.charge]
        precursor_ids = [item.id for item in precursor_frame_items]
        precursor_mzs = [item.monoisotopic_mz for item in precursor_frame_items]

        if len(precursor_ids) == 0:
            continue

        # Determine index cutoff for each precursor (according to ppm tolerance)
        # (it is costly to convert between index and mz space)
        ppm_multiplier = ppm / 1_000_000
        min_index_list = td.mzToIndex(frame, [mz - mz * ppm_multiplier for mz in precursor_mzs])
        max_index_list = td.mzToIndex(frame, [mz + mz * ppm_multiplier for mz in precursor_mzs])
        index_list = td.mzToIndex(frame, precursor_mzs)

        tof_scan_data = td.readScansByNumber(frame, 0, max_scan_number)
        for precursor_id, precursor_index, min_index, max_index in zip(precursor_ids, index_list, min_index_list,
                                                                       max_index_list):

            mobility_spectra_item = MobilitySpectraItem()

            # build frame precursor search
            for scan_number, (indexes, intensities) in enumerate(tof_scan_data):

                if len(indexes) == 0:
                    continue

                min_tof_index, max_tof_index = indexes[0], indexes[-1]

                if min_index > max_tof_index or max_index < min_tof_index:
                    continue

                closest_index_idx = find_nearest_idx(indexes, precursor_index)
                if min_index <= indexes[closest_index_idx] <= max_index:
                    mobility_spectra_item.indexes.append(indexes[closest_index_idx])
                    mobility_spectra_item.intensities.append(intensities[closest_index_idx])
                    mobility_spectra_item.scan_numbers.append(scan_number)

            precursor_mobility_spectra_dict[precursor_id] = mobility_spectra_item

    return precursor_mobility_spectra_dict
