import argparse
import os.path
from pathlib import Path

from src.senpy.ip2_project.file_types import Ip2FileType
from src.senpy.ip2_project.search import get_file_from_search
from src.senpy.ip2_project.project import get_latest_search_per_experiment, get_searches_matching_ids
from src.senpy.sqt.parser import read_file, write_file

def parse_args():
    # Parse Arguments
    _parser = argparse.ArgumentParser(description='Arguments for Ip2 project extractor')
    _parser.add_argument('-p', '--project', required=True, type=lambda p: Path(p).absolute(), help='path to ip2 project')
    _parser.add_argument('-i', '--search_ids', nargs='+', required=False, type=str, help='experiment to convert')
    _parser.add_argument('-l', '--list_files', required=False, action='store_true', help='only list files')

    return _parser.parse_args()


def assert_file_exist(pth):
    assert (os.path.isfile(pth))


def set_timsscore_to_zero(sqt: Path):
    h_lines, s_lines = read_file(str(sqt))

    for s_line in s_lines:
        for m_line in s_line.m_lines:
            m_line.tims_score = 0
            m_line.predicted_ook0 = s_line.experimental_ook0

    write_file(h_lines, s_lines, str(sqt), version='v2.1.0_ext')


def convert_projects(project, search_ids=None):
    if search_ids is None:
        searches = get_latest_search_per_experiment(project)
    else:
        searches = get_searches_matching_ids(project, search_ids)

    sqt_files = [get_file_from_search(search, Ip2FileType.SQT) for search in searches]
    for sqt in sqt_files:
        print(sqt)

    con = input("continue: yes/no\n")
    if con == 'no':
        print('Quiting')
        return
    elif con == 'yes':
        for sqt in sqt_files:
            print(f'sqt: {sqt}')
            set_timsscore_to_zero(sqt)
    else:
        print("input not recognized!")


if __name__ == '__main__':
    args = parse_args()
    convert_projects(project=args.project, search_ids=args.search_ids)
