from typing import List

from feature.biosaur.lines import BiosaurFeatureLine
from feature.dinosaur.lines import DinosaurFeatureLine


def parse_file(file_path: str) -> List[BiosaurFeatureLine]:
    """
    Parse biosaur file into BiosaurFeatureLine's
    :param file_path: path to feature.tsv file
    :return: List of BiosaurFeatureLine's
    """
    FeatureLine = None
    with open(file_path) as file:
        for i, line in enumerate(file):
            if i == 0:
                continue
            else:
                if FeatureLine is None:
                    line_elems = line.split('/t')

                    if len(line_elems) == BiosaurFeatureLine.get_number_elements():
                        FeatureLine = BiosaurFeatureLine
                    elif len(line_elems) == DinosaurFeatureLine.get_number_elements():
                        FeatureLine = DinosaurFeatureLine
                    else:
                        print(f"Number of line elements does not match supported file types.")
                        raise NotImplementedError

                feature_line = FeatureLine.deserialize(line)
                yield feature_line

        return feature_line
