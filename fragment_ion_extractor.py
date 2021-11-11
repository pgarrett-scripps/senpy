import argparse
import json
import os
from dataclasses import dataclass
import matplotlib.pyplot as plt

from pyteomics import mass
from senpy.ms2.parser import parse_file_incremental as parse_ms2_file_incremental
from senpy.dtaSelectFilter.parser import parse_file as parse_dta_filter_file


def get_fragment(peptide, ion_type, ion_number, loss, charge):
    if ion_type in 'abc':
        return mass.fast_mass(peptide[:ion_number], ion_type=ion_type, charge=charge) - loss / charge + \
               peptide[:ion_number].count("C") * 57.02146 / charge
    elif ion_type in 'xyz':
        return mass.fast_mass(peptide[ion_number:], ion_type=ion_type, charge=charge) - loss / charge + \
               peptide[len(peptide) - ion_number:].count("C") * 57.02146 / charge
    else:
        print("ion type not supported: ", ion_type)
        raise NotImplemented


@dataclass
class FragmentIon:
    ion_type: str
    ion_number: int
    loss: float
    loss_type: str
    charge: int
    mass: float

    def encode_ion(self):
        return f"{self.ion_type}{self.ion_number}_{self.charge}_{self.loss_type}"


def get_ptm_index_dict(peptide):
    # extract ptm info
    ptm_dict = {}
    while "(" in peptide:
        start_index_of_lowest_index_ptm = peptide.find("(")
        end_index_of_lowest_index_ptm = peptide.find(")")
        ptm_residue = peptide[start_index_of_lowest_index_ptm - 1]

        ptm_mass = float(peptide[start_index_of_lowest_index_ptm + 1:end_index_of_lowest_index_ptm])
        peptide = peptide[:start_index_of_lowest_index_ptm] + peptide[end_index_of_lowest_index_ptm + 1:]
        ptm_dict[start_index_of_lowest_index_ptm - 1] = ptm_mass

    return ptm_dict


def remove_ptm(peptide):
    while "(" in peptide:
        start_index_of_lowest_index_ptm = peptide.find("(")
        end_index_of_lowest_index_ptm = peptide.find(")")
        peptide = peptide[:start_index_of_lowest_index_ptm] + peptide[end_index_of_lowest_index_ptm + 1:]

    return peptide

def get_fragment_ions(peptide, ion_types, charges, losses, residue_modifications):
    ptm_dict = get_ptm_index_dict(peptide)
    clean_peptide = remove_ptm(peptide)

    abc_ion_mass_offset = 0

    total_ptm_shift = 0
    for aa in residue_modifications:
        total_ptm_shift += clean_peptide.count(aa) * residue_modifications[aa]
    xyz_ion_mass_offset = sum(ptm_dict.values()) + total_ptm_shift
    for i in range(len(clean_peptide)):
        for ion_type in ion_types:
            for loss_type in losses:
                for charge in charges:
                    if ion_type in 'abc':

                        abc_ion_peptide = clean_peptide[:i + 1]

                        frag_ion_mass = mass.fast_mass(abc_ion_peptide, ion_type=ion_type, charge=charge)
                        frag_ion_mass -= losses[loss_type] / charge # Neutral Loss

                        residue_modifications_list = [abc_ion_peptide.count(aa) * mass_shift for aa, mass_shift in residue_modifications.items()]
                        frag_ion_mass += sum(residue_modifications_list) / charge # Residue specific modifications
                        ptm_list = [ptm_mass for aa_index, ptm_mass in ptm_dict.items() if aa_index <= i]
                        frag_ion_mass += sum(ptm_list) / charge

                        fragment_ion = FragmentIon(ion_type, i + 1, losses[loss_type], loss_type, charge, frag_ion_mass)
                        yield fragment_ion
                    elif ion_type in 'xyz':

                        xyz_ion_peptide = clean_peptide[i:]

                        frag_ion_mass = mass.fast_mass(xyz_ion_peptide, ion_type=ion_type, charge=charge)
                        frag_ion_mass -= losses[loss_type] / charge  # Neutral Loss

                        residue_modifications_list = [xyz_ion_peptide.count(aa) * mass_shift for aa, mass_shift in residue_modifications.items()]
                        frag_ion_mass += sum(residue_modifications_list) / charge # Residue specific modifications

                        ptm_list = [ptm_mass for aa_index, ptm_mass in ptm_dict.items() if aa_index >= i]
                        frag_ion_mass += sum(ptm_list) / charge

                        fragment_ion = FragmentIon(ion_type, len(xyz_ion_peptide), losses[loss_type], loss_type, charge,
                                                   frag_ion_mass)
                        yield fragment_ion
                    else:
                        print("ion type not supported: ", ion_type)
                        raise NotImplemented


