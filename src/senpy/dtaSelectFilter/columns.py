from enum import Enum


class PeptideLineColumns_v2_1_13(Enum):
    is_unique = 0
    file_name = 1
    x_corr = 2
    delta_cn = 3
    conf = 4
    mass_plus_hydrogen = 5
    calc_mass_plus_hydrogen = 6
    ppm = 7
    total_intensity = 8
    spr = 9
    prob_score = 10
    pi = 11
    ion_proportion = 12
    redundancy = 13
    measured_im_value = 14
    predicted_im_value = 15
    im_score = 16
    sequence = 17


class PeptideLineColumns_v2_1_12(Enum):
    """
    Unique|FileName|XCorr|DeltCN|Conf%|M+H+|CalcM+H+|TotalIntensity|SpR|Prob_Score|IonProportion|Redundancy|Sequence
    """
    is_unique = 0
    file_name = 1
    x_corr = 2
    delta_cn = 3
    conf = 4
    mass_plus_hydrogen = 5
    calc_mass_plus_hydrogen = 6
    total_intensity = 7
    spr = 8
    prob_score = 9
    ion_proportion = 10
    redundancy = 11
    sequence = 12


class PeptideLineColumns_v2_1_12_paser(Enum):
    """
    Unique|FileName|XCorr|DeltCN|Conf%|M+H+|CalcM+H+|TotalIntensity|SpR|Prob_Score|IonProportion|Redundancy|Sequence
    """
    is_unique = 0
    file_name = 1
    x_corr = 2
    delta_cn = 3
    conf = 4
    mass_plus_hydrogen = 5
    calc_mass_plus_hydrogen = 6
    ppm = 7
    total_intensity = 8
    spr = 9
    prob_score = 10
    pi = 11
    ion_proportion = 12
    redundancy = 13
    sequence = 14
    ret_time = 15
    ptm_index = 16
    ptm_index_protein_list = 17


class PeptideLineColumns_v2_1_13_timscore(Enum):
    """
    Unique|FileName|XCorr|DeltCN|Conf%|M+H+|CalcM+H+|TotalIntensity|SpR|Prob_Score|IonProportion|Redundancy|Sequence
    """
    is_unique = 0
    file_name = 1
    x_corr = 2
    delta_cn = 3
    conf = 4
    mass_plus_hydrogen = 5
    calc_mass_plus_hydrogen = 6
    ppm = 7
    total_intensity = 8
    spr = 9
    prob_score = 10
    pi = 11
    ion_proportion = 12
    redundancy = 13
    measured_im_value = 14
    predicted_im_value = 15
    im_score = 16
    sequence = 17
    experimental_mz = 18
    corrected_1k0 = 19
    ion_mobility = 20
    ret_time = 21
    ptm_index = 22
    ptm_index_protein_list = 23


class PeptideLineFileNameColumns(Enum):
    file_name = 0
    low_scan = 1
    high_scan = 2
    charge = 3


class ProteinLineColumns_v2_1_12(Enum):
    """
    Enum class to represent PasefFrameMsMsInfo table column numbers
    """
    locus_name = 0
    sequence_count = 1
    spectrum_count = 2
    sequence_coverage = 3
    length = 4
    molWt = 5
    pi = 6
    validation_status = 7
    nsaf = 8
    empai = 9
    description_name = 10

class ProteinLineColumns_v2_1_13(Enum):
    """
    Enum class to represent PasefFrameMsMsInfo table column numbers
    """
    locus_name = 0
    sequence_count = 1
    spectrum_count = 2
    sequence_coverage = 3
    length = 4
    molWt = 5
    pi = 6
    validation_status = 7
    nsaf = 8
    empai = 9
    description_name = 10


class ProteinLineColumns_v2_1_12_paser(Enum):
    """
    Enum class to represent PasefFrameMsMsInfo table column numbers
    """
    locus_name = 0
    sequence_count = 1
    spectrum_count = 2
    sequence_coverage = 3
    length = 4
    molWt = 5
    pi = 6
    validation_status = 7
    nsaf = 8
    empai = 9
    description_name = 10
    h_redundancy = 11
    l_redundancy = 12
    m_redundancy = 13


class ProteinLineColumns_v2_1_13_timscore(Enum):
    """
    Enum class to represent PasefFrameMsMsInfo table column numbers
    """
    locus_name = 0
    sequence_count = 1
    spectrum_count = 2
    sequence_coverage = 3
    length = 4
    molWt = 5
    pi = 6
    validation_status = 7
    nsaf = 8
    empai = 9
    description_name = 10
    h_redundancy = 11
    l_redundancy = 12