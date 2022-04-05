import dataclasses
from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Type, Callable

from senpy.ms2_refactor.lines import Line


class LineSerializer(ABC):

    def __init__(self, columns: Enum, ms2_line: Type[Line], line_exception: Type[Exception], line_letter: str):
        self.columns = columns  # Enum representing column order
        self.ms2_line = ms2_line  # Dataclass for line type
        self.line_exception = line_exception
        self.line_letter = line_letter

        self.attribute_map: Dict[str, int] = {field.name: i for i, field in enumerate(dataclasses.fields(self.ms2_line))}
        self.type_map: Dict[str, int] = {field.name: type(field) for field in dataclasses.fields(self.ms2_line)}

    def __hash__(self):
        return hash((str(self.columns)))

    def deserialize(self, line: str) -> Line:
        line_elements = line.rstrip().split("\t")

        if len(line_elements) != len(self.columns):
            raise self.line_exception(_line=line)

        data = [None] * len(dataclasses.fields(self.ms2_line))

        for i, elem in enumerate(line_elements):
            element_name = self.columns(i).name
            deserializer = self.get_deserializer_by_name(element_name)
            if element_name in self.attribute_map:
                attribute_index = self.attribute_map[element_name]
                data[attribute_index] = deserializer(elem)

        return self.ms2_line(*data)

    def serialize(self, line: Line) -> str:

        line_elements = [None] * len(self.columns)

        for column in self.columns:
            if column.name == 'letter':
                line_elements[column.value] = self.line_letter
                continue

            serializer = self.get_serializer_by_name(column.name)
            line_attr = getattr(line, column.name)
            line_elements[column.value] = serializer(line_attr)
        return '\t'.join(line_elements) + '\n'

    @abstractmethod
    def get_serializer_by_name(self, name: str) -> Callable:
        pass

    @abstractmethod
    def get_deserializer_by_name(self, name: str) -> Callable:
        pass
