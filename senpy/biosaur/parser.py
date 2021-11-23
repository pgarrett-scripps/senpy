from senpy.biosaur.lines import FeatureLine
from senpy.biosaur.serializer import FeatureLineSerializer


def parse_file(file_path) -> ([str], [FeatureLine]):
    """
    Parse ms2 file into h_lines and s_lines
    :param file_path: ms2 file
    :return: h_lines: [str], s_lines: [SLine]
    """
    h_lines, feature_lines = [], []

    with open(file_path) as file:
        for i, line in enumerate(file):
            if i == 0:
                h_lines.append(line)
            else:
                feature_line = FeatureLineSerializer.deserialize(line)
                feature_lines.append(feature_line)
        return h_lines, feature_lines