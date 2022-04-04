import argparse
import os
import re

import numpy as np
import pandas as pd
from deeplc import DeepLC
from tqdm import tqdm
#from deeplc import DeepLC
from senpy.ms2.lines import ILine
from senpy.ms2_fast.parser import read_file_incrementally as parse_ms2_incrementally
from senpy.sqt.parser import read_file
from itertools import compress

def parse_args():
    # Parse Arguments
    _parser = argparse.ArgumentParser(description='Arguments for Ms2 Extractor')
    _parser.add_argument('--sqt', required=True, type=str,
                         help='path to sqt file')
    _parser.add_argument('--ms2', required=True, type=str, default=None,
                         help='path to ms2 file')
    _parser.add_argument('--retention_time_keyword', required=False, type=str, default=ILine.RETENTION_TIME_KEYWORD,
                         help='I line keyword for retention time')

    # add the command line args from the stream-engine
    return _parser.parse_args()


def get_scan_num_to_retention_time_map(ms2_file, retention_time_keyword):
    scan_num_to_retention_time_map = {}
    for ms2_spectra in tqdm(parse_ms2_incrementally(ms2_file)):
        rt = float(ms2_spectra.get_retention_time(keyword=retention_time_keyword))
        sn = int(ms2_spectra.s_line.get_low_scan())
        scan_num_to_retention_time_map[sn] = rt
    return scan_num_to_retention_time_map

def get_peptide_df(sequences):
    d = {'seq': sequences, 'modifications': [''] * len(sequences)}
    db_df = pd.DataFrame(data=d)
    return db_df


def get_calibration_df(sequences, retention_times):
    d = {'seq': sequences, 'tr': retention_times, 'modifications': [''] * len(retention_times)}
    calibration_df = pd.DataFrame(d)
    return calibration_df


def is_valid_sequence(sequence):
    return bool(re.match('^[ARNDCEQGHILKMFPSTWYV]+$', sequence))


def generate_rt_score_sqt(sqt_file, ms2_file, retention_time_keyword):
    scan_num_to_retention_time_map = get_scan_num_to_retention_time_map(ms2_file, retention_time_keyword)

    _, s_lines = read_file(sqt_file)
    print(len(s_lines))

    # determine 95% Xcorr: This represents good quality id's
    x_corrs = []
    for s_line in s_lines:
        if len(s_line.m_lines) > 0 and s_line.m_lines[0].xcorr > 0 and not s_line.m_lines[0].is_reverse():
            x_corrs.append(s_line.m_lines[0].xcorr)
    x_corr_95_percentile = np.percentile(x_corrs, 95)
    print(x_corr_95_percentile)

    # Filter sequences which have xcorrs > x_corr_95_percentile
    align_sequences = []
    align_retention_times = []
    for s_line in s_lines:
        if len(s_line.m_lines) > 0 and s_line.m_lines[0].xcorr >= x_corr_95_percentile and not s_line.m_lines[0].is_reverse():
            align_sequences.append(s_line.m_lines[0].sequence.split(".")[1] )
            align_retention_times.append(scan_num_to_retention_time_map[s_line.low_scan])

    # Calibrate DeepLC with best sequences
    valid_sequence_flags = [is_valid_sequence(sequence) for sequence in align_sequences]
    calibration_df = get_calibration_df(sequences=list(compress(align_sequences, valid_sequence_flags)),
                                        retention_times=list(compress(align_retention_times, valid_sequence_flags)))
    dlc = DeepLC()
    dlc.calibrate_preds(seq_df=calibration_df)

    # get sequences/rts for prediction
    sequences = []
    for s_line in s_lines:
        if len(s_line.m_lines) > 0 and s_line.m_lines[0].xcorr >= x_corr_95_percentile and not s_line.m_lines[0].is_reverse():
            sequences.append(s_line.m_lines[0].sequence.split(".")[1])
            #retention_times.append(scan_num_to_retention_time_map[s_line.low_scan])

    valid_sequence_flags = [is_valid_sequence(sequence) for sequence in sequences]
    sequences = list(compress(sequences, valid_sequence_flags))
    sequences = list(set(sequences))

    peptide_df = get_peptide_df(sequences)
    calibrated_predictions = dlc.make_preds(seq_df=peptide_df)
    sequence_to_retention_time_map = {seq : rt for seq, rt in zip(sequences, calibrated_predictions)}

    # determin mean/sqt error for best sequences
    rt_prediction_errors = [sequence_to_retention_time_map[seq] - expt_rt for seq, expt_rt in zip(align_sequences, align_retention_times)]
    print(np.mean(rt_prediction_errors), np.std(rt_prediction_errors))

    # Update experimental ook0 values and generate timscores
    for s_line in s_lines:
        experimental_retention_time = scan_num_to_retention_time_map[s_line.low_scan]
        s_line.experimental_ook0 = experimental_retention_time
        for m_line in s_line.m_lines:
            clean_seq = m_line.sequence.split(".")[1]
            if clean_seq in sequence_to_retention_time_map:
                predicted_rt = sequence_to_retention_time_map[clean_seq]

            """# if s_line.experimental_ook0 is None or m_line.xcorr == 0 or predicted_mobility is None:
            if s_line.experimental_ook0 is None or predicted_mobility is None:
                m_line.predicted_ook0 = None  # Correct
                m_line.tims_score = None
                continue

            error = (s_line.experimental_ook0 - predicted_mobility) / s_line.experimental_ook0
            timsscore = calculate_timsscore(error, std_by_charge[s_line.charge])
            m_line.predicted_ook0 = predicted_mobility
            m_line.tims_score = timsscore"""




if __name__ == '__main__':
    args = parse_args()

    print(args)

    generate_rt_score_sqt(args.sqt, args.ms2, retention_time_keyword=args.retention_time_keyword)

"""
def align(pep_df):
    dlc = DeepLC()
    dlc.calibrate_preds(seq_df=pep_df)

    calibrated_predictions = dlc.make_preds(seq_df=pep_df)
    pep_df['calibrated_prediction'] = calibrated_predictions
    pep_df['calibrated_percent_error'] = abs((pep_df["tr"] - pep_df['calibrated_prediction']) / pep_df["tr"])

    uncalibrated_predictions = dlc.make_preds(seq_df=pep_df, calibrate=False)
    pep_df['uncalibrated_prediction'] = uncalibrated_predictions
    pep_df['kde_density'] = get_kde_density_values(pep_df)
    pep_df['line_percent_error'] = get_best_fit_error(pep_df)

    # get most accurate peptides for calibration
    dlc = DeepLC()
    df_final = get_df_by_percentile(pep_df, 60)
    dlc.calibrate_preds(seq_df=df_final)

    return dlc
"""
