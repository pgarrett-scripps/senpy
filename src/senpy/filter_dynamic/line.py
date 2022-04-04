from dataclasses import dataclass


def map_line(header_keys, line_values):
    return {key: value for key, value in zip(header_keys, line_values)}
