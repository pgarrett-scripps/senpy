import argparse
import os

import numpy as np
from matplotlib import pyplot as plt

from src.senpy.dtaSelectFilter.parser import read_file as parse_dta_filter_file
from src.senpy.sqt.parser import read_file as parse_sqt_file


def parse_args():
    # Parse Arguments
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('sqt_file', type=input_file_path, help='absolute path to sqt file')
    args = parser.parse_args()
    return args

def input_file_path(path):
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")

def dta_select(dta_select_filter_file):
    ppms = []
    h_lines, locus_lines, end_lines = parse_dta_filter_file(dta_select_filter_file)
    for locus_line in locus_lines:
        for unique_line in locus_line.peptide_lines:
            ppms.append(unique_line.ppm)

    plt.hist(ppms)
    plt.show()

    print(np.mean(ppms))

def sqt_select(sqt_file):

    xcorrs = []
    h_lines, s_lines = parse_sqt_file(sqt_file)
    for s_line in s_lines:
        for m_line in s_line.m_lines:
            if not m_line.is_reverse():
                xcorrs.append(m_line.xcorr)

    percentile_xcorr = np.percentile(xcorrs, 95)
    print(percentile_xcorr)

    ppms = {}
    for s_line in s_lines:
        for m_line in s_line.m_lines:
            if not m_line.is_reverse() and m_line.xcorr >= percentile_xcorr:
                if s_line.charge not in ppms:
                    ppms[s_line.charge] = []
                ppms[s_line.charge].append((m_line.calculated_mass - s_line.experimental_mass)/m_line.calculated_mass*1_000_000)

    for charge in ppms:
        plt.hist(ppms[charge], bins = 50, label=charge)
        plt.legend()
        plt.show()

    print(np.mean(ppms))



if __name__ == '__main__':
    args = parse_args()
    for arg in vars(args):
        print(arg, getattr(args, arg))

    sqt_select(sqt_file = args.sqt_file)