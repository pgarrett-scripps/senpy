from pathlib import Path

from src.senpy.ip2_project.experiment import get_searches_from_experiment, get_search_by_id_from_experiment, get_latest_search_from_experiment, get_oldest_search_from_experiment
from src.senpy.ip2_project.project import get_experiments_in_project, get_searches_matching_ids
from src.senpy.ip2_project.search import get_file_from_search
from src.senpy.ip2_project.file_types import Ip2FileType

ip2_project = r"C:\data\test_ip2_project"
experiment = r"C:\data\test_ip2_project\Human_Trypsin_SK_Fractionation_Concatenation_Group_1_1uL_G5_1_1029_2022_05_18_02_251464"
search = r"C:\data\test_ip2_project\Human_Trypsin_SK_Fractionation_Concatenation_Group_1_1uL_G5_1_1029_2022_05_18_02_251464\search\projects2022_05_18_19_157895"

searches = get_searches_from_experiment(Path(experiment))
print(len(searches))

print(get_search_by_id_from_experiment(Path(experiment), '157895'))
print(get_search_by_id_from_experiment(Path(experiment), '157896'))
print(get_search_by_id_from_experiment(Path(experiment), '157897'))

print(get_latest_search_from_experiment(Path(experiment)))
print(get_oldest_search_from_experiment(Path(experiment)))

print(get_experiments_in_project(Path(ip2_project)))

for file_type in Ip2FileType:
    print(file_type, get_file_from_search(Path(search), file_type))

print(get_searches_matching_ids(Path(ip2_project), ['157895', '157896']))

print(str(get_oldest_search_from_experiment(Path(experiment))))
