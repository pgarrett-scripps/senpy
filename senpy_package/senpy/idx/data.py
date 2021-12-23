from dataclasses import dataclass, field
from typing import List


@dataclass
class IdxInfo:
    precursorMass: float
    seqOffset: int
    seqLength: int
    proteinIds: List[int] = field(default_factory=list)

