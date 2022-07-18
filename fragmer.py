from typing import List, Set
from pyteomics import mass
from itertools import product
import numpy as np
from numba import jit
from dataclasses import dataclass
from enum import Enum


class IonType(Enum):
    A = 'a'
    B = 'b'
    C = 'c'
    X = 'x'
    Y = 'y'
    Z = 'z'


FORWARD_IONS = {IonType.A, IonType.B, IonType.C}
BACKWARD_IONS = {IonType.X, IonType.Y, IonType.Z}
WATER_MASS = 18.01528
PROTON_MASS = 1.00727647


def get_mass_spectra(peptide: str, ion_type: IonType, charge: int) -> List[float]:
    """
    The function generates all possible m/z for fragments of IonType for charge
    """
    ions = []
    for i in range(1, len(peptide) + 1):
        if ion_type in FORWARD_IONS:
            ions.append(mass.fast_mass(peptide[:i], ion_type=ion_type.value, charge=charge))
        elif ion_type in BACKWARD_IONS:
            ions.append(mass.fast_mass(peptide[i - 1:], ion_type=ion_type.value, charge=charge))
        else:
            raise NotImplementedError(f"Ion Type: {ion_type} Not Supported!")
    return ions


def generate_fragmer_dict(amino_acids: str, permutations: int, ion_types: Set[IonType]):
    """Calculates all permutations up to length permutations with replacement. All peptide substrings are
    fragmented for IonTypes"""
    fragment_dict = {}
    for ion_type in ion_types:
        fragment_dict[ion_type] = {}
        for perm_repeat in range(1, permutations + 1):
            perms = [p for p in product(amino_acids, repeat=perm_repeat)]
            for perm in perms:
                seqmer = "".join(perm)
                fragment_dict[ion_type][seqmer] = np.array(get_mass_spectra(seqmer, ion_type=ion_type, charge=0))

    return fragment_dict


def get_k_length_sub_strings(seq, k, reverse=False):
    """Given a sequence return a list of substrings of length k, if reverse == True start from the back"""
    if reverse:
        return [seq[max([i - k, 0]):i] for i in range(len(seq), 0, -k)]
    else:
        return [seq[i:i + k] for i in range(0, len(seq), k)]


@jit(nopython=True)
def combine_masses(masses, k):
    """given an array of masses, iteratively add each chunk of k elements"""
    for i in range(0, len(masses), k):
        if i != 0:
            masses[i:i + k] = masses[i:i + k] + masses[i - 1]
    return masses


@dataclass
class FragIons:
    ion_type: IonType
    charge: int
    ions: np.array


def get_mass_spectra_old(peptide, types=('b', 'y'), maxcharge=2):
    """
    The function generates all possible m/z for fragments of types
    `types` and of charges from 1 to `maxharge`.
    """
    ions = []
    for ion_type in types:
        for charge in range(1, maxcharge + 1):
            for i in range(1, len(peptide) + 1):
                if ion_type[0] in 'abc':
                    ions.append(mass.fast_mass(peptide[:i], ion_type=ion_type, charge=charge))
                else:
                    ions.append(mass.fast_mass(peptide[i - 1:], ion_type=ion_type, charge=charge))
    return ions


class Fragmer:
    """
    Fragmer generates fragment ion spectra for peptides from precomputed N-mers up to length permutations.
    The fragment ions for each N-mer is stores in a dictionary, peptides are turned into a list of N-mers:

    permutations = 3
    peptide = "PEPTIDE"
        if B_ions -> ["PEP", "TID", "E"]
        if Y_ions -> ["IDE", "EPT", "P"]

    The fragment masses for each N-mer is lookedup in the precomputed N-mer dictionary:

        if B_ions -> [[ 98.0600364, 227.1026264, 324.1553864], [102.0549564, 215.1390164, 330.1659564], [130.04986647]]
        if Y_ions -> [[376.1714311, 263.0873711, 148.0604311], [346.1608711, 217.1182811, 120.0655211], [116.07060115]]

        * each sub-array of y-ion N-mers are reversed so that they

        if Y_ions -> [[148.0604311, 263.0873711, 376.1714311], [120.0655211, 217.1182811, 346.1608711], [116.0706011]]

    The ragged array is flattened to form a 1d array

        B_ions -> [98.06003647 227.10262647 324.15538647 102.05495647 215.13901647 330.16595647 130.04986647]
        Y_ions -> [148.06043115 263.08737115 376.17143115 120.06552115 217.11828115 346.16087115 116.07060115]

    A window of len N (permutations) is looped over the flattened array.
    The N-1 ion is appended to the next windows fragment ions.

        98.0600364 227.1026264 324.1553864    |   102.054956 215.139016 330.165956    |  130.04986647

        [98.0600364 227.1026264 324.1553864] -> + 324.15538647  - (WATER if y-ion)
                                                   -------------------------------------------
                                                  425.203066 538.287126 653.314066]  -> + 653.3140664 - (WATER if y-ion)
                                                                                          --------------
                                                                                          782.35665646

        98.0600364 227.1026264 324.1553864    |   425.2030664 538.2871264 653.3140664  |  782.35665646]

    """

    def __init__(self, permutations: int, ion_types=None, valid_amino_acids: str = 'ARNDCEQGHILKMFPSTWYV'):

        if ion_types is None:
            ion_types = {IonType.B, IonType.Y}

        self._permutations = permutations
        self._ion_types = ion_types
        self._valid_amino_acids = valid_amino_acids
        self._fragmer_dict = generate_fragmer_dict(self.valid_amino_acids, self.permutations, self.ion_types)

    def fragment_peptide(self, peptide_sequence, ion_types: Set[IonType], charges: List[int]) -> List[FragIons]:
        frag_ions = []
        for ion_type in ion_types:
            subseqs = get_k_length_sub_strings(peptide_sequence, self.permutations, reverse=ion_type in BACKWARD_IONS)
            if ion_type in BACKWARD_IONS:
                subseq_masses = [self.fragmer_dict[ion_type][subseq][::-1] for subseq in subseqs]
                if ion_type == IonType.Y:
                    subseq_masses = [masses - WATER_MASS * i for i, masses in enumerate(subseq_masses)]
            else:
                subseq_masses = [self.fragmer_dict[ion_type][subseq] for subseq in subseqs]
            frag_ion_masses = combine_masses(np.concatenate(subseq_masses).ravel(), k=self.permutations)
            for charge in charges:
                frag_ions.append(FragIons(ion_type=ion_type, charge=charge,
                                          ions=((frag_ion_masses[:-1] + (PROTON_MASS * charge)) / charge)))
        return frag_ions

    @property
    def permutations(self):
        return self._permutations

    @property
    def ion_types(self):
        return self._ion_types

    @property
    def valid_amino_acids(self):
        return self._valid_amino_acids

    @property
    def fragmer_dict(self):
        return self._fragmer_dict
