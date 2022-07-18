import os
from pathlib import Path
from typing import List


def get_searches_from_experiment(experiment: Path) -> List[Path]:
    searches = list(experiment.glob('search/*/'))
    searches = [search for search in searches if search.is_dir()]  # removes luciphor_ptm_out_final.txt
    searches.sort(key=os.path.getctime)
    return searches


def get_search_by_id_from_experiment(experiment: Path, search_id: str) -> Path:
    searches = get_searches_from_experiment(experiment)
    for search in searches:
        if search_id in search.name:
            return search


def get_latest_search_from_experiment(experiment: Path) -> Path:
    return get_searches_from_experiment(experiment)[0]


def get_oldest_search_from_experiment(experiment: Path) -> Path:
    return get_searches_from_experiment(experiment)[-1]


