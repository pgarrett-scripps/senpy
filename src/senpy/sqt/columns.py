from enum import Enum


class LLineColumns(Enum):
    letter = 0
    locus_name = 1
    peptide_index_in_protein_sequence = 2
    peptide_sequence = 3


class MLineColumns(Enum):
    letter = 0
    xcorr_rank = 1
    sp_rank = 2
    calculated_mass = 3
    delta_cn = 4
    xcorr = 5
    sp = 6
    matched_ions = 7
    expected_ions = 8
    sequence = 9
    validation_status = 10


class MLineColumns_v2_1_0(Enum):
    letter = 0
    xcorr_rank = 1
    sp_rank = 2
    calculated_mass = 3
    delta_cn = 4
    xcorr = 5
    sp = 6
    matched_ions = 7
    expected_ions = 8
    sequence = 9
    validation_status = 10
    predicted_ook0 = 11
    tims_score = 12


class MLineColumns_v2_1_0_ext(Enum):
    letter = 0
    xcorr_rank = 1
    sp_rank = 2
    calculated_mass = 3
    delta_cn = 4
    xcorr = 5
    sp = 6
    matched_ions = 7
    expected_ions = 8
    sequence = 9
    validation_status = 10
    predicted_ook0 = 11
    tims_score = 12
    tims_b_score_m2 = 13
    tims_b_score_best_m = 14


class SLineColumns(Enum):
    letter = 0
    low_scan = 1
    high_scan = 2
    charge = 3
    process_time = 4
    server = 5
    experimental_mass = 6
    total_ion_intensity = 7
    lowest_sp = 8
    number_matches = 9


class SLineColumns_v2_1_0(Enum):
    letter = 0
    low_scan = 1
    high_scan = 2
    charge = 3
    process_time = 4
    server = 5
    experimental_mass = 6
    total_ion_intensity = 7
    lowest_sp = 8
    number_matches = 9
    experimental_ook0 = 10


class SLineColumns_v2_1_0_ext(Enum):
    letter = 0
    low_scan = 1
    high_scan = 2
    charge = 3
    process_time = 4
    server = 5
    experimental_mass = 6
    total_ion_intensity = 7
    lowest_sp = 8
    number_matches = 9
    experimental_ook0 = 10
    experimental_mz = 11
    corrected_ook0 = 12

