from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import Lock
from typing import Any, List, Dict


"""
PSM (becomes a python dict)
"{"mz":1000, "rt":250, "ook0":0.9, "Sequence": "PEPTIDE", "score": 2.0 ...}"
{"mz":1000, "rt":250, "ook0":0.9, "Sequence": "PEPTIDE", "score": 2.0 ...}
"""

#bounday.py
@dataclass
class Boundary:
    __slots__ = "lower", "upper"
    lower: float
    upper: float


def psm_in_bounds(mz, ook0, rt, mz_bounds: Boundary, ook0_bounds: Boundary, rt_bounds: Boundary) -> bool:
    return mz_bounds.lower <= mz <= mz_bounds.upper and \
           ook0_bounds.lower <= ook0 <= ook0_bounds.upper and \
           rt_bounds.lower <= rt <= rt_bounds.upper


def get_mz_bounds(mz: float, ppm: float) -> Boundary:
    return Boundary(lower=mz - mz * ppm / 1_000_000,
                    upper=mz + mz * ppm / 1_000_000)


def get_ook0_bounds(ook0: float, tolerance: float) -> Boundary:
    return Boundary(lower=ook0 - ook0 * tolerance,
                    upper=ook0 + ook0 * tolerance)


def get_rt_bounds(rt: float, offset: float) -> Boundary:
    return Boundary(lower=rt - offset,
                    upper=rt + offset)


# Trees.py
@dataclass
class AbstractPSMTree(ABC):
    db: Any
    _lock: Lock = Lock()

    @abstractmethod
    def search(self, mz_bounds: Boundary, ook0_bounds: Boundary, rt_bounds: Boundary) -> List[Dict]:
        """
        searches the PSMTree over a given boundary. Return all psm's within the bounds
        """
        pass

    @abstractmethod
    def add(self, psm: Dict) -> None:
        """
        adds psm to interval tree with passed dims
        """
        pass

    @abstractmethod
    def len(self) -> int:
        pass

    @abstractmethod
    def save(self, file_name: str) -> None:
        """
        saves all psm's within tree to a text file
        """
        pass

    @abstractmethod
    def load(self, file_name: str) -> None:
        """
        adds psm's from text file to PSMTree
        """
        pass

"""
Remove pass and replace with actual code
"""

@dataclass
class PsmRedBlackTree(AbstractPSMTree):
    db: RedBlackTree = RedBlackTree()

    def search(self, mz_bounds: Boundary, ook0_bounds: Boundary, rt_bounds: Boundary) -> List[Dict]:
        pass

    def add(self, psm: Dict) -> None:
        pass

    def len(self) -> int:
        pass

    def save(self, file_name: str) -> None:
        pass

    def load(self, file_name: str) -> None:
        pass


@dataclass
class PsmKDTree(AbstractPSMTree):
    db: KDTree = KDTree()

    def search(self, mz_bounds: Boundary, ook0_bounds: Boundary, rt_bounds: Boundary) -> List[Dict]:
        pass

    def add(self, psm: Dict) -> None:
        pass

    def len(self) -> int:
        pass

    def save(self, file_name: str) -> None:
        pass

    def load(self, file_name: str) -> None:
        pass