def get_fragment_ions_information(ms2_file, dta_select_filter_file, fragment_types, fragment_charges, fragment_losses, residue_modifications):
    print("fragment_types: ", fragment_types)
    print("fragment_charges: ", fragment_charges)
    print("fragment_losses: ", fragment_losses)

    ms2_file_name = os.path.basename(ms2_file).split(".")[0]
    print("MS2 File Name: ", ms2_file_name)
    print("Reading: ", dta_select_filter_file)
    h_lines, locus_lines, end_lines = parse_dta_filter_file(dta_select_filter_file)
    dta_filter_dict = {}
    # map appropriate file scan numbers to unique lines
    for locus_line in locus_lines:
        for unique_line in locus_line.unique_lines:
            if unique_line.file_name == ms2_file_name:
                dta_filter_dict[unique_line.low_scan] = unique_line

    out_file = open("tmp.out", "w")
    print("Reading: ", ms2_file)
    s_line_generator = parse_ms2_file_incremental(ms2_file)
    for s_line in s_line_generator:
        if s_line.low_scan not in dta_filter_dict:
            continue

        collision_energy = s_line.get_i_line_dict()['Collision Energy']
        unique_line = dta_filter_dict[s_line.low_scan]
        fragment_ions = get_fragment_ions(unique_line.get_clean_seq(), fragment_types, fragment_charges,
                                          fragment_losses, residue_modifications)

        fragment_ion_bins = {}
        for fragment_ion in fragment_ions:
            bin_key = int(fragment_ion.mass * 100)
            if bin_key not in fragment_ion_bins:
                fragment_ion_bins[bin_key] = []
            fragment_ion_bins[bin_key].append(fragment_ion)

        identified_fragment_codes = []
        identified_masses = []
        identified_intensities = []
        max_fragment_intensity = max(s_line.get_intensity_spectra())

        for mass, intensity in zip(s_line.get_mass_spectra(), s_line.get_intensity_spectra()):
            bin_key = int(mass * 100)

            if bin_key not in fragment_ion_bins:
                continue

            for fragment_ion in fragment_ion_bins[bin_key]:
                if (mass - fragment_ion.mass) <= mass * 40 / 1_000_000:
                    # found fragment ion!
                    identified_fragment_codes.append(fragment_ion.encode_ion())
                    identified_masses.append(str(mass))
                    identified_intensities.append(str(round(intensity)))
        # print(unique_line.get_clean_seq())
        # print(identified_fragment_codes, identified_intensities)
        # find fragment ions in ms2 spectra
        """plt.title("{} {} {} {}".format(unique_line.sequence, max_fragment_intensity, max(identified_intensities), collision_energy))
        plt.bar(identified_masses, identified_intensities, width=5)
        plt.show()"""

        out_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(unique_line.sequence,
                                                                 unique_line.charge,
                                                                 unique_line.low_scan,
                                                                 collision_energy,
                                                                 max_fragment_intensity,
                                                                 ";".join(identified_fragment_codes),
                                                                 ";".join(identified_masses),
                                                                 ";".join(identified_intensities)))
    out_file.close()


def parse_args():
    # Parse Arguments
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('ms2_file', metavar='ms2_file', type=str, help='path to ms2_file')
    parser.add_argument('dta_select_filter_file', metavar='dta_select_filter_file', type=str,
                        help='path to dta_select_filter_file')

    parser.add_argument('-f', '--fragments', nargs='+', help='fragment ions to generate', default=['b', 'y'])
    parser.add_argument('-c', '--fragment_ion_charges', nargs='+', help='fragment ion charges to generate',
                        default=[1, 2, 3])
    parser.add_argument('-l', '--neutral_losses', help='fragment ion neutral losses charges to generate',
                        nargs='+', default=["H20_18.01051", "NH3_17.02647", "CO_27.99491"])
    parser.add_argument('-m', '--residue_modification', help='residue specific modifications ex: Cysteine ~57',
                        nargs='+', default=["C_57.02146"])
    args = parser.parse_args()

    # Parse neutral losses
    tmp_loss_dict = {}
    for loss_string in args.neutral_losses:
        loss_symbol = loss_string.split("_")[0]
        loss_mass = float(loss_string.split("_")[1])
        tmp_loss_dict[loss_symbol] = loss_mass
    tmp_loss_dict['NA'] = 0
    args.neutral_losses = tmp_loss_dict

    # Parse residue modifications
    tmp_mod_dict = {}
    for mod_string in args.residue_modification:
        residue_symbol = mod_string.split("_")[0]
        mod_mass = float(mod_string.split("_")[1])
        tmp_mod_dict[residue_symbol] = mod_mass
    args.residue_modification = tmp_mod_dict

    # convert charges to integers
    args.fragment_ion_charges = [int(charge) for charge in args.fragment_ion_charges]
    return args

if __name__ == "__main__":
    args = parse_args()
    print(args)

    """    for ion in get_fragment_ions("P(115.007)EPC(115.007)TIDE(115.007)", ['b','y'], [2], {'NA':0}, {'C':57.02146}):
        print(ion)"""

    get_fragment_ions_information(args.ms2_file,
                                  args.dta_select_filter_file,
                                  args.fragments,
                                  args.fragment_ion_charges,
                                  args.neutral_losses,
                                  args.residue_modification)