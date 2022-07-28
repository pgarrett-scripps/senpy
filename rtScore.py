import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
from deeplc import DeepLC
import scipy.stats as stats

from src.senpy.ip2_project.file_types import Ip2FileType
from src.senpy.ip2_project.project import get_latest_search_per_experiment, get_searches_matching_ids
from src.senpy.ip2_project.search import get_file_from_search
from src.senpy.ms2.lines import ILine
from src.senpy.ms2 import fast_parser as fast_ms2_parser
from src.senpy.sqt import parser as sqt_parser

MOD_MAP = {}
MOD_MAP['(15.994915)'] = 'Oxidation'
MOD_MAP['(0.984016)'] = 'Deamidated'


def parse_args():
    # Parse Arguments
    _parser = argparse.ArgumentParser(description='Arguments for Ms2 Extractor')
    _parser.add_argument('--sqt', required=False, type=str,
                         help='path to sqt file')
    _parser.add_argument('--ms2', required=False, type=str, default=None,
                         help='path to ms2 file')
    _parser.add_argument('--out', required=False, type=str, default=None,
                         help='path to out sqt file')
    _parser.add_argument('--newfile', required=False, action='store_true', default=None,
                         help='path to out sqt file')
    _parser.add_argument('-p', '--project', required=False, type=lambda p: Path(p).absolute(), help='path to ip2 project')
    _parser.add_argument('-i', '--search_ids', nargs='+', required=False, type=str, help='experiment to convert')
    _parser.add_argument('--retention_time_keyword', required=False, type=str, default=ILine.RETENTION_TIME_KEYWORD,
                         help='I line keyword for retention time')

    # add the command line args from the stream-engine
    return _parser.parse_args()


def get_scan_num_to_retention_time_map(ms2_spectras, retention_time_keyword):
    scan_num_to_retention_time_map = {}
    for ms2_spectra in ms2_spectras:
        rt = float(ms2_spectra.get_retention_time(keyword=retention_time_keyword))
        sn = int(ms2_spectra.s_line.get_low_scan())
        scan_num_to_retention_time_map[sn] = rt
    return scan_num_to_retention_time_map


def convert_mod_sequence(sequence):
    mods = []

    for key in MOD_MAP:
        while sequence.find(key) != -1:
            itr = 0
            for aa in sequence[:sequence.find(key)]:
                if aa.isalpha():
                    itr += 1
            sequence = sequence.replace(key, "", 1)
            mods.append(f"{itr}|{MOD_MAP[key]}")
    return mods, sequence


def calculate_score(error, std):
    z_score = error / std
    timsscore = stats.norm.sf(abs(z_score)) * 2
    return timsscore


def is_valid_sequence(sequence):
    return bool(re.match('^[ARNDCEQGHILKMFPSTWYV]+$', sequence))


def generate_rt_score_sqt(sqt_file, ms2_file, out_file, retention_time_keyword):
    _, ms2_spectras = fast_ms2_parser.read_file(ms2_file)
    _, s_lines = sqt_parser.read_file(sqt_file)

    rt_by_sn_map = get_scan_num_to_retention_time_map(ms2_spectras, retention_time_keyword)

    data = {'ip2_seq': [], 'tr': [], 'reverse': [], 'xcorr': [], 'm_line_number': []}
    for s_line in s_lines:
        for i, m_line in enumerate(s_line.m_lines):
            data['ip2_seq'].append(m_line.sequence)
            data['tr'].append(rt_by_sn_map[s_line.low_scan])
            data['xcorr'].append(m_line.xcorr)
            data['reverse'].append(m_line.is_reverse())
            data['m_line_number'].append(i)

    df = pd.DataFrame(data)
    df['clean_seq'] = [seq[2:-2] for seq in df.ip2_seq]
    df['modifications'] = ["|".join(convert_mod_sequence(seq)[0]) for seq in df.clean_seq]
    df['seq'] = [convert_mod_sequence(seq)[1] for seq in df.clean_seq]
    df['is_valid'] = [is_valid_sequence(seq) for seq in df.seq]

    x_corr_percentile = np.percentile(df[(df.reverse == False) & (df.m_line_number == 0)].xcorr, 95)
    print(x_corr_percentile)

    align_df = df[(df.reverse == False) & (df.xcorr >= x_corr_percentile)
                  & (df.is_valid == True) & (df.m_line_number == 0)]
    print("number of alignment peptides: ", len(align_df))

    dlc = DeepLC()
    dlc.calibrate_preds(seq_df=align_df)

    prediction_df = df[(df.is_valid == True)]
    prediction_df['pred_rt'] = dlc.make_preds(seq_df=prediction_df)

    prediction_df_targets = prediction_df[
        (prediction_df.xcorr >= x_corr_percentile) & (prediction_df.reverse == False) & (
                    prediction_df.m_line_number == 0)]

    pred_error = prediction_df_targets.tr - prediction_df_targets.pred_rt
    pred_rt_by_seq_dict = {seq: rt for seq, rt in zip(prediction_df.ip2_seq, prediction_df.pred_rt)}
    rt_std = np.std(pred_error)

    # Update experimental ook0 values and generate timscores
    for s_line in s_lines:
        experimental_rt = rt_by_sn_map[s_line.low_scan]
        s_line.experimental_ook0 = experimental_rt
        for m_line in s_line.m_lines:
            sequence = m_line.sequence
            if sequence in pred_rt_by_seq_dict and m_line.xcorr != 0:
                predicted_rt = pred_rt_by_seq_dict[sequence]
                error = experimental_rt - predicted_rt
                timsscore = calculate_score(error, rt_std)
            else:
                predicted_rt = None
                timsscore = None

            m_line.predicted_ook0 = predicted_rt
            m_line.tims_score = timsscore

    sqt_parser.write_file(_, s_lines, str(out_file), version="v2.1.0_ext")


if __name__ == '__main__':
    args = parse_args()

    print(args)

    if args.project and args.search_ids:

        searches = get_searches_matching_ids(args.project, args.search_ids)
        sqt_files = [get_file_from_search(search, Ip2FileType.SQT) for search in searches]
        ms2_files = [get_file_from_search(search, Ip2FileType.MS2) for search in searches]

        print("sqt_files: ", sqt_files)
        print("ms2_files: ", ms2_files)
        con = input("continue: yes/no\n")
        if con != "yes":
            quit(1)

        for ms2, sqt in zip(ms2_files, sqt_files):
            if args.newfile:
                args.out = Path(str(sqt) + ".rtscore")
            print(str(ms2).split("\\")[-1])
            generate_rt_score_sqt(str(sqt), str(ms2), str(args.out), retention_time_keyword=args.retention_time_keyword)

    if args.sqt and args.ms2:
        if args.newfile:
            args.out = Path(str(args.sqt) + ".rtscore")
        generate_rt_score_sqt(args.sqt, args.ms2, args.out, retention_time_keyword=args.retention_time_keyword)
