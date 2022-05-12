import argparse
import os.path
from glob import glob

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
    _parser.add_argument('--output_dir', required=False, type=str, help='path to output dir')

    return _parser.parse_args()


def _get_latest_search_dir(experiment_path):
    search_folder_path = os.path.join(experiment_path, "search", "*")
    searches = glob(search_folder_path, recursive=True)
    searches.remove('luciphor_ptm_out_final.txt')
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


def main(project_path, output_dir=None):
    ip2_search_paths = get_latest_project_search_dirs(project_path)
    print([glob(os.path.join(pth, "*.ms2"), recursive=True) for pth in ip2_search_paths])
    ms2_file_paths = [glob(os.path.join(pth, "*.ms2"), recursive=True)[0] for pth in ip2_search_paths]
    dta_filter_file_paths = [os.path.join(pth, "DTASelect-filter.txt") for pth in ip2_search_paths]

    # Check that all files exists
    [assert_file_exist(pth) for pth in ms2_file_paths]
    [assert_file_exist(pth) for pth in dta_filter_file_paths]

    for ms2_file_path, dta_filter_file_path in zip(ms2_file_paths,dta_filter_file_paths):

        if output_dir:
            out_file_path = os.path.join(output_dir, os.path.basename(ms2_file_path) + ".out")
        else:
            out_file_path = os.path.splitext(ms2_file_path)[0] + ".out"

        generate_output(ms2_path=ms2_file_path, filter_path=dta_filter_file_path,
                        out_path=out_file_path, dta_filter_version="v2.1.13_timscore")


if __name__ == '__main__':
    args = parse_args()
    main(project_path=args.project_path, output_dir=args.output_dir)
