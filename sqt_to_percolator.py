import argparse
import re
from pathlib import Path
from typing import List

from Bio.SeqUtils.ProtParam import ProteinAnalysis

from senpy.sqt.lines import SLine
from src.senpy.sqt import parser as sqt_parser


def parse_args():
    # Parse Arguments
    _parser = argparse.ArgumentParser(description='Arguments for Ms2 Extractor')
    _parser.add_argument('--sqt', required=False, type=str,
                         help='path to sqt file')

    # add the command line args from the stream-engine
    return _parser.parse_args()


def convert_sqt_to_pin(sqt: str):
    s_lines = List[SLine]
    _, s_lines = sqt_parser.read_file(sqt)

    # id <tab> label <tab> scannr <tab> feature1 <tab> ... <tab> featureN <tab> peptide <tab> proteinId1 <tab> .. <tab> proteinIdM
    with open(sqt + ".tsv", "w") as pin_file:
        # PSMId < tab > Label < tab > ScanNr < tab > feature1name < tab > ... < tab > featureNname < tab > Peptide < tab > Proteins
        pin_file.write(f"{'PSMId'}\t{'Label'}\t{'ScanNr'}\t{'ExpMass'}\t{'CalcMass'}\t"
                       f"{'seq_len'}\t{'charge1'}\t{'charge2'}\t{'charge3'}\t{'charge4'}\t{'SP'}\t"
                       f"{'aromaticity'}\t{'instability_index'}\t{'gravy'}\t{'helix'}\t{'turn'}\t{'sheet'}\t{'BB'}\t"
                       #f"{'BB'}\t"
                       f"{'TIMScore'}\t{'RTScore'}\t{'xcorr'}\t{'deltaCN'}\t{'Peptide'}\t{'Proteins'}\n")
        id_index = 0

        for s_line in s_lines:
            id = s_line.low_scan
            charge = s_line.charge
            for i, m_line in enumerate(s_line.m_lines):
                xcorr = m_line.xcorr

                if i > 0:
                    continue

                if xcorr == 0:
                    continue
                if i == len(s_line.m_lines)-1:
                    continue
                else:
                    delta_cn = s_line.m_lines[i+1].delta_cn

                #delta_cn = m_line.delta_cn
                label = -1 if m_line.is_reverse() else 1
                peptide = m_line.sequence
                proteins = [l_line.locus_name for l_line in m_line.l_lines]
                #proteins = [protein.split("|")[1] for protein in proteins if "contaminant" not in protein]
                if len(proteins) == 0:
                    continue

                unmod_seq = "".join([c for c in m_line.get_clean_seq() if c.isalpha()])
                seq_len = len(unmod_seq)

                get_aromaticity = lambda x: ProteinAnalysis(x).aromaticity()
                get_instability_index = lambda x: ProteinAnalysis(x).instability_index()
                get_gravy = lambda x: ProteinAnalysis(x).gravy()
                get_helix = lambda x: ProteinAnalysis(x).secondary_structure_fraction()[0]
                get_turn = lambda x: ProteinAnalysis(x).secondary_structure_fraction()[1]
                get_sheet = lambda x: ProteinAnalysis(x).secondary_structure_fraction()[2]

                aas = 'ARNDCEQGHILKMFPSTWYV'
                bbs = [610, 690, 890, 610, 360, 970, 510, 810, 690, -1450, -1650, 460, -660, -1520, -170, 420, 290,
                       -1200, -1430, -750]
                BB_MAP = {aa: bb for aa, bb in zip(aas, bbs)}

                def compute_bull_breese(peptide):
                    bb = 0
                    for aa in peptide:
                        bb += BB_MAP[aa]
                    return bb / len(peptide)

                get_bb = lambda x: compute_bull_breese(x)

                """
                percolator_proteins = []
                try:
                    for locus_name in proteins:
                        if "Reverse" in locus_name:
                            percolator_proteins.append("random_seq_" + locus_name.split("|")[1])
                        else:
                            percolator_proteins.append(locus_name.split("|")[1])
                except IndexError:
                    print(s_line)"""

                proteins_serialized = " ".join(proteins)
                ExpMass = s_line.experimental_mass
                CalcMass = m_line.calculated_mass
                rtscore = 0 if m_line.tims_score is None else m_line.tims_score
                timscore = 0 if m_line.predicted_ook0 is None else m_line.predicted_ook0

                charges = [0]*4
                if charge == 1:
                    charges[0] = 1
                if charge == 2:
                    charges[1] = 1
                if charge == 3:
                    charges[2] = 1
                if charge == 4:
                    charges[3] = 1

                sp = m_line.sp

                pin_file.write(f"{id_index}\t{label}\t{id}\t{ExpMass}\t{CalcMass}\t"
                               f"{seq_len}\t{charges[0]}\t{charges[1]}\t{charges[2]}\t{charges[3]}\t{sp}\t"
                               f"{get_aromaticity(unmod_seq)}\t{get_instability_index(unmod_seq)}\t{get_gravy(unmod_seq)}\t"
                               f"{get_helix(unmod_seq)}\t{get_turn(unmod_seq)}\t{get_sheet(unmod_seq)}\t{get_bb(unmod_seq)}\t"
                               #f"{get_bb(unmod_seq)}\t"
                               f"{timscore}\t{rtscore}\t{xcorr}\t{delta_cn}\t{peptide}\t{proteins_serialized}\n")
                id_index += 1



if __name__ == '__main__':
    args = parse_args()
    print(args)

    convert_sqt_to_pin(args.sqt)
