import os
from pathlib import Path
from typing import List

from .experiment import get_latest_search_from_experiment, get_oldest_search_from_experiment, \
    get_searches_from_experiment, get_search_by_id_from_experiment

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

ITEMS_TO_REMOVE = ['default_params', 'tmp_bulk_upload', 'activeExpList.txt']


def get_experiments_in_project(project: Path) -> List[Path]:
    experiments = list(project.glob('*/'))
    experiments = [experiment for experiment in experiments if experiment.name not in ITEMS_TO_REMOVE]
    experiments.sort(key=os.path.getctime)
    return experiments


def get_latest_search_per_experiment(project: Path) -> List[Path]:
    experiments = get_experiments_in_project(project)
    searches = [get_latest_search_from_experiment(experiment) for experiment in experiments]
    return searches


def get_oldest_per_experiment(project: Path) -> List[Path]:
    experiments = get_experiments_in_project(project)
    searches = [get_oldest_search_from_experiment(experiment) for experiment in experiments]
    return searches


def get_nth_search_per_experiment(project: Path, n: int) -> List[Path]:
    experiments = get_experiments_in_project(project)
    searches = [get_searches_from_experiment(experiment)[n] for experiment in experiments]
    return searches


def get_searches_matching_ids(project: Path, search_ids: List[str]) -> List[Path]:
    experiments = get_experiments_in_project(project)
    searches = []
    for experiment in experiments:
        for search_id in search_ids:
            search = get_search_by_id_from_experiment(experiment, search_id)
            if search:
                searches.append(search)
    return searches
