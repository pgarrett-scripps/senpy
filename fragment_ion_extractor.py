import argparse
import os
from dataclasses import dataclass

from pyteomics import mass
from senpy_package.senpy.ms2.parser import parse_file_incremental as parse_ms2_file_incremental
from senpy_package.senpy.dtaSelectFilter.parser import parse_file as parse_dta_filter_file


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

    for i in range(len(clean_peptide)):
        for ion_type in ion_types:
            for loss_type in losses:
                for charge in charges:
                    if ion_type in 'abc':

                        abc_ion_peptide = clean_peptide[:i + 1]

                        frag_ion_mass = mass.fast_mass(abc_ion_peptide, ion_type=ion_type, charge=charge)
                        frag_ion_mass -= losses[loss_type] / charge  # Neutral Loss

                        residue_modifications_list = [abc_ion_peptide.count(aa) * mass_shift for aa, mass_shift in
                                                      residue_modifications.items()]
                        frag_ion_mass += sum(residue_modifications_list) / charge  # Residue specific modifications
                        ptm_list = [ptm_mass for aa_index, ptm_mass in ptm_dict.items() if aa_index <= i]
                        frag_ion_mass += sum(ptm_list) / charge

                        fragment_ion = FragmentIon(ion_type, i + 1, losses[loss_type], loss_type, charge, frag_ion_mass)
                        yield fragment_ion
                    elif ion_type in 'xyz':

                        xyz_ion_peptide = clean_peptide[i:]

                        frag_ion_mass = mass.fast_mass(xyz_ion_peptide, ion_type=ion_type, charge=charge)
                        frag_ion_mass -= losses[loss_type] / charge  # Neutral Loss

                        residue_modifications_list = [xyz_ion_peptide.count(aa) * mass_shift for aa, mass_shift in
                                                      residue_modifications.items()]
                        frag_ion_mass += sum(residue_modifications_list) / charge  # Residue specific modifications

                        ptm_list = [ptm_mass for aa_index, ptm_mass in ptm_dict.items() if aa_index >= i]
                        frag_ion_mass += sum(ptm_list) / charge

                        fragment_ion = FragmentIon(ion_type, len(xyz_ion_peptide), losses[loss_type], loss_type, charge,
                                                   frag_ion_mass)
                        yield fragment_ion
                    else:
                        print("ion type not supported: ", ion_type)
                        raise NotImplemented


def get_fragment_ions_information(ms2_file, dta_select_filter_file, fragment_types, fragment_charges, fragment_losses,
                                  residue_modifications):
    supported_residues = set('ARNDCQGEHILKMFPSTWYV')
    max_ppm = 40

    # Fragment ion parameters
    print("fragment_types: ", fragment_types)
    print("fragment_charges: ", fragment_charges)
    print("fragment_losses: ", fragment_losses)

    # Parse DTASelect-filter file
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
    print(f"{len(dta_filter_dict)} ms2 scans identified in dta-filter")

    # Create outfile for fragment ions
    out_file = open(f"{ms2_file.split('.')[0]}.ions", "w", buffering=1_000_000)
    out_file.write(f"H\tFragment Types\t{fragment_types}\n")
    out_file.write(f"H\tFragment Charges\t{fragment_charges}\n")
    out_file.write(f"H\tFragment Losses\t{fragment_losses}\n")
    out_file.write(
        "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format("sequence", "charge", "scan_number", "collision_energy",
                                                      "max_fragment_intensity", "identified_fragment_codes",
                                                      "identified_masses_ppm", "identified_masses",
                                                      "identified_intensities"))

    print("Reading: ", ms2_file)
    invalid_residue_count = 0
    s_line_generator = parse_ms2_file_incremental(ms2_file)
    for s_line in s_line_generator:
        if s_line.low_scan not in dta_filter_dict:
            continue

        assert (s_line.z_line.charge == dta_filter_dict[s_line.low_scan].charge)  # sanity check
        unique_line = dta_filter_dict[s_line.low_scan]

        # skip peptides with invalid Residues
        clean_sequence = unique_line.get_clean_seq()
        if not set(clean_sequence).issubset(supported_residues):
            invalid_residue_count += 1
            continue

        collision_energy = s_line.get_i_line_dict()['Collision Energy']
        fragment_ions = get_fragment_ions(clean_sequence, fragment_types, fragment_charges,
                                          fragment_losses, residue_modifications)

        fragment_ion_bins = {}
        for fragment_ion in fragment_ions:
            start_bin_key = int((fragment_ion.mass - fragment_ion.mass * max_ppm / 1_000_000) * 100)
            end_bin_key = int((fragment_ion.mass + fragment_ion.mass * max_ppm / 1_000_000) * 100)
            for bin_key in range(start_bin_key, end_bin_key + 1):
                if bin_key not in fragment_ion_bins:
                    fragment_ion_bins[bin_key] = []
                fragment_ion_bins[bin_key].append(fragment_ion)

        identified_fragment_codes = []
        identified_masses_ppm = []
        identified_masses = []
        identified_intensities = []
        max_fragment_intensity = max(s_line.get_intensity_spectra())

        for mass, intensity in zip(s_line.get_mass_spectra(), s_line.get_intensity_spectra()):
            bin_key = int(mass * 100)

            if bin_key not in fragment_ion_bins:
                continue

            for fragment_ion in fragment_ion_bins[bin_key]:
                fragment_ion_ppm = (fragment_ion.mass - mass) / fragment_ion.mass * 1_000_000
                if abs(fragment_ion_ppm) <= max_ppm:
                    # found fragment ion!
                    identified_fragment_codes.append(fragment_ion.encode_ion())
                    identified_masses_ppm.append(fragment_ion_ppm)
                    identified_masses.append(mass)
                    identified_intensities.append(intensity)

        # print(unique_line.get_clean_seq())
        # print(identified_fragment_codes, identified_intensities)
        # find fragment ions in ms2 spectra
        """my_cmap = plt.get_cmap("viridis")
        colors = [my_cmap(abs(ppm/40)) for ppm in identified_masses_ppm]
        plt.title("{} {} {} {}".format(unique_line.sequence, max_fragment_intensity, max(identified_intensities), collision_energy))
        plt.bar(identified_masses, identified_intensities, width=5, color=colors)
        plt.show()"""

        identified_masses_ppm = [str(round(x, 1)) for x in identified_masses_ppm]
        identified_intensities = [str(round(x, 1)) for x in identified_intensities]
        identified_masses = [str(round(x, 5)) for x in identified_masses]

        out_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(unique_line.sequence,
                                                                     unique_line.charge,
                                                                     unique_line.low_scan,
                                                                     collision_energy,
                                                                     max_fragment_intensity,
                                                                     ";".join(identified_fragment_codes),
                                                                     ";".join(identified_masses_ppm),
                                                                     ';'.join(identified_masses),
                                                                     ";".join(identified_intensities)))
    out_file.close()

    print(f"invalid_residue_count: {invalid_residue_count}")


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
