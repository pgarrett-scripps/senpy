from pathlib import Path

from .file_types import Ip2FileType


def get_file_from_search(search: Path, file_type: Ip2FileType) -> Path:
    files = list(search.glob(f'{file_type.value}'))
    if len(files) > 0:
        return files[0]
