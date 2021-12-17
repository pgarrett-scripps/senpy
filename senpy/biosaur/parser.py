from senpy.abstract_class import LineSerializer
from senpy.biosaur.lines import FeatureLine
from senpy.biosaur.serializer import DinosuarLineSerializer, BiosaurFeatureLineSerializer

def get_feature_serializer(columns: int) -> LineSerializer:
    if columns == 14: #dinosaur
        return DinosuarLineSerializer
    elif columns == 24: #biosaur
        return BiosaurFeatureLineSerializer
    else:
        print("columns: ", columns)
        raise NotImplementedError

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
                Serializer = get_feature_serializer(len(line.split("\t")))
                h_lines.append(line)
            else:
                feature_line = Serializer.deserialize(line)
                feature_lines.append(feature_line)
        return h_lines, feature_lines