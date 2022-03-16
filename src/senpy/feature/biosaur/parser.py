from typing import List

from feature.biosaur.lines import BiosaurFeatureLine


def parse_file(file_path: str) -> List[BiosaurFeatureLine]:
    """
    Parse biosaur file into BiosaurFeatureLine's
    :param file_path: path to feature.tsv file
    :return: List of BiosaurFeatureLine's
    """
    with open(file_path) as file:
        for i, line in enumerate(file):
            if i == 0:
                continue
            else:
                feature_line = BiosaurFeatureLine.deserialize(line)
                yield feature_line

        return feature_line
