import os

from senpy.idx.data import IdxInfo
from senpy.idx.serializer import IdxSerializer


def parse_file(idx_folder_path: str) -> [IdxInfo]:
    idx_files = os.listdir(idx_folder_path)
    idx_info_list = []
    for idx_file in idx_files:

        if 'idx' in idx_file:
            idx_file_path = idx_folder_path + os.path.sep + idx_file
            idx_info_list.extend(IdxSerializer.deserialize(idx_file_path))

    return idx_info_list


def write_file(idx_info_list: [IdxInfo]) -> None:
    pass
