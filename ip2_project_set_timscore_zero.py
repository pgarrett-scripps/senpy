import argparse
import os.path
from glob import glob
from src.senpy.sqt.parser import read_file, write_file

import numpy as np

from generate_output import generate_output

# IP2 Files Structure:
# Project_Name <-- project_path
#   Experiments*
#       search
#           searches*
#       spectra
#           ms2
#   default_params
#   tmp_bulk_upload
#   activeExptList.txt


def parse_args():
    # Parse Arguments
    _parser = argparse.ArgumentParser(description='Arguments for Ip2 project extractor')
    _parser.add_argument('--project_path', required=True, type=str, help='path to ip2 project')

    return _parser.parse_args()


def _get_latest_search_dir(experiment_path):
    search_folder_path = os.path.join(experiment_path, "search", "*")
    searches = glob(search_folder_path, recursive=True)
    searches = [search for search in searches if "luciphor_ptm_out_final" not in search]
    search_times = [os.path.getctime(search) for search in searches]
    latest_search = searches[np.argmax(search_times)]
    return latest_search


def get_experiments_in_project(project_path):
    experiments = os.listdir(project_path)
    experiments.remove("default_params")
    experiments.remove("tmp_bulk_upload")
    experiments.remove("activeExpList.txt")
    return experiments


def get_latest_project_search_dirs(project_path):
    experiments = get_experiments_in_project(project_path)
    print(f"experiments: {len(experiments)}")
    search_paths = [_get_latest_search_dir(os.path.join(project_path, expt)) for expt in experiments]
    return search_paths


def assert_file_exist(pth):
    assert (os.path.isfile(pth))


def set_timsscore_to_zero(sqt_path):
    h_lines, s_lines = read_file(sqt_path)

    for s_line in s_lines:
        for m_line in s_line.m_lines:
            m_line.tims_score = 0
            m_line.predicted_ook0 = s_line.experimental_ook0

    write_file(h_lines, s_lines, sqt_path+".zero", version='v2.1.0_ext')


def main(project_path):
    ip2_search_paths = get_latest_project_search_dirs(project_path)
    sqt_file_path = [glob(os.path.join(pth, "*.sqt"), recursive=True)[0] for pth in ip2_search_paths]
    print(sqt_file_path)
    # Check that all files exists
    [assert_file_exist(pth) for pth in sqt_file_path]

    for sqt_file in sqt_file_path:

        set_timsscore_to_zero(sqt_file)

if __name__ == '__main__':
    args = parse_args()
    main(project_path=args.project_path)
