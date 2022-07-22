import argparse

from src.senpy.sqt import parser as sqt_parser


def parse_args():
    # Parse Arguments
    _parser = argparse.ArgumentParser(description='Arguments for Ms2 Extractor')
    _parser.add_argument('--sqt_rt', required=False, type=str,
                         help='path to sqt file')
    _parser.add_argument('--sqt_tim', required=False, type=str,
                         help='path to sqt file')

    # add the command line args from the stream-engine
    return _parser.parse_args()


def combine_sqt(sqt_rt, sqt_tim):
    _, s_lines_rt = sqt_parser.read_file(sqt_rt)
    _, s_lines_tims = sqt_parser.read_file(sqt_tim)

    for s_line_rt, s_line_tim in zip(s_lines_rt, s_lines_tims):

        for m_line_rt, m_line_tim in zip(s_line_rt.m_lines, s_line_tim.m_lines):
            m_line_rt.predicted_ook0 = m_line_tim.tims_score

    sqt_parser.write_file(_, s_lines_rt, sqt_tim + ".com", version="v2.1.0_ext")


if __name__ == '__main__':
    args = parse_args()
    print(args)

    combine_sqt(args.sqt_rt, args.sqt_tim)