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

    return _parser.parse_args()


def assert_file_exist(pth):
    assert (os.path.isfile(pth))


def convert_projects(project, search_ids=None):
    if search_ids is None:
        searches = get_latest_search_per_experiment(project)
    else:
        searches = get_searches_matching_ids(project, search_ids)



    for search in searches:
        print(search)

    con = input("continue: yes/no\n")
    if con == 'no':
        print('Quiting')
        return
    elif con == 'yes':
        for search in searches:
            print(f'search: {search}')
            remove_DTA_files(search)
    else:
        print("input not recognized!")


if __name__ == '__main__':
    args = parse_args()
    convert_projects(project=args.project, search_ids=args.search_ids)
