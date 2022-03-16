from typing import List

from feature.dinosaur.lines import DinosaurFeatureLine


def parse_file(file_path: str) -> List[DinosaurFeatureLine]:
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
                feature_line = DinosaurFeatureLine.deserialize(line)
                yield feature_line

        return feature_line